import requests
import pandas as pd
from config import DATA_SOURCES, NEWSAPI_KEY, NEWSDATA_KEY
from datetime import datetime



def fetch_alerts(source):
    """
    Generic function to fetch disaster alerts
    from different sources based on source type.
    """
    

    alerts = []

    # USGS Earthquake Feed
    if source["type"] == "usgs":
        data = requests.get(source["url"]).json()
        for eq in data["features"][:5]:
            timestamp = eq["properties"]["time"]
            date_time = datetime.utcfromtimestamp(timestamp / 1000)

            alerts.append({
            "source": source["name"],
            "title": f"Magnitude {eq['properties']['mag']} earthquake",
            "location": eq["properties"]["place"],
            "year": date_time.year,
            "date": date_time.strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": date_time
            })


    # NewsAPI
    elif source["type"] == "newsapi":
        params = {
            "q": "disaster flood earthquake cyclone",
            "apiKey": NEWSAPI_KEY
        }
        data = requests.get(source["url"], params=params).json()
        
        for article in data.get("articles", []):
            published = article.get("publishedAt", "")
            try:
                dt = datetime.fromisoformat(published.replace("Z", ""))
            except:
                dt = datetime.utcnow()
                
            alerts.append({
            "source": source["name"],
            "title": article.get("title", ""),
            "location": article.get("source", {}).get("name", ""),
            "year": article.get("publishedAt", "")[:4],
            "date": article.get("publishedAt", ""),
            "timestamp": dt
            })

           
    # NewsData.io
    elif source["type"] == "newsdata":
        params = {
            "apikey": NEWSDATA_KEY,
            "q": "disaster flood earthquake"
        }
        data = requests.get(source["url"], params=params).json()

        for article in data.get("results", []):
            if isinstance(article, dict):
                title = article.get("title", "")
                location = article.get("country", "")
            else:
                title = str(article)
                location = ""

        alerts.append({
            "source": source["name"],
            "title": title,
            "location": location
        })

    return alerts


def orchestrator_agent():
    """
    Orchestrates all data sources and combines alerts.
    """

    all_alerts = []

    for source in DATA_SOURCES:
        all_alerts.extend(fetch_alerts(source))

    return pd.DataFrame(all_alerts)
