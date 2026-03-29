#!/usr/bin/env python3
"""
LazyTree 研究ダッシュボード用チャットサーバー。
Railway / ローカル兼用。PORT環境変数でポート番号を指定可（デフォルト8787）。
"""
from __future__ import annotations

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

try:
    from openai import OpenAI
    _openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    USE_OPENAI = bool(os.environ.get("OPENAI_API_KEY"))
except ImportError:
    USE_OPENAI = False
    _openai_client = None

WEB_DIR = Path(__file__).parent


def chat_reply(system: str, user_message: str) -> str:
    """チャット応答を生成。OpenAI gpt-4o-miniを使用。"""
    if USE_OPENAI and _openai_client:
        resp = _openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_message},
            ],
            max_tokens=500,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
    return "（OPENAI_API_KEY が設定されていません）"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def log_message(self, fmt, *args):
        pass

    def do_POST(self):
        if self.path == "/chat":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            user_msg = body.get("message", "")
            context = body.get("context", "")

            system = (
                context + "\n\n"
                "簡潔かつ丁寧に日本語で答えてください。"
                "数値データや具体例を交えて返答してください。"
                "返答は3〜5文程度が目安です。"
            )
            reply = chat_reply(system, user_msg)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"reply": reply}, ensure_ascii=False).encode())
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8787))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"起動: http://0.0.0.0:{port}")
    server.serve_forever()
