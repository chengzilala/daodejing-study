#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 web/content/ 下的《道德经》Markdown 编译成 web/dist/ 静态站点。

用法：
    python3 web/build.py

依赖：仅 Python 3 标准库，无需安装任何第三方包。
"""
import json
import re
import shutil
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parent
CONTENT = WEB / "content"
TEMPLATES = WEB / "templates"
ASSETS = WEB / "assets"
DIST = WEB / "dist"

CN_DIGITS = "零一二三四五六七八九"


def cn_num(n):
    """阿拉伯数字转中文（1→一，10→十，81→八十一）。"""
    if n < 10:
        return CN_DIGITS[n]
    if n == 10:
        return "十"
    if n < 20:
        return "十" + CN_DIGITS[n % 10]
    if n < 100:
        tens, ones = divmod(n, 10)
        return CN_DIGITS[tens] + "十" + (CN_DIGITS[ones] if ones else "")
    return str(n)


def load_config():
    with open(WEB / "site.config.json", encoding="utf-8") as f:
        return json.load(f)


def read_template(name):
    return (TEMPLATES / name).read_text(encoding="utf-8")


def _flush(ch, section, buf):
    text = "\n".join(buf).strip()
    if not text:
        return
    lines = [s.strip() for s in text.split("\n") if s.strip()]
    if section == "原文":
        ch["yuanwen"] = lines
    elif section == "白话":
        ch["baihua"] = lines
    elif section == "导读":
        ch["daodu"] = lines


def _parse_file(path):
    text = path.read_text(encoding="utf-8")
    result = []
    cur = None
    section = None
    buf = []
    for raw in text.split("\n"):
        line = raw.strip()
        m = re.match(r"^##\s*第?(\d+)\s*章\s*(.*)$", line)
        if m:
            if cur is not None:
                _flush(cur, section, buf)
                result.append(cur)
            no = int(m.group(1))
            topic = m.group(2).strip()
            cur = {"no": no,
                   "topic": topic or "第%s章" % cn_num(no),
                   "yuanwen": [], "baihua": [], "daodu": []}
            section = None
            buf = []
            continue
        m2 = re.match(r"^###\s*(原文|白话|导读)", line)
        if m2 and cur is not None:
            _flush(cur, section, buf)
            section = m2.group(1)
            buf = []
            continue
        if cur is not None and line:
            buf.append(line)
    if cur is not None:
        _flush(cur, section, buf)
        result.append(cur)
    return result


def parse_chapters():
    chapters = []
    files = sorted(p for p in CONTENT.glob("*.md") if p.name != "_模板.md")
    for path in files:
        chapters.extend(_parse_file(path))
    chapters.sort(key=lambda c: c["no"])
    return chapters


def render_html(template, mapping):
    out = template
    for key, val in mapping.items():
        out = out.replace("@@" + key + "@@", str(val))
    return out


def para_html(lines):
    return "".join("<p>%s</p>\n" % s for s in lines)


def build_index(cfg, chapters):
    cards = []
    for c in chapters:
        group = "dao" if c["no"] <= 37 else "de"
        cards.append(
            '<a class="ddj-card" data-group="%s" href="chapter/%d.html">'
            '<span class="ddj-no">第%s章</span>'
            '<span class="ddj-topic">%s</span></a>'
            % (group, c["no"], cn_num(c["no"]), c["topic"])
        )
    mapping = {
        "SITE_NAME": cfg["siteName"],
        "SITE_DESC": cfg["siteDescription"],
        "ASSETS": "",
        "CARDS": "\n".join(cards),
    }
    return render_html(read_template("index.html"), mapping)


def build_chapter(cfg, chapters, c, idx):
    prev = chapters[idx - 1] if idx > 0 else None
    nxt = chapters[idx + 1] if idx < len(chapters) - 1 else None
    prev_html = ('<a class="ddj-prev" href="%d.html">← 第%s章</a>'
                 % (prev["no"], cn_num(prev["no"]))) if prev else '<span class="ddj-prev empty"></span>'
    next_html = ('<a class="ddj-next" href="%d.html">第%s章 →</a>'
                 % (nxt["no"], cn_num(nxt["no"]))) if nxt else '<span class="ddj-next empty"></span>'
    mapping = {
        "SITE_NAME": cfg["siteName"],
        "ASSETS": "../",
        "TITLE": "第%s章 · %s" % (cn_num(c["no"]), c["topic"]),
        "CHAPTER_NO": "第%s章" % cn_num(c["no"]),
        "TOPIC": c["topic"],
        "YUANWEN": para_html(c["yuanwen"]),
        "BAIHUA": para_html(c["baihua"]),
        "DAODU": para_html(c["daodu"]),
        "PREV": prev_html,
        "NEXT": next_html,
    }
    return render_html(read_template("chapter.html"), mapping)


def main():
    cfg = load_config()
    chapters = parse_chapters()
    if not chapters:
        print("未解析到任何章节，请检查 web/content/ 下的 Markdown。")
        sys.exit(1)
    print("解析到 %d 章" % len(chapters))

    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "chapter").mkdir(parents=True, exist_ok=True)

    (DIST / "index.html").write_text(build_index(cfg, chapters), encoding="utf-8")
    for i, c in enumerate(chapters):
        (DIST / "chapter" / ("%d.html" % c["no"])).write_text(
            build_chapter(cfg, chapters, c, i), encoding="utf-8")

    if ASSETS.exists():
        shutil.copytree(ASSETS, DIST / "assets")
    print("构建完成：web/dist/")


if __name__ == "__main__":
    main()
