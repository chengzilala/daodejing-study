#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地预览：把 web/dist/ 作为站点根目录起一个静态服务。

用法：
    python3 web/serve.py
    然后浏览器打开 http://localhost:5173
"""
import http.server
import socketserver
import sys
from pathlib import Path

PORT = 5173
DIST = Path(__file__).resolve().parent / "dist"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST), **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write("[serve] %s\n" % (fmt % args))


def main():
    if not (DIST / "index.html").exists():
        print("还没有构建产物，请先运行：python3 web/build.py")
        sys.exit(1)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("已在本地启动：http://localhost:%d  （Ctrl+C 停止）" % PORT)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止。")


if __name__ == "__main__":
    main()
