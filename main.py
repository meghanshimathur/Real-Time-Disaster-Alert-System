# backend/main.py

import pandas as pd
from data_collab import orchestrator_agent
from classification import classify_alert
from alerts_priority import calculate_severity, priority_score
from advisory import advisory_agent
from datetime import datetime, timedelta

from email_notification import send_summary_email



def time_ago(event_time):
    # Handle missing or invalid timestamps
    if event_time is None or pd.isna(event_time):
        return "Time unknown"

    try:
        diff = datetime.utcnow() - event_time
        minutes = int(diff.total_seconds() / 60)

        if minutes < 60:
            return f"{minutes} minutes ago"
        elif minutes < 1440:
            return f"{minutes // 60} hours ago"
        else:
            return f"{minutes // 1440} days ago"

    except Exception:
        return "Time unknown"



def confidence_score(source):
    if "," in source:
        return "HIGH"
    return "MEDIUM"

def run_pipeline():
    # Phase 1
    alerts_df = orchestrator_agent()

    results = []
    email_alerts = []

    for _, row in alerts_df.iterrows():
        # Phase 2
        classification = classify_alert(row["title"])

        if classification["disaster_type"] == "not a disaster":
            continue

        # Phase 3
        severity = calculate_severity(
            classification["disaster_type"],
            row["title"]
        )

        # Phase 4
        advice = advisory_agent(
            classification["disaster_type"],
            severity,
            row["location"]
        )

        results.append({
            "source": row["source"],
            "title": row["title"],
            "location": row["location"],
            "year": row.get("year", "N/A"),
            "date": row.get("date", "N/A"),
            "time_ago": time_ago(row["timestamp"]),
            "confidence": confidence_score(row["source"]),
            "disaster_type": classification["disaster_type"],
            "severity": severity,
            "priority": priority_score(severity),
            "advice": advice
        })
        
        email_alerts.append({
            "timestamp": row["timestamp"],
            "location": row["location"],
            "disaster_type": classification["disaster_type"],
            "priority": priority_score(severity),
            "advice": advice
        })
    # ---------------------------------------
# 📧 Send ONLY TOP 5 latest alerts
# ---------------------------------------

# Sort alerts by latest timestamp
    email_alerts = sorted(
    email_alerts,
    key=lambda x: x["timestamp"],
    reverse=True
)

# Take top 5
    top_5_alerts = email_alerts[:5]

    if top_5_alerts:
        send_summary_email(top_5_alerts)
        print("✅ Top 5 alerts email sent")
    else:
        print("ℹ️ No alerts available for email")


    '''if email_alerts:
        send_summary_email(email_alerts)'''

    return pd.DataFrame(results)


if __name__ == "__main__":
    final_output = run_pipeline()
    print(final_output.head())
   


