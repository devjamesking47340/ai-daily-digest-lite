import feedparser
import json
import datetime
from typing import List, Dict

# Lightweight demo: fetch RSS items and select top ones by keyword priority
# In real usage, replace 'fake_llm_score' with any LLM API call.

def fetch_rss_items(url: str, limit: int = 20) -> List[Dict]:
    """Fetch RSS feed and return limited items with basic fields."""
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries[:limit]:
        items.append({
            'title': entry.get('title', ''),
            'link': entry.get('link', ''),
            'summary': entry.get('summary', '')[:100]
        })
    return items

def fake_llm_score(title: str, keywords: List[str]) -> float:
    """Compute a simple heuristic score (replace with LLM call later)."""
    title_lower = title.lower()
    score = 0.0
    for kw in keywords:
        if kw.lower() in title_lower:
            score += 1.0
    # add random noise to simulate model variance
    import random
    return score + random.uniform(0, 0.5)

def select_top_items(items: List[Dict], top_n: int = 5) -> List[Dict]:
    """Score items and return top N by score."""
    keywords = ['ai', 'model', 'openai', 'llm']
    scored = []
    for item in items:
        item['score'] = fake_llm_score(item['title'], keywords)
        scored.append(item)
    scored.sort(key=lambda x: x['score'], reverse=True)
    return scored[:top_n]

def write_daily_digest(top_items: List[Dict], outfile: str = 'digest.md'):
    """Write a simple markdown digest."""
    date_str = datetime.date.today().isoformat()
    lines = [f'# Daily AI Digest - {date_str}', '']
    for i, item in enumerate(top_items, 1):
        lines.append(f"{i}. **{item['title']}** (Score: {item['score']:.2f})")
        lines.append(f"   {item['link']}")
        lines.append(f"   {item['summary']}")
    with open(outfile, 'w') as f:
        f.write('\n'.join(lines))
    print(f'Digest written to {outfile}')

def main():
    rss_url = 'https://www.reddit.com/r/MachineLearning/.rss'  # example feed
    items = fetch_rss_items(rss_url)
    if not items:
        print('No items fetched. Check network/feed.')
        return
    top = select_top_items(items, top_n=5)
    write_daily_digest(top)

if __name__ == '__main__':
    main()
