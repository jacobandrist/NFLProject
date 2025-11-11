from fastapi import FastAPI, HTTPException
from typing import Optional
import sqlite3

DB_PATH = "nfl.db"

app = FastAPI(title="NFL Last 5 Games API", version="0.1.0")


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


# Detect actual team column names once at startup
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
