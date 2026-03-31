# frontend/app.py

from flask import Flask, render_template
import sys
import os
from collections import Counter

# Allow frontend to access backend folder
sys.path.append(os.path.abspath("../backend"))

# Import backend pipeline
from main import run_pipeline

# Initialize Flask app
app = Flask(__name__)


@app.route("/")
def home():
    """
    This route:
    1. Calls backend pipeline
    2. Gets final disaster alerts
    3. Sends them to HTML page
    """

    alerts_df = run_pipeline()        # Run full AI pipeline
    alerts = alerts_df.to_dict("records")  # Convert to list of dicts
    
    summary = Counter(alert["disaster_type"] for alert in alerts)
    high_priority = sum(1 for alert in alerts if alert["severity"] == "HIGH")

    return render_template("index.html", alerts=alerts,summary=summary,
    high_priority=high_priority)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
