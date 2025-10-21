import requests

API_KEY = "4b83a7eb707c4349a53ae9406372bc86"
BASE_URL = "https://newsapi.org/v2/everything"

def fetch_combined_news(
    keywords=None,
    from_date="2025-10-18",
    sort_by="publishedAt",  # 'relevancy' | 'popularity' | 'publishedAt'
    per_keyword=15,         # fetch a bit more per keyword, we'll trim later
    total_limit=10          # final combined cap
):
    """
    Fetch and combine articles for multiple keywords, remove duplicates,
    sort by publish time (desc), and return top `total_limit` items.
    """
    if keywords is None:
        keywords = ["Personal Finance", "Budgeting Tips"]

    combined = []
    seen_titles = set()

    for kw in keywords:
        params = {
            "q": kw,
            "from": from_date,
            "sortBy": sort_by,
            "language": "en",
            "apiKey": API_KEY,
            "pageSize": per_keyword,
            "page": 1,
        }

        resp = requests.get(BASE_URL, params=params, timeout=30)
        # If an error occurs, just skip this keyword silently to avoid extra prints
        if resp.status_code != 200:
            continue

        data = resp.json()
        articles = data.get("articles", [])

        for a in articles:
            title = a.get("title") or ""
            if not title or title in seen_titles:
                continue
            seen_titles.add(title)

            combined.append({
                "keyword": kw,
                "title": title,
                "source": (a.get("source") or {}).get("name"),
                "publishedAt": a.get("publishedAt"),
                "url": a.get("url"),
            })

    # Sort by publishedAt (desc) where possible; keep items without date at the end
    def sort_key(item):
        return item.get("publishedAt") or ""

    combined.sort(key=sort_key, reverse=True)

    return combined[:total_limit]


if __name__ == "__main__":
    topics = ["Personal Finance", "Budgeting Tips"]
    results = fetch_combined_news(
        keywords=topics,
        from_date="2025-10-18",
        sort_by="publishedAt",
        per_keyword=15,
        total_limit=10
    )

    print("Top 10 combined articles on Personal Finance, Budgeting Tips:\n")
    for i, article in enumerate(results, start=1):
        print(f"{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   Published: {article['publishedAt']}")
        print(f"   URL: {article['url']}\n")
