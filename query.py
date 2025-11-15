import requests
import time
import csv

API_KEY = "INSERT_API_KEY_HERE" 
url = "https://newsapi.org/v2/everything"

query = "Mark Carney"
language = "en"
page_size = 100 # daily rate with free plan
target_articles = 500

all_articles = {}
page = 1

while len(all_articles) < target_articles:
    params = {
        "q": query,
        "language": language,
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "page": page
    }
    
    response = requests.get(url, params=params, headers={"X-Api-Key": API_KEY})
    data = response.json()
    
    if data.get("status") != "ok":
        print("Error:", data.get("code"), " ", data.get("message"))
        break
    
    articles = data.get("articles", [])
    if not articles:
        print("No more articles found.")
        break
    
    for article in articles:
        if article["url"] not in all_articles:
            all_articles[article["url"]] = article

        if len(all_articles) >= target_articles:
            break
    
    page += 1
    time.sleep(1)

csv_file = "articles.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["publishedAt", "title", "description", "url", "source_name"])
    for article in all_articles.values():
        writer.writerow([
            article.get("publishedAt"),
            article.get("title"),
            article.get("description"),
            article.get("url"),
            article.get("source", {}).get("name")
        ])