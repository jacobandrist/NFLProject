import nfl_data_py as nfl
import pandas as pd
import sqlite3

DB_PATH = "nfl.db"

YEARS = [2022,2023,2024]

def load_rosters(conn):
    roster_cols = ["players_id", "player_name", "recent_team", "position"]
    print("Loading rosters...")
    rosters = nfl.import_seasonal_rosters(YEARS, columns=roster_cols)

    rosters = rosters.drop_duplicates(subset=["player_id"])

    rosters.to_sql("players", conn, if_exists="replace", index= False)
    print(f"Inserted {len(rosters)} players")

def load_weekly_stats(conn):
    weekly_cols = [
        "player_id",
        "player_name",
        "recent_team",
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

    print("Loading weekly stats...")
    weekly = nfl.import_weekly_data(YEARS, columns=weekly_cols, downcast=True)

    weekly = weekly.dropna(
        subset=[
            "passing_yards",
            "rushing_yards",
            "receiving_yards",
            "fantasty_points_ppr"
        ],
        how="all",
    )

    weekly.to_sql("weekly stats", conn, if_exists="replace", index=False)
    print(f"Inserted {len(weekly)} weekly stat rows")

def create_indexes(conn):
    cur = conn.cursor()

    print("Creating indexes...")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_players_name ON players(player_name);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_players_team_pos ON players(recent_team, position);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_weekly_player ON weekly_stats(player_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_weekly_season_week ON weekly_stats(season, week);")

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