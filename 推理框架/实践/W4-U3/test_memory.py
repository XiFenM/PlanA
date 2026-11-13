import json
import subprocess
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from memory import (MemorySampler, _RocmSmiBackend, _SysfsBackend,
                    discover_sysfs_devices, normalize_bdf, parse_rocm_smi_json,
                    parse_server_memory)


def make_card(root, card, bdf, *, used=100, total=1000, vendor="0x1002"):
    physical = root / "pci" / bdf
    physical.mkdir(parents=True, exist_ok=True)
    (physical / "vendor").write_text(vendor)
    (physical / "mem_info_vram_used").write_text(str(used))
    (physical / "mem_info_vram_total").write_text(str(total))
    node = root / "drm" / card
    node.mkdir(parents=True)
    (node / "device").symlink_to(physical)
    return physical


def wait_for_samples(sampler, count=1):
    deadline = time.monotonic() + 2
    while time.monotonic() < deadline:
        with sampler._lock:
            if len(sampler._rows) >= count:
                return
        time.sleep(0.005)
    raise AssertionError("memory sampler did not emit the expected samples")


class SysfsTests(unittest.TestCase):
    def test_bdf_normalization_and_invalid_values(self):
        self.assertEqual(normalize_bdf("00000000:AB:00.0"), "0000:ab:00.0")
        self.assertEqual(normalize_bdf("ab:00.0"), "0000:ab:00.0")
        self.assertIsNone(normalize_bdf("0"))
        self.assertIsNone(normalize_bdf("0000:ab:00.8"))

    def test_discovery_ignores_connectors_and_deduplicates_physical_device(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            physical = make_card(root, "card0", "0000:ab:00.0")
            make_card(root, "card1", "0000:bc:00.0", vendor="0x10de")
            alias = root / "drm" / "card9"
            alias.mkdir()
            (alias / "device").symlink_to(physical)
            (root / "drm" / "card0-DP-1").mkdir()
            found = discover_sysfs_devices(root / "drm")
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0]["pci_bdf"], "0000:ab:00.0")

    def test_unreadable_counter_is_not_reported_as_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            physical = make_card(root, "card0", "0000:ab:00.0")
            found = discover_sysfs_devices(root / "drm")
            (physical / "mem_info_vram_used").unlink()
            item = _SysfsBackend(found, None).sample()["devices"][0]
            self.assertIsNone(item["used_bytes"])
            self.assertIn("FileNotFoundError", item["error"])

    def test_impossible_counter_is_explicit_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_card(root, "card0", "0000:ab:00.0", used=1001)
            item = _SysfsBackend(discover_sysfs_devices(root / "drm"), None).sample()["devices"][0]
            self.assertIsNone(item["used_bytes"])
            self.assertIn("invalid VRAM", item["error"])


