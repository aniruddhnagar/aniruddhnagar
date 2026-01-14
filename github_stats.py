import os
import requests
from collections import Counter
import matplotlib.pyplot as plt

# ----------------------------
# CONFIG
# ----------------------------
GITHUB_USERNAME = "aniruddhnagar"  # <-- your GitHub username
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # GitHub Actions token

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)  # Ensure folder exists

# ----------------------------
# FETCH REPOS
# ----------------------------
repos_url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100"
response = requests.get(repos_url, headers=HEADERS)
repos = response.json()

if isinstance(repos, dict) and repos.get("message"):
    print("Error fetching repos:", repos["message"])
    exit(1)

print(f"Fetched {len(repos)} repos.")

# ----------------------------
# COMPUTE LANGUAGE STATS
# ----------------------------
languages = []
for repo in repos:
    lang = repo["language"]
    if lang:
        languages.append(lang)

lang_counter = Counter(languages)
print("Language usage:", lang_counter)

# ----------------------------
# PLOT PIE CHART
# ----------------------------
plt.figure(figsize=(6,6))
plt.pie(lang_counter.values(), labels=lang_counter.keys(), autopct="%1.1f%%", startangle=140)
plt.title("GitHub Language Usage")
plt.savefig(os.path.join(ASSETS_DIR, "github_language_pie.png"))
plt.close()

# ----------------------------
# PLOT BAR CHARTS: Stars & Forks
# ----------------------------
repo_names = [repo["name"] for repo in repos]
repo_stars = [repo["stargazers_count"] for repo in repos]
repo_forks = [repo["forks_count"] for repo in repos]

# Stars bar chart
plt.figure(figsize=(8,6))
plt.barh(repo_names, repo_stars, color="skyblue")
plt.xlabel("Stars")
plt.title("GitHub Stars per Repo")
plt.tight_layout()
plt.savefig(os.path.join(ASSETS_DIR, "github_stars_bar.png"))
plt.close()

# Forks bar chart
plt.figure(figsize=(8,6))
plt.barh(repo_names, repo_forks, color="orange")
plt.xlabel("Forks")
plt.title("GitHub Forks per Repo")
plt.tight_layout()
plt.savefig(os.path.join(ASSETS_DIR, "github_forks_bar.png"))
plt.close()

# ----------------------------
# SUMMARY
# ----------------------------
summary_md = f"""
# GitHub Stats Summary

**Total Repositories:** {len(repos)}  
**Languages Used:** {', '.join(lang_counter.keys())}  
**Top Language:** {lang_counter.most_common(1)[0][0] if lang_counter else 'N/A'}
"""

with open(os.path.join(ASSETS_DIR, "github_summary.md"), "w") as f:
    f.write(summary_md)

print("Charts and summary generated successfully in 'assets/' folder.")
