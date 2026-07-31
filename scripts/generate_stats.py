import frontmatter, os, json
from datetime import datetime

content_dir = "content"

stats = {
    "total_posts": 0,
    "tags": {},
    "years": {},
    "word_count": 0,
}

for root, _, files in os.walk(content_dir):
    for f in files:
        if f.endswith(".md"):
            post = frontmatter.load(os.path.join(root, f))
            stats["total_posts"] += 1
            date = post.get("date")
            tags = post.get("tags", [])
            body = post.content or ""
            stats["word_count"] += len(body.split())

            if date:
                year = datetime.fromisoformat(str(date)).year
                stats["years"][year] = stats["years"].get(year, 0) + 1

            for tag in tags:
                stats["tags"][tag] = stats["tags"].get(tag, 0) + 1

os.makedirs("data", exist_ok=True)
with open("data/content_stats.json", "w") as f:
    json.dump(stats, f, indent=2)