class SmiTests(unittest.TestCase):
    def test_per_card_bytes_and_explicit_mapping(self):
        data = {"card0": {"PCI Bus": "0000:ab:00.0", "VRAM Total Memory (B)": "2,000",
                          "VRAM Total Used Memory (B)": "125"},
                "card1": {"PCI Bus": "0000:bc:00.0", "VRAM Total Memory (B)": 4000,
                          "VRAM Total Used Memory (B)": 500}}
        result = parse_rocm_smi_json("WARNING: query\n" + json.dumps(data), "bc:00.0")
        self.assertEqual(result["scope"], "matched_pci_bdf")
        self.assertEqual([d["used_bytes"] for d in result["devices"]], [500])
        unmapped = parse_rocm_smi_json(json.dumps(data))
        self.assertEqual(unmapped["scope"], "all_devices_unmapped")
        self.assertEqual(len(unmapped["devices"]), 2)

    def test_missing_bdf_does_not_fall_back_to_first_card(self):
        data = {"card0": {"VRAM Total Memory (B)": "1000", "VRAM Total Used Memory (B)": "10"}}
        result = parse_rocm_smi_json(json.dumps(data), "0000:ab:00.0")
        self.assertEqual(result["devices"], [])
        self.assertIn("not found", result["error"])

    def test_duplicate_bdf_is_ambiguous_not_one_device(self):
        data = {name: {"PCI Bus": "0000:ab:00.0", "VRAM Total Memory (B)": 1000,
                       "VRAM Total Used Memory (B)": used}
                for name, used in (("card0", 100), ("card1", 200))}
        result = parse_rocm_smi_json(json.dumps(data), "ab:00.0")
        self.assertEqual(result["scope"], "ambiguous_pci_bdf")
        self.assertEqual(len(result["devices"]), 2)
        self.assertIsNotNone(result["error"])

    def test_unknown_units_and_broken_json_remain_missing(self):
        data = {"card0": {"VRAM Total Memory (MiB)": "1000", "VRAM Total Used Memory (MiB)": "10"}}
        device = parse_rocm_smi_json(json.dumps(data))["devices"][0]
        self.assertIsNone(device["used_bytes"])
        self.assertIsNotNone(device["error"])
        self.assertIsNotNone(parse_rocm_smi_json("invalid json")["error"])

    def test_smi_query_has_bounded_timeout(self):
        with patch("memory.subprocess.run", side_effect=subprocess.TimeoutExpired(["rocm-smi"], 2)) as run:
            result = _RocmSmiBackend("/fake/rocm-smi", None).sample()
        self.assertEqual(run.call_args.kwargs["timeout"], 2.0)
        self.assertIsNotNone(result["error"])
        self.assertEqual(result["devices"], [])


