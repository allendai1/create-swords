"""Receives from Studio into this folder: the balance export (ServerStorage.Builders.ExportBalance) and playtest logs
(ServerScriptService.PlaytestLog, posted every 15 s during Play, appended to playtests/<session>.jsonl).
python Development/sim/receive.py   (leave it running while you playtest; Ctrl+C to stop)
Only Studio's posts get in: header X-Studio: 1 and Host 127.0.0.1:8765 or localhost:8765, else 403 (a web page can't add
the header without a CORS preflight, which this refuses; the Host check stops DNS rebinding). Bodies must be JSON, else 400."""
import http.server
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = {"balance.json", "golden.json"}
PLAYTESTS = os.path.join(HERE, "playtests")


class Handler(http.server.BaseHTTPRequestHandler):
    def reply(self, code):
        self.send_response(code)
        self.end_headers()
        if code == 200:
            self.wfile.write(b"ok")

    def from_studio(self):
        port = self.server.server_address[1]
        return self.headers.get("X-Studio") == "1" and self.headers.get("Host") in (f"127.0.0.1:{port}", f"localhost:{port}")

    def do_POST(self):
        if not self.from_studio():
            return self.reply(403)
        name = self.path.strip("/")
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        try:
            data = json.loads(body)
        except ValueError:
            return self.reply(400)
        session = re.fullmatch(r"playtest/([\w-]+)", name)
        if session:
            events = data
            os.makedirs(PLAYTESTS, exist_ok=True)
            with open(os.path.join(PLAYTESTS, session[1] + ".jsonl"), "a", encoding="utf-8", newline="\n") as f:
                f.writelines(json.dumps(e) + "\n" for e in events)
            print(f"playtest {session[1]}: +{len(events)} events", flush=True)
            return self.reply(200)
        if name not in NAMES:
            return self.reply(404)
        with open(os.path.join(HERE, name), "wb") as f:
            f.write(body)
        print(f"wrote {name} ({len(body):,} bytes)", flush=True)
        self.reply(200)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    http.server.HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
