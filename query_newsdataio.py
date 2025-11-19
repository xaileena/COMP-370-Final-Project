import requests
import csv

API_KEY = "API_KEY"
URL = "https://newsdata.io/api/1/news"
QUERY = "Mark Carney"
COUNTRIES = "us,ca"
LANGUAGE = "en"

params = {
    "apikey": API_KEY,
    "q": QUERY,
    "country": COUNTRIES,
    "language": LANGUAGE,
    "page": 0
}

all_articles = {}
page = 1

while True:
    params["page"] = page
    response = requests.get(URL, params=params)
    data = response.json()
    articles = data.get("results", [])
    if not articles:
        break

    for article in articles:
        if not isinstance(article, dict):
            continue  # skip if not a dictionary
        url = article.get("link")
        if url and url not in all_articles:
            all_articles[url] = {
                "publishedAt": article.get("pubDate"),
                "title": article.get("title"),
                "description": article.get("description"),
                "url": url,
                "source_name": article.get("source_id")
            }
    page += 1
    if not data.get("nextPage"):
        break

csv_file = "articles_newsdataio.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["publishedAt", "title", "description", "url", "source_name"])
    for article in all_articles.values():
        writer.writerow([
            article["publishedAt"],
            article["title"],
            article["description"],
            article["url"],
            article["source_name"]
        ])