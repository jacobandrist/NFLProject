import nflreadpy as nfl
import pandas as pd
import sqlite3
import ssl
import urllib.request
import certifi

ctx = ssl.create_default_context(cafile=certifi.where())
urllib.request.install_opener(
    urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
)

DB_PATH = "nfl.db"

# Always use the current NFL season
CURRENT_SEASON = nfl.get_current_season()
YEARS = [CURRENT_SEASON]



def load_rosters(conn):
    print("Loading rosters...")

    rosters = nfl.load_rosters(seasons=YEARS).to_pandas()

    id_col = None
    for col in ["player_id", "gsis_id"]:
        if col in rosters.columns:
            id_col = col
            break

    if id_col is None:
        raise RuntimeError(
            f"No suitable ID column found in rosters. Columns: {list(rosters.columns)}"
        )

    rosters["player_id"] = rosters[id_col]

    name_col = None
    for col in ["player_name", "full_name", "display_name"]:
        if col in rosters.columns:
            name_col = col
            break

    if name_col:
        rosters["player_name"] = rosters[name_col]
    else:
        rosters["player_name"] = rosters["player_id"]

    team_source_col = None
    for col in ["recent_team", "team"]:
        if col in rosters.columns:
            team_source_col = col
            break

    if team_source_col:
        rosters["recent_team"] = rosters[team_source_col]

    keep_cols = ["player_id", "player_name", "position"]
    for col in ["recent_team", "team"]:
        if col in rosters.columns:
            keep_cols.append(col)

    keep_cols = [c for c in keep_cols if c in rosters.columns]

    rosters = rosters[keep_cols].drop_duplicates(subset=["player_id"])

    rosters.to_sql("players", conn, if_exists="replace", index=False)
    print(f"Inserted {len(rosters)} players")


def load_weekly_stats(conn):
    print("Loading weekly stats...")

    weekly = nfl.load_player_stats(
        seasons=YEARS,
        summary_level="week",
    ).to_pandas()

    keep_cols = [
        "player_id",
        "player_name",
        "recent_team", 
        "team",
        "season",
        "week",
        "passing_yards",
        "rushing_yards",
        "receiving_yards",
        "passing_tds",
        "rushing_tds",
        "receiving_tds",
        "fantasy_points_ppr",
    ]
    keep_cols = [c for c in keep_cols if c in weekly.columns]

    weekly = weekly[keep_cols]

    weekly.to_sql("weekly_stats", conn, if_exists="replace", index=False)
    print(f"Inserted {len(weekly)} weekly stat rows")


def create_indexes(conn):
    print("Creating indexes...")
    cur = conn.cursor()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_players_id ON players(player_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_players_name ON players(player_name);")
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_weekly_player ON weekly_stats(player_id);"
    )
    conn.commit()
    print("Indexes created.")


def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        load_rosters(conn)
        load_weekly_stats(conn)
        create_indexes(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
