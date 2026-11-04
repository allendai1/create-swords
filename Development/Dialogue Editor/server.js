// Dialogue Editor: serves index.html on 127.0.0.1:8767.
// studio.json = what is in the game (POSTed by an export from Studio); edits.json = Allen's edits (POSTed by the page).
// No dependencies: node server.js
const http = require("http");
const fs = require("fs");
const path = require("path");

const DIR = __dirname;
const PORT = 8767;
const WRITABLE = { "/studio": "studio.json", "/edits": "edits.json" };
const TYPES = { ".html": "text/html; charset=utf-8", ".json": "application/json; charset=utf-8", ".js": "text/javascript" };

http.createServer((req, res) => {
	res.setHeader("Access-Control-Allow-Origin", "*");
	if (req.method === "OPTIONS") return res.end();
	const url = req.url.split("?")[0];
	if (req.method === "POST" && WRITABLE[url]) {
		let body = "";
		req.on("data", (c) => (body += c));
		req.on("end", () => {
			try {
				JSON.parse(body); // never write a broken file
			} catch (e) {
				res.statusCode = 400;
				return res.end("bad json: " + e.message);
			}
			fs.writeFileSync(path.join(DIR, WRITABLE[url]), body.endsWith("\n") ? body : body + "\n");
			res.end("ok");
		});
		return;
	}
	if (req.method === "DELETE" && url === "/edits") {
		fs.rmSync(path.join(DIR, "edits.json"), { force: true });
		return res.end("ok");
	}
	const file = path.join(DIR, url === "/" ? "index.html" : path.normalize(url).replace(/^[\\/]+/, ""));
	if (!file.startsWith(DIR) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
		res.statusCode = 404;
		return res.end("not found");
	}
	res.setHeader("Content-Type", TYPES[path.extname(file)] || "application/octet-stream");
	res.setHeader("Cache-Control", "no-store");
	fs.createReadStream(file).pipe(res);
}).listen(PORT, "127.0.0.1", () => console.log(`Dialogue Editor on http://127.0.0.1:${PORT}`));
