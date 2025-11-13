# 🏈 NFL Stats API

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.121.1-brightgreen)
![nflreadpy](https://img.shields.io/badge/nflreadpy-Live%20NFL%20Data-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

A modern REST API for exploring NFL player and game statistics — powered by [**nflreadpy**](https://pypi.org/project/nflreadpy/), the official Python package for fetching live data from the **nflverse** ecosystem.

Built with:
- ⚡ **FastAPI** — high-performance async web framework  
- 🧠 **nflreadpy** — fast data access from nflverse repositories  
- 🗄 **SQLite** — simple and lightweight local data store  
- 📊 **Pandas + Polars** — efficient data transformations  

---

## 📂 Project Overview

backend/
├── load_data.py # Loads NFL data into the local SQLite database
├── main.py # FastAPI app exposing player/game endpoints
├── db.py # Database connection helper
├── requirements.txt # Dependencies
└── nfl.db # Generated SQLite database (auto-created)

---

## 🧠 About `nflreadpy`

[`nflreadpy`](https://pypi.org/project/nflreadpy/) is a Python package for downloading structured NFL data directly from the **nflverse** repositories.  
It offers:
- Fast data loading via [Polars](https://www.pola.rs/)
- Automatic caching (memory or filesystem)
- Consistent API with the R package [`nflreadr`](https://nflreadr.nflverse.com)
- Access to player, team, roster, and fantasy data

Example usage:

```python
import nflreadpy as nfl

# Load play-by-play data
pbp = nfl.load_pbp()

# Load player stats for the current and previous season
player_stats = nfl.load_player_stats([2024, 2025])

# Convert to pandas for easier manipulation
df = player_stats.to_pandas()
```
⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/yourusername/nfl-stats-api.git
cd nfl-stats-api/backend
2️⃣ Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
🧩 Key dependencies:
fastapi
uvicorn
nflreadpy
pandas
pyarrow
🏗 Load the Data
Before running the API, load the latest NFL data into the local database:
python load_data.py
This script:
Pulls current-season rosters and weekly player stats via nflreadpy
Normalizes data for use with the API
Saves everything into nfl.db
🚀 Run the Server
Start your local FastAPI instance:
uvicorn main:app --reload
Then open:
Interactive API Docs → http://127.0.0.1:8000/docs
Health Check → http://127.0.0.1:8000
🔗 API Endpoints
GET /
Health check.
Response:
{ "status": "ok", "message": "NFL API running" }
GET /players
Search players by name, team, or position.
Query Param	Type	Description
q	string	Substring match on player name
team	string	Team abbreviation (e.g. DET, KC)
position	string	Player position (QB, RB, WR, TE, etc.)
limit	int	Max number of results (default: 50)
Example:
GET /players?q=goff
GET /players/{player_id}
Get information for a single player.
Example:

GET /players/00-0033873
GET /players/{player_id}/games
Return recent weekly game stats (defaults to current season).
Query Param	Type	Description
limit	int	Number of games (default: 5)
season	int	Optional season year
Example:
GET /players/00-0033873/games?limit=5
Response:
[
  {
    "season": 2025,
    "week": 8,
    "team": "DET",
    "passing_yards": 312,
    "rushing_yards": 10,
    "passing_tds": 2,
    "fantasy_points_ppr": 21.4
  }
]
GET /players/{player_id}/games/summary
Aggregated stats (totals and averages) across the last N games.
Example:

GET /players/00-0033873/games/summary?limit=5
Response:
{
  "player_id": "00-0033873",
  "limit": 5,
  "games_played": 5,
  "stats": {
    "avg_passing_yards": 325.6,
    "total_passing_yards": 1628,
    "avg_passing_tds": 2.4,
    "total_passing_tds": 12,
    "avg_fantasy_points_ppr": 22.5
  }
}
🔁 Updating Data
To refresh data for the newest games:
python load_data.py
You can automate this with a cron job, GitHub Actions workflow, or a scheduled task.
🧩 Configuration Notes
The data loader (load_data.py) uses:
from nflreadpy.config import update_config

update_config(
    cache_mode="filesystem",
    cache_dir="~/nfl_cache",
    cache_duration=86400,  # 1 day
    verbose=True,
)
This enables local caching so repeated runs don’t re-download the same data.
📅 Current Season Only
The script automatically detects the current NFL season:
CURRENT_SEASON = nfl.get_current_season()
YEARS = [CURRENT_SEASON]
You can change this if you want to include multiple seasons.
🧰 Requirements
See requirements.txt, or install manually:
pip install fastapi uvicorn nflreadpy pandas pyarrow
🪪 License
This project is licensed under the MIT License.
Data sourced via nflverse and nflreadpy, which are licensed under CC-BY 4.0 and MIT respectively.
🙌 Credits
nflverse team — for maintaining open NFL data sources
nflreadpy maintainers — for the Python port
Built by Jacob Andrist and Grant Messer
