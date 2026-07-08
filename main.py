"""
AI x Luxury Fashion Weekly News Digest
Uses the Anthropic API (with the web search tool) to find the 5 most
important news stories from the past 7 days about AI and luxury fashion,
then writes the results to news.txt and docs/index.html.
"""

import json
import os
import re
from datetime import datetime, timezone

import anthropic

MODEL = "claude-sonnet-5"
MAX_TOKENS = 4096

PROMPT = """Search the web for news from the past 7 days about the \
intersection of AI (artificial intelligence) and luxury fashion \
(e.g. LVMH, Kering, Chanel, luxury retail, luxury brands using AI tools, \
generative AI in fashion design/marketing/personalization, etc).

Find the 5 most important stories. Then respond with ONLY a JSON array \
(no markdown fences, no preamble, no commentary) of exactly 5 objects, \
each with these keys:
- "headline": string
- "summary": string (exactly 2 sentences)
- "source": string (publication name)
- "url": string (direct article URL)

Order the array from most to least important."""


def get_stories() -> list[dict]:
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": PROMPT}],
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 8}],
    )

    text = "".join(
        block.text for block in response.content if block.type == "text"
    )

    match = re.search(r"\[.*\]", text, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find JSON array in model response:\n{text}")

    return json.loads(match.group(0))


def write_txt(stories: list[dict], generated_at: str) -> None:
    lines = [f"AI x Luxury Fashion — Weekly Digest ({generated_at})", "=" * 60, ""]
    for i, story in enumerate(stories, 1):
        lines += [
            f"{i}. {story['headline']}",
            f"   {story['summary']}",
            f"   Source: {story['source']}",
            f"   URL: {story['url']}",
            "",
        ]
    with open("news.txt", "w") as f:
        f.write("\n".join(lines))


def write_html(stories: list[dict], generated_at: str) -> None:
    cards = "\n".join(
        f"""      <article class="card">
        <span class="rank">{i}</span>
        <h2>{story['headline']}</h2>
        <p>{story['summary']}</p>
        <div class="meta">
          <span class="source">{story['source']}</span>
          <a href="{story['url']}" target="_blank" rel="noopener">Read article &rarr;</a>
        </div>
      </article>"""
        for i, story in enumerate(stories, 1)
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI x Luxury Fashion — Weekly Digest</title>
<style>
  :root {{
    --bg: #0e0e10;
    --card: #18181b;
    --text: #f2f2f0;
    --muted: #a1a1aa;
    --accent: #d4af37;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 60px 20px;
    background: var(--bg);
    color: var(--text);
    font-family: 'Georgia', 'Times New Roman', serif;
  }}
  .wrap {{ max-width: 720px; margin: 0 auto; }}
  header {{ text-align: center; margin-bottom: 48px; }}
  header h1 {{
    font-size: 2.1rem;
    letter-spacing: 0.03em;
    margin: 0 0 8px;
  }}
  header p {{ color: var(--muted); font-family: sans-serif; font-size: 0.9rem; }}
  .card {{
    background: var(--card);
    border: 1px solid #27272a;
    border-radius: 10px;
    padding: 28px 32px;
    margin-bottom: 24px;
    position: relative;
  }}
  .rank {{
    position: absolute;
    top: -14px;
    left: -14px;
    background: var(--accent);
    color: #111;
    font-family: sans-serif;
    font-weight: 700;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
  }}
  .card h2 {{ font-size: 1.25rem; margin: 4px 0 12px; line-height: 1.35; }}
  .card p {{ color: #d4d4d8; line-height: 1.6; margin: 0 0 16px; }}
  .meta {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: sans-serif;
    font-size: 0.85rem;
  }}
  .source {{ color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  footer {{ text-align: center; color: var(--muted); font-family: sans-serif; font-size: 0.8rem; margin-top: 40px; }}
</style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>AI &times; Luxury Fashion</h1>
      <p>Weekly Digest &middot; Updated {generated_at}</p>
    </header>
{cards}
    <footer>Generated automatically every week via Claude + GitHub Actions.</footer>
  </div>
</body>
</html>
"""
    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w") as f:
        f.write(html)


def main() -> None:
    generated_at = datetime.now(timezone.utc).strftime("%B %d, %Y")
    stories = get_stories()
    write_txt(stories, generated_at)
    write_html(stories, generated_at)
    print(f"Wrote news.txt and docs/index.html with {len(stories)} stories.")


if __name__ == "__main__":
    main()
