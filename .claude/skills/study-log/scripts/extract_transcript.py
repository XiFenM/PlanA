#!/usr/bin/env python3
"""提取 Claude Code 会话记录（JSONL）为可读的对话 Markdown。

用法：
  extract_transcript.py list                          # 列出本项目全部会话（新→旧）
  extract_transcript.py extract --latest              # 提取最近一个会话
  extract_transcript.py extract --session d88c65bd    # 按 session id 前缀提取
  extract_transcript.py extract --latest --date 2026-07-03   # 只保留某天的消息
  extract_transcript.py extract --latest --tools -o /tmp/dump.md

只保留主链上的 user/assistant 文本；自动剔除 thinking、tool_use/tool_result、
subagent 侧链（isSidechain）、meta 消息、压缩摘要（isCompactSummary）、
<system-reminder> 与本地命令注入块。--tools 时以单行标注工具调用。
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

STRIP_PATTERNS = [
    re.compile(r"<system-reminder>.*?</system-reminder>", re.S),
    re.compile(r"<local-command-caveat>.*?</local-command-caveat>", re.S),
    re.compile(r"<local-command-stdout>.*?</local-command-stdout>", re.S),
    re.compile(r"<command-message>.*?</command-message>", re.S),
    re.compile(r"<command-args>.*?</command-args>", re.S),
    re.compile(r"<ide_selection>.*?</ide_selection>", re.S),
]
COMMAND_NAME_RE = re.compile(r"<command-name>(.*?)</command-name>", re.S)


def project_dir(cwd: str) -> Path:
    slug = "-" + cwd.strip("/").replace("/", "-").replace(".", "-")
    return Path.home() / ".claude" / "projects" / slug


def iter_records(path: Path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def clean_text(text: str) -> str:
    for pat in STRIP_PATTERNS:
        text = pat.sub("", text)
    m = COMMAND_NAME_RE.search(text)
    if m:
        text = COMMAND_NAME_RE.sub("", text)
        cmd = m.group(1).strip()
        rest = text.strip()
        text = f"> ⌨️ 命令：{cmd}" + (f"\n\n{rest}" if rest else "")
    return text.strip()


def tool_brief(block: dict) -> str:
    name = block.get("name", "?")
    inp = block.get("input") or {}
    for key in ("file_path", "path", "description", "skill", "pattern", "query", "command"):
        if key in inp:
            val = str(inp[key]).replace("\n", " ")
            return f"{name}({val[:80]})"
    return name


def message_text(rec: dict, include_tools: bool) -> str:
    msg = rec.get("message") or {}
    content = msg.get("content")
    parts = []
    if isinstance(content, str):
        parts.append(content)
    elif isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            btype = block.get("type")
            if btype == "text":
                parts.append(block.get("text", ""))
            elif btype == "tool_use" and include_tools:
                parts.append(f"> 🔧 {tool_brief(block)}")
            # thinking / tool_result / image 一律跳过
    return clean_text("\n\n".join(p for p in parts if p and p.strip()))


def session_files(pdir: Path):
    files = sorted(pdir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        sys.exit(f"未找到会话文件：{pdir}")
    return files


def first_user_snippet(path: Path) -> str:
    for rec in iter_records(path):
        if rec.get("type") == "user" and not rec.get("isMeta") and not rec.get("isSidechain") \
                and not rec.get("isCompactSummary"):
            text = message_text(rec, include_tools=False)
            if text and not text.startswith("> ⌨️"):
                return text.replace("\n", " ")[:60]
    return "(无用户消息)"


def time_range(path: Path):
    first = last = None
    for rec in iter_records(path):
        ts = rec.get("timestamp")
        if ts:
            first = first or ts
            last = ts
    return first, last


def cmd_list(pdir: Path):
    print(f"{'SESSION':<10} {'开始':<17} {'结束':<17} {'大小':>7}  首条用户消息")
    for f in session_files(pdir):
        first, last = time_range(f)
        fmt = lambda ts: (ts or "?")[:16].replace("T", " ")
        size_kb = f.stat().st_size // 1024
        print(f"{f.stem[:8]:<10} {fmt(first):<17} {fmt(last):<17} {size_kb:>6}K  {first_user_snippet(f)}")


def cmd_extract(pdir: Path, args):
    files = session_files(pdir)
    if args.session:
        matches = [f for f in files if f.stem.startswith(args.session)]
        if not matches:
            sys.exit(f"没有以 {args.session} 开头的会话")
        target = matches[0]
    else:
        target = files[0]

    out_lines = [f"# 会话提取 · {target.stem[:8]}", ""]
    first, last = time_range(target)
    out_lines.append(f"> 时间范围：{first} → {last}" + (f" · 仅保留 {args.date}" if args.date else ""))
    out_lines.append("")

    n_msgs = 0
    for rec in iter_records(target):
        rtype = rec.get("type")
        if rtype not in ("user", "assistant"):
            continue
        if rec.get("isSidechain") or rec.get("isMeta"):
            continue
        ts = rec.get("timestamp") or ""
        if args.date and not ts.startswith(args.date):
            continue
        if rec.get("isCompactSummary"):
            out_lines += [f"## [{ts[11:16]}] （上下文压缩摘要，略）", ""]
            continue
        text = message_text(rec, include_tools=args.tools)
        if not text:
            continue
        role = "用户" if rtype == "user" else "Claude"
        out_lines += [f"## [{ts[11:16]}] {role}", "", text, ""]
        n_msgs += 1

    result = "\n".join(out_lines)
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"已写入 {args.output}（{n_msgs} 条消息，{len(result)//1024}K 字符）")
    else:
        print(result)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode", choices=["list", "extract"])
    ap.add_argument("--session", help="session id 前缀")
    ap.add_argument("--latest", action="store_true", help="取最近会话（extract 默认行为）")
    ap.add_argument("--date", help="只保留该日期（YYYY-MM-DD）的消息")
    ap.add_argument("--tools", action="store_true", help="以单行标注工具调用")
    ap.add_argument("-o", "--output", help="输出文件路径（默认打印 stdout）")
    ap.add_argument("--project", help="项目根目录（默认当前目录）", default=os.getcwd())
    args = ap.parse_args()

    pdir = project_dir(args.project)
    if args.mode == "list":
        cmd_list(pdir)
    else:
        cmd_extract(pdir, args)


if __name__ == "__main__":
    main()