class SamplerTests(unittest.TestCase):
    def test_blocked_query_has_bounded_stop_and_cannot_write_late_samples(self):
        entered, release = threading.Event(), threading.Event()

        class SlowBackend:
            name = "test_blocked_query"

            def sample(self):
                entered.set()
                release.wait(5)
                return {"devices": [], "scope": "unavailable", "error": "late result"}

        with tempfile.TemporaryDirectory() as tmp, \
             patch("memory._select_backend", return_value=SlowBackend()), \
             patch("memory._COMMAND_TIMEOUT", 0.01):
            sampler = MemorySampler(tmp).start()
            self.assertTrue(entered.wait(1))
            before = time.monotonic()
            try:
                summary = sampler.stop()
                self.assertLess(time.monotonic() - before, 2.5)
                self.assertEqual(summary["status"], "stop_timeout")
                self.assertFalse(summary["thread_stopped"])
            finally:
                release.set()
                sampler._thread.join(1)
            self.assertEqual((Path(tmp) / "memory_samples.jsonl").read_text(), "")

    def test_maps_requested_card_and_samples_change_without_cross_card_sum(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_card(root, "card0", "0000:ab:00.0", used=900)
            target = make_card(root, "card1", "0000:bc:00.0", used=100)
            sampler = MemorySampler(root / "results", 0.05, visible_bdf="bc:00.0", sysfs_root=root / "drm").start()
            wait_for_samples(sampler)
            (target / "mem_info_vram_used").write_text("300")
            wait_for_samples(sampler, 3)
            summary = sampler.stop()
            self.assertTrue(summary["thread_stopped"])
            self.assertTrue(summary["runtime_device_mapping_confirmed"])
            self.assertEqual(len(summary["devices"]), 1)
            self.assertEqual(summary["devices"][0]["sampled_max_used_bytes"], 300)
            self.assertEqual(summary["devices"][0]["first_used_bytes"], 100)
            self.assertEqual(sampler.stop(), summary)
            rows = [json.loads(line) for line in (root / "results" / "memory_samples.jsonl").read_text().splitlines()]
            self.assertEqual(len(rows), summary["sample_count"])
            self.assertGreaterEqual(summary["duration_seconds"], rows[-1]["elapsed_seconds"])
            self.assertEqual(json.loads((root / "results" / "memory_summary.json").read_text()), summary)

    def test_multiple_devices_unmapped_and_context_does_not_swallow_exception(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_card(root, "card0", "0000:ab:00.0", used=100)
            make_card(root, "card1", "0000:bc:00.0", used=500)
            sampler = MemorySampler(root / "results", 0.1, sysfs_root=root / "drm")
            with self.assertRaisesRegex(RuntimeError, "benchmark failed"):
                with sampler:
                    wait_for_samples(sampler)
                    raise RuntimeError("benchmark failed")
            summary = sampler.stop()
            self.assertEqual(summary["scope"], "all_devices_unmapped")
            self.assertFalse(summary["runtime_device_mapping_confirmed"])
            self.assertEqual(len(summary["devices"]), 2)
            self.assertNotIn("sampled_max_used_bytes", summary)

    def test_no_backend_records_unavailable_without_runtime_fallback(self):
        with tempfile.TemporaryDirectory() as tmp, patch("memory.shutil.which", return_value=None):
            sampler = MemorySampler(Path(tmp) / "results", 0.1, sysfs_root=Path(tmp) / "empty").start()
            wait_for_samples(sampler)
            summary = sampler.stop()
            self.assertEqual(summary["status"], "unavailable")
            self.assertTrue(summary["errors"])
            self.assertEqual(summary["devices"], [])

    def test_counter_failure_after_success_is_partial(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            card = make_card(root, "card0", "0000:ab:00.0")
            sampler = MemorySampler(root / "results", 0.05, sysfs_root=root / "drm").start()
            wait_for_samples(sampler)
            (card / "mem_info_vram_used").unlink()
            wait_for_samples(sampler, 3)
            summary = sampler.stop()
            self.assertEqual(summary["status"], "partial")
            self.assertEqual(summary["devices"][0]["sampled_max_used_bytes"], 100)
            self.assertGreater(summary["devices"][0]["failed_samples"], 0)

    def test_existing_results_not_overwritten_and_invalid_intervals_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            marker = path / "memory_samples.jsonl"
            marker.write_text("keep")
            with self.assertRaises(FileExistsError):
                MemorySampler(path).start()
            self.assertEqual(marker.read_text(), "keep")
        for interval in (0, -1, float("nan"), float("inf"), True):
            with self.subTest(interval=interval), self.assertRaises(ValueError):
                MemorySampler("unused", interval)


class LogTests(unittest.TestCase):
    def test_real_version_log_variants_preserve_three_scopes(self):
        text = ("(EngineCore pid=42) Model loading took 2.89 GiB and 2.730597 seconds\n"
                "Available KV cache memory: 30.39 GiB\n"
                "\x1b[31mGPU KV cache size: 1,138,160 tokens\x1b[0m\n")
        data = parse_server_memory(text)
        self.assertEqual(data["model_loading_gib"], 2.89)
        self.assertEqual(data["kv_available_gib"], 30.39)
        self.assertEqual(data["kv_capacity_tokens"], 1138160)
        self.assertEqual(data["warnings"], [])
        self.assertEqual(data["reports"][0]["literal"], "2.89")
        with_memory = parse_server_memory("Model loading took 1.25 GiB memory and 1.0 seconds")
        self.assertEqual(with_memory["model_loading_gib"], 1.25)
        self.assertIsNone(with_memory["kv_available_gib"])
        self.assertNotIn("model_loading_bytes", data)

    def test_conflicting_reports_do_not_silently_select_or_sum(self):
        text = ("Model loading took 2.89 GiB and 1.0 seconds\n"
                "Model loading took 1.20 GiB memory and 1.0 seconds\n")
        data = parse_server_memory(text)
        self.assertIsNone(data["model_loading_gib"])
        self.assertIn("conflicting", " ".join(data["warnings"]))
        self.assertEqual(len(data["reports"]), 2)

    def test_malformed_log_number_is_a_warning_not_a_measurement(self):
        data = parse_server_memory("GPU KV cache size: 1,12 tokens")
        self.assertIsNone(data["kv_capacity_tokens"])
        self.assertIn("invalid numeric", " ".join(data["warnings"]))


if __name__ == "__main__":
    unittest.main()
