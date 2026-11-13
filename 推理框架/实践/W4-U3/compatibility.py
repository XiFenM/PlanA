"""Explicitly reviewed vLLM profiles; no open-ended version/flag guessing."""
from __future__ import annotations
import copy


PROFILES = {
    "0.26.0": {
        "version": "0.26.0", "source_commit": "568afb3a13806beb53bb2e6bd518269357b237c0",
        "disable_prefix_caching": "--no-enable-prefix-caching",
        "disable_log_requests": "--no-enable-log-requests",
    },
    "0.33.0": {
        "version": "0.33.0", "source_commit": "4ba787ec9959e566d3b587a796dff07673324da5",
        "disable_prefix_caching": "--disable-prefix-caching",
        "disable_log_requests": "--disable-log-requests",
    },
}
COMMON_FLAGS = (
    "--max-num-batched-tokens", "--max-num-seqs", "--max-model-len",
    "--enable-chunked-prefill", "--no-async-scheduling", "--enforce-eager",
    "--generation-config", "--served-model-name", "--logprobs-mode",
    "--quantization", "--block-size",
)


def profile_for_version(version):
    if not isinstance(version,str):
        raise ValueError("vLLM version must be a string")
    base=version.split("+",1)[0]
    if base not in PROFILES:
        raise ValueError(f"仅支持已核验的 vLLM {', '.join(PROFILES)}；实际为 {version or '未安装'}")
    return copy.deepcopy(PROFILES[base])


def required_flags(version):
    profile=profile_for_version(version)
    return COMMON_FLAGS+(profile["disable_prefix_caching"],profile["disable_log_requests"])


def missing_cli_flags(help_text,version):
    # v0.33 accepts hidden --no-enable-* legacy aliases too, but use its visible
    # --disable-* spellings; absence of a hidden alias is not absence of support.
    return [flag for flag in required_flags(version) if flag not in help_text]
