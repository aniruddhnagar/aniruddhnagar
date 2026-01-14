import os
import requests
import matplotlib.pyplot as plt
from collections import Counter

USERNAME = "aniruddhnagar"
TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {"Authorization": f"token {TOKEN}"}
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# ----------------------------
# Fetch repositories
# ----------------------------
repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
repos = requests.get(repos_url, headers=HEADERS).json()

# ----------------------------
# Language Stats
# ----------------------------
language_counter = Counter()

for repo in repos:
    if repo["fork"]:
        continue
    lang_url = repo["languages_url"]
    langs = requests.get(lang_url, headers=HEADERS).json()
    for lang, bytes_count in langs.items():
        language_counter[lang] += bytes_count

# Plot Language Pie
plt.figure(figsize=(6, 6))
plt.pie(
    language_counter.values(),
    labels=language_counter.keys(),
    autopct="%1.1f%%",
    startangle=140,
    textprops={"fontsize": 10},
)
plt.title("Language Usage", fontsize=14)
plt.tight_layout()
plt.savefig(f"{ASSETS_DIR}/language_usage.png", dpi=150)
plt.close()

# ----------------------------
# Commit Stats
# ----------------------------
commit_counts = Counter()

for repo in repos:
    if repo["fork"]:
        continue

    commits_url = f"https://api.github.com/repos/{USERNAME}/{repo['name']}/commits?per_page=100"
    commits = requests.get(commits_url, headers=HEADERS).json()

    if isinstance(commits, list):
        commit_counts[repo["name"]] += len(commits)

# Take top 8 repos by commits
top_repos = commit_counts.most_common(8)

if top_repos:
    repos_names, commits_numbers = zip(*top_repos)

    plt.figure(figsize=(8, 4))
    plt.bar(repos_names, commits_numbers)
    plt.xticks(rotation=30, ha="right", fontsize=9)
    plt.ylabel("Commits")
    plt.title("Top Repositories by Commit Count", fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{ASSETS_DIR}/commit_stats.png", dpi=150)
    plt.close()

# ----------------------------
# Summary Markdown (optional)
# ----------------------------
with open(f"{ASSETS_DIR}/summary.md", "w") as f:
    f.write("## GitHub Stats (Auto-generated)\n\n")
    f.write("### Language Usage\n")
    for lang, count in language_counter.most_common():
        f.write(f"- {lang}\n")
