from fastapi import FastAPI, HTTPException
from typing import Optional
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
import nflreadpy as nfl
import pandas as pd


DB_PATH = "nfl.db"

app = FastAPI(title="NFL Last 5 Games API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_table_columns(table_name: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name})")
    cols = [row[1] for row in cur.fetchall()]
    conn.close()
    return cols


PLAYERS_COLS = get_table_columns("players")
WEEKLY_COLS = get_table_columns("weekly_stats")

TEAM_COL_PLAYERS = (
    "recent_team"
    if "recent_team" in PLAYERS_COLS
    else ("team" if "team" in PLAYERS_COLS else None)
)
TEAM_COL_WEEKLY = (
    "recent_team"
    if "recent_team" in WEEKLY_COLS
    else ("team" if "team" in WEEKLY_COLS else None)
)

# Load team metadata once at startup
try:
    teams_polars = nfl.load_teams()
    teams_df = teams_polars.to_pandas()
    print("Teams DataFrame columns:", teams_df.columns.tolist())
    print("First few rows of teams data:")
    print(teams_df.head())
    
    # Create dictionary mapping for team lookup
    _teams_dict = {}
    for _, row in teams_df.iterrows():
        team_abbr = row.get('team_abbr') or row.get('team')
        if team_abbr:
            _teams_dict[team_abbr] = row.to_dict()
    
    print(f"Loaded {len(_teams_dict)} teams")
    print("Sample team data:", _teams_dict.get('DET', 'DET not found'))

except Exception as e:
    print(f"Error loading team metadata from nflreadpy: {e}")
    _teams_dict = {}

# Load player metadata
try:
    players_polars = nfl.load_players()
    players_df = players_polars.to_pandas()

    if "gsis_id" in players_df.columns:
        _players_meta = players_df.set_index("gsis_id")
    elif "player_id" in players_df.columns:
        _players_meta = players_df.set_index("player_id")
    else:
        _players_meta = None

    if "headshot" in players_df.columns:
        HEADSHOT_COL = "headshot"
    elif "headshot_url" in players_df.columns:
        HEADSHOT_COL = "headshot_url"
    else:
        HEADSHOT_COL = None

except Exception as e:
    print(f"Error loading player metadata from nflreadpy: {e}")
    _players_meta = None
    HEADSHOT_COL = None


@app.get("/")
def root():
    return {"status": "ok", "message": "NFL API running"}


@app.get("/team/{team}")
def get_team(team: str):
    conn = get_db()
    cur = conn.cursor()

    SEASON = 2025

    if not TEAM_COL_WEEKLY:
        conn.close()
        raise HTTPException(
            status_code=500,
            detail="Team column not available in weekly_stats",
        )

    team_col = f"ws.{TEAM_COL_WEEKLY}"
    team = team.upper()

    # Get team metadata
    team_name = None
    team_colors = None
    team_logo = None

    if team in _teams_dict:
        meta = _teams_dict[team]
        
        # Try different possible column names for team name
        team_name = (
            meta.get("team_name") or 
            meta.get("team_nick") or
            meta.get("team_nickname") or
            meta.get("name") or 
            meta.get("full_name") or 
            meta.get("nickname")
        )
        
        # Try different possible column names for colors
        team_colors = {
            "primary": (
                meta.get("team_color") or 
                meta.get("color_primary") or
                meta.get("team_color_primary") or
                meta.get("primary_color")
            ),
            "secondary": (
                meta.get("team_color2") or 
                meta.get("color_secondary") or
                meta.get("team_color_secondary") or
                meta.get("secondary_color")
            ),
        }
        
        # Try different possible column names for logo
        team_logo = (
            meta.get("team_logo_espn") or
            meta.get("team_logo_wikipedia") or
            meta.get("team_logo") or
            meta.get("team_wordmark") or
            meta.get("logo_espn") or
            meta.get("logo")
        )
        
        print(f"Team {team} metadata: name={team_name}, colors={team_colors}, logo={team_logo}")

    base_stats = [
        "passing_yards",
        "rushing_yards",
        "receiving_yards",
        "passing_tds",
        "rushing_tds",
        "receiving_tds",
        "fantasy_points_ppr",
    ]
    stat_cols = [c for c in base_stats if c in WEEKLY_COLS]

    if not stat_cols:
        conn.close()
        raise HTTPException(
            status_code=500,
            detail="No stat columns available in weekly_stats",
        )

    team_select_parts = [f"SUM(ws.{c}) AS {c}" for c in stat_cols]
    team_select_clause = ",\n          ".join(team_select_parts)

    sql_team = f"""
        SELECT
            {team_select_clause}
        FROM weekly_stats AS ws
        LEFT JOIN players AS p
            ON ws.player_id = p.player_id
        WHERE ws.season = ?
            AND {team_col} = ?
    """

    cur.execute(sql_team, (SEASON, team))
    team_row = cur.fetchone()

    if not team_row or all(v is None for v in team_row):
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"No data found for team {team} in {SEASON}",
        )

    team_totals = {k: team_row[idx] for idx, k in enumerate(stat_cols)}

    pos_select_parts = ["p.position", "COUNT(DISTINCT ws.player_id) AS players"]
    pos_select_parts.extend([f"SUM(ws.{c}) AS {c}" for c in stat_cols])
    pos_select_clause = ",\n            ".join(pos_select_parts)

    sql_pos = f"""
        SELECT
            {pos_select_clause}
        FROM weekly_stats AS ws
        LEFT JOIN players AS p
            ON ws.player_id = p.player_id
        WHERE ws.season = ?
          AND {team_col} = ?
        GROUP BY p.position
        ORDER BY p.position
    """

    cur.execute(sql_pos, (SEASON, team))
    pos_rows = cur.fetchall()
    by_position = [dict(row) for row in pos_rows]

    plyr_select_parts = [
        "ws.player_id",
        "p.player_name AS player_name",
        "p.position",
    ]
    plyr_select_parts.extend([f"SUM(ws.{c}) AS {c}" for c in stat_cols])
    plyr_select_clause = ",\n            ".join(plyr_select_parts)

    sql_player = f"""
        SELECT
            {plyr_select_clause}
        FROM weekly_stats AS ws
        LEFT JOIN players AS p
            ON ws.player_id = p.player_id
        WHERE ws.season = ?
          AND {team_col} = ?
        GROUP BY ws.player_id, p.player_name, p.position
        ORDER BY fantasy_points_ppr DESC
    """

    cur.execute(sql_player, (SEASON, team))
    plyr_rows = cur.fetchall()
    by_player = [dict(r) for r in plyr_rows]

    conn.close()

    for d in [team_totals, *by_position, *by_player]:
        if "fantasy_points_ppr" in d and d["fantasy_points_ppr"] is not None:
            d["fantasy_points_ppr"] = round(d["fantasy_points_ppr"], 2)

    return {
        "team": team,
        "season": SEASON,
        "team_name": team_name,
        "team_colors": team_colors,
        "team_logo": team_logo,
        "team_totals": team_totals,
        "by_position": by_position,
        "by_player": by_player,
    }


# ... rest of your endpoints remain the same ...