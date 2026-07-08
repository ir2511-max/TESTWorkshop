# AI × Luxury Fashion — Weekly Digest

A self-updating weekly news digest on AI and luxury fashion, powered by the
Anthropic API (Claude + web search). Runs entirely on GitHub Actions — no
local server or cloning required — and publishes a live page via GitHub
Pages at `https://<username>.github.io/<reponame>`.

Each run:
1. Asks Claude to search the web for the 5 most important AI × luxury
   fashion stories from the past 7 days.
2. Writes a plain-text copy to `news.txt`.
3. Writes a styled page to `docs/index.html`.
4. Commits and pushes both files back to the repo.

## Setup

### 1. Add your Anthropic API key as a secret
1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**.
2. Click **New repository secret**.
3. Name: `ANTHROPIC_API_KEY`
4. Value: your API key from [console.anthropic.com](https://console.anthropic.com).
5. Save.

### 2. Enable GitHub Pages
1. Go to **Settings** → **Pages**.
2. Under **Build and deployment** → **Source**, choose **Deploy from a branch**.
3. Set **Branch** to `main` and folder to `/docs`.
4. Save. Your page will be live at `https://<username>.github.io/<reponame>`
   (may take a minute or two the first time).

### 3. Trigger the first run manually
1. Go to the **Actions** tab.
2. Select the **Weekly AI x Luxury Fashion Digest** workflow.
3. Click **Run workflow** → **Run workflow**.
4. Once it finishes, `news.txt` and `docs/index.html` will be updated and
   pushed automatically, and your Pages site will reflect the new digest
   shortly after.

## Schedule

The workflow also runs automatically every **Monday at 13:00 UTC**. Edit the
`cron` line in `.github/workflows/weekly.yml` to change the schedule.

## Files

```
.
├── main.py                     # Fetches stories via Claude + web search, writes outputs
├── requirements.txt             # Python dependency (anthropic SDK)
├── news.txt                     # Plain-text digest (auto-updated)
├── docs/
│   └── index.html               # Styled digest page served by GitHub Pages (auto-updated)
└── .github/workflows/weekly.yml # Scheduled + manual GitHub Actions workflow
```

## Notes

- The script uses `claude-sonnet-5` with the Anthropic web search tool. If
  you'd like to use a different model, edit the `MODEL` constant at the top
  of `main.py`.
- No local Python environment is required to operate this repo day-to-day —
  everything runs in GitHub Actions. You only need Python locally if you
  want to test `main.py` yourself (`pip install -r requirements.txt` and
  `export ANTHROPIC_API_KEY=...` first).
