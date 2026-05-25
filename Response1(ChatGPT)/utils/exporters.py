import json
from pathlib import Path
from datetime import datetime

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)

def export_json(filename, data):

    filepath = EXPORT_DIR / filename

    with open(filepath, "a") as f:

        json.dump(data, f)
        f.write("\n")

def export_alert(alert):

    timestamp = datetime.utcnow().strftime("%Y%m%d")

    filename = f"alerts_{timestamp}.json"

    export_json(filename, alert)