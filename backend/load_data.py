import nfl_data_py as nfl
import pandas as pd
import sqlite3

DB_PATH = "nfl.db"
YEARS = [2022, 2023, 2024]

def load_rosters(conn):
    print("Loading rosters...")
    rosters = nfl.import_seasonal_rosters(YEARS)

    if "recent_team" in rosters.columns:
        team_col = "recent_team"
    elif "team" in rosters.columns:
        team_col = "team"
    else:
        team_col = None

    keep_cols = ["player_id", "player_name", "position"]
    if team_col:
        keep_cols.append(team_col)

    keep_cols = [c for c in keep_cols if c in rosters.columns]
    rosters = rosters[keep_cols].drop_duplicates(subset=["player_id"])

    rosters.to_sql("players", conn, if_exists="replace", index=False)
    print(f"Inserted {len(rosters)} players")



def load_weekly_stats(conn):
    print("Loading weekly stats...")
    weekly = nfl.import_weekly_data(YEARS, downcast=True)

    keep_cols = [c for c in [
        "player_id", "player_name", "recent_team", "season", "week",
        "passing_yards", "rushing_yards", "receiving_yards",
        "passing_tds", "rushing_tds", "receiving_tds", "fantasy_points_ppr"
    ] if c in weekly.columns]

    weekly = weekly[keep_cols]

    # Save to database
    weekly.to_sql("weekly_stats", conn, if_exists="replace", index=False)
    print(f"Inserted {len(weekly)} weekly stat rows")


def create_indexes(conn):
    print("Creating indexes...")
    cur = conn.cursor()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_players_id ON players(player_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_players_name ON players(player_name);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_weekly_player ON weekly_stats(player_id);")
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
