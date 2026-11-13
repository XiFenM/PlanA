"""Versioned CLI and evidence labels; no installed vLLM/GPU needed."""
from __future__ import annotations
import unittest
from compatibility import PROFILES,COMMON_FLAGS,profile_for_version,missing_cli_flags
import run


class CompatibilityTests(unittest.TestCase):
    def test_only_reviewed_public_versions_with_build_suffixes(self):
        self.assertEqual(profile_for_version("0.33.0+rocm72")["version"],"0.33.0")
        self.assertEqual(profile_for_version("0.26.0+rocm723")["version"],"0.26.0")
        for value in ("0.34.0","0.33.0rc1","0.33.1",None,""):
            with self.assertRaises(ValueError):profile_for_version(value)

    def test_new_visible_help_does_not_need_hidden_legacy_aliases(self):
        help_text="\n".join(COMMON_FLAGS)+"\n--enable-prefix-caching, --disable-prefix-caching\n--enable-log-requests, --disable-log-requests\n"
        self.assertNotIn("--no-enable-prefix-caching",help_text)
        self.assertEqual(missing_cli_flags(help_text,"0.33.0+rocm72"),[])
        self.assertIn("--no-enable-prefix-caching",missing_cli_flags(help_text,"0.26.0"))
        self.assertIn("--disable-prefix-caching",missing_cli_flags(help_text.replace("--disable-prefix-caching",""),"0.33.0"))

    def test_commands_follow_profile_without_changing_workload(self):
        for variant in ("bf16","awq"):
            old=run.server_command("/model",variant,"bfloat16",8123,vllm_version="0.26.0")
            new=run.server_command("/model",variant,"bfloat16",8123,vllm_version="0.33.0+rocm72")
            self.assertEqual([(a,b) for a,b in zip(old,new) if a!=b],[
                ("--no-enable-prefix-caching","--disable-prefix-caching"),
                ("--no-enable-log-requests","--disable-log-requests")])

    def test_method_labels_actual_profile_and_keeps_numerical_gates(self):
        old=run.method("0.26.0+rocm723")
        new=run.method("0.33.0+rocm72")
        self.assertEqual(new["vllm_target"],"0.33.0")
        self.assertEqual(new["vllm_profile"]["source_commit"],"4ba787ec9959e566d3b587a796dff07673324da5")
        for key in ("reference","run_order","quality","memory","budget","requests_per_round"):
            self.assertEqual(old[key],new[key])
        self.assertFalse(new["full_model_cpu_reference"])

    def test_version_error_includes_observed_version_and_profiles_are_copied(self):
        errors=run.environment_reasons({"packages":{"vllm":"0.34.0"}})
        self.assertTrue(any("实际为 0.34.0" in e for e in errors))
        p=profile_for_version("0.33.0")
        p["version"]="changed"
        self.assertEqual(PROFILES["0.33.0"]["version"],"0.33.0")


if __name__=="__main__":unittest.main()
