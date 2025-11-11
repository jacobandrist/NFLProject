from fastapi import FastAPI, HTTPException
from typing import Optional
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
import nflreadpy as nfl


DB_PATH = "nfl.db"

app = FastAPI(title="NFL Last 5 Games API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000",
                   "http://localhost:5173", "http://127.0.0.1:5173"],
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
        raise HTTPException(status_code=500, detail="Team column not availabe in weekly stats")
    
    team_col = f"ws.{TEAM_COL_WEEKLY}"
    team = team.upper()

    base_stats= [
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
        raise HTTPException(status_code=500, detail="No stat columns available in weekly_stats")
    
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
        raise HTTPException(status_code=404, detail="No data found for team {team} in {SEASON}")
    
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
    by_position = []
    for row in pos_rows:
        d = dict(row)
        by_position.append(d)

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
        "team_totals": team_totals,
        "by_position": by_position,
        "by_player": by_player,
    }

@app.get("/leaders")
def get_leaders(limit: int = 10, position: Optional[str] = None):

    conn = get_db()
    cur = conn.cursor()

    SEASON = 2025 

    if TEAM_COL_WEEKLY:
        team_expr = f"ws.{TEAM_COL_WEEKLY}"
    else:
        team_expr = "NULL"

    sql = f"""
        SELECT
            ws.player_id,
            p.player_name AS player_name,
            {team_expr} AS team,
            p.position,
            COUNT(*) AS games_played,
            SUM(ws.fantasy_points_ppr) AS total_fantasy_points_ppr,
            AVG(ws.fantasy_points_ppr) AS avg_fantasy_points_ppr
        FROM weekly_stats AS ws
        LEFT JOIN players AS p
            ON ws.player_id = p.player_id
        WHERE ws.season = ?
    """

    params = [SEASON]

    if position:
        sql += " AND p.position = ?"
        params.append(position.upper())

    sql += f"""
        GROUP BY
            ws.player_id,
            p.player_name,
            {team_expr},
            p.position
        ORDER BY total_fantasy_points_ppr DESC
        LIMIT ?
    """
    params.append(limit)

    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()

    result = [dict(r) for r in rows]
    for r in result:
        for key in ("total_fantasy_points_ppr", "avg_fantasy_points_ppr"):
            if key in r and r[key] is not None:
                r[key] = round(r[key], 2)

    return result

@app.get("/players")
def search_players(
    q: Optional[str] = None,
    team: Optional[str] = None,
    position: Optional[str] = None,
    limit: int = 50,
):
    """
    Search players by name/team/position.

    - q: substring match on player_name
    - team: team abbreviation (KC, DET, etc.) if team column exists
    - position: QB/RB/WR/TE, etc.
    """
    conn = get_db()
    cur = conn.cursor()

    # Build base SELECT, aliasing team column (if any) as 'team'
    if TEAM_COL_PLAYERS:
        select_team = f"{TEAM_COL_PLAYERS} AS team"
    else:
        select_team = "NULL AS team"

    sql = f"""
        SELECT
            player_id,
            player_name,
            {select_team},
            position
        FROM players
        WHERE 1=1
    """
    params = []

    if q:
        sql += " AND player_name LIKE ?"
        params.append(f"%{q}%")

    if position:
        if "position" in PLAYERS_COLS:
            sql += " AND position = ?"
            params.append(position.upper())

    if team and TEAM_COL_PLAYERS:
        sql += f" AND {TEAM_COL_PLAYERS} = ?"
        params.append(team.upper())

    sql += " ORDER BY player_name LIMIT ?"
    params.append(limit)

    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()

    return [dict(r) for r in rows]

@app.get("/players/{player_id}")
def get_player(player_id: str):
    """
    Get basic info on a single player.
    """
    conn = get_db()
    cur = conn.cursor()

    if TEAM_COL_PLAYERS:
        select_team = f"{TEAM_COL_PLAYERS} AS team"
    else:
        select_team = "NULL AS team"

    sql = f"""
        SELECT
            player_id,
            player_name,
            {select_team},
            position
        FROM players
        WHERE player_id = ?
    """

    cur.execute(sql, (player_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Player not found")

    return dict(row)

@app.get("/players/{player_id}/games")
def get_last_games(player_id: str, limit: int = 5):
    """
    Get last `limit` games (weekly stats) for a player.
    """
    conn = get_db()
    cur = conn.cursor()

    if TEAM_COL_WEEKLY:
        select_team = f"{TEAM_COL_WEEKLY} AS team"
    else:
        select_team = "NULL AS team"

    # Only use stat columns if they exist
    stat_cols = []
    if "passing_yards" in WEEKLY_COLS:
        stat_cols.append("passing_yards")
    if "rushing_yards" in WEEKLY_COLS:
        stat_cols.append("rushing_yards")
    if "receiving_yards" in WEEKLY_COLS:
        stat_cols.append("receiving_yards")
    if "passing_tds" in WEEKLY_COLS:
        stat_cols.append("passing_tds")
    if "rushing_tds" in WEEKLY_COLS:
        stat_cols.append("rushing_tds")
    if "receiving_tds" in WEEKLY_COLS:
        stat_cols.append("receiving_tds")
    if "fantasy_points_ppr" in WEEKLY_COLS:
        stat_cols.append("fantasy_points_ppr")

    # Build SELECT list dynamically
    select_parts = [
        "season" if "season" in WEEKLY_COLS else "NULL AS season",
        "week" if "week" in WEEKLY_COLS else "NULL AS week",
        select_team,
    ]
    select_parts.extend(stat_cols)

    select_clause = ", ".join(select_parts)

    sql = f"""
        SELECT
            {select_clause}
        FROM weekly_stats
        WHERE player_id = ?
        ORDER BY season DESC, week DESC
        LIMIT ?
    """

    cur.execute(sql, (player_id, limit))
    rows = cur.fetchall()
    conn.close()

    return [dict(r) for r in rows]
