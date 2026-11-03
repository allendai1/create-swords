"""Is balance.json still what Studio runs? Paste the hashes Studio prints for
    require(game.ServerStorage.Builders.ExportBalance:Clone())(nil, "hashes")   (JSON-encode it in the Command Bar)
and run: python Development/sim/check_export.py '<that JSON>'. Lists every changed source; re-export if any."""
import json
import sys

import rules

studio = json.loads(sys.argv[1])
saved = rules.load().raw["sources"]
changed = sorted(k for k in set(studio) | set(saved) if studio.get(k) != saved.get(k))
print("export is current" if not changed else "re-export: changed since balance.json: " + ", ".join(changed))
sys.exit(1 if changed else 0)
