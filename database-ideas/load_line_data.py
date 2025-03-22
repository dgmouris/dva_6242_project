import time
import csv
from datetime import datetime

from pathlib import Path

def load_line_data():
    print("Loading line data...")
    file_path = Path(__file__)
    root = file_path.parent.parent.parent

    line_data_file = Path(root / "data" / "shots" / "lines_2023_2024.csv")


    all_line_data = []

    with open(line_data_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # Uses the first line as column headers

        for row in reader:
            # Extract player IDs based on position
            position = row["position"]
            line_id = row["lineId"]
            if position == "line" and len(line_id) == 21:
                player1ID = int(line_id[:7])
                player2ID = int(line_id[7:14])
                player3ID = int(line_id[14:])
            elif position == "pairing" and len(line_id) == 14:
                player1ID = int(line_id[:7])
                player2ID = int(line_id[7:])
                player3ID = None
            else:
                # Handle unexpected cases (optional)
                player1ID = None
                player2ID = None
                player3ID = None

            line_data = {
                "line_id": int(row["lineId"]),
                "season": int(row["season"]),
                "name": row["name"],
                "team": row["team"],
                "position": position,
                "situation": row["situation"],
                "games_played": int(row["games_played"]),
                "icetime": int(row["icetime"]),
                "ice_time_rank": int(row["iceTimeRank"]),
                "x_goals_percentage": float(row["xGoalsPercentage"]),
                "corsi_percentage": float(row["corsiPercentage"]),
                "fenwick_percentage": float(row["fenwickPercentage"]),
                "x_on_goal_for": float(row["xOnGoalFor"]),
                "x_goals_for": float(row["xGoalsFor"]),
                "x_rebounds_for": float(row["xReboundsFor"]),
                "x_freeze_for": float(row["xFreezeFor"]),
                "x_play_stopped_for": float(row["xPlayStoppedFor"]),
                "x_play_continued_in_zone_for": float(row["xPlayContinuedInZoneFor"]),
                "x_play_continued_outside_zone_for": float(row["xPlayContinuedOutsideZoneFor"]),
                "flurry_adjusted_x_goals_for": float(row["flurryAdjustedxGoalsFor"]),
                "score_venue_adjusted_x_goals_for": float(row["scoreVenueAdjustedxGoalsFor"]),
                "flurry_score_venue_adjusted_x_goals_for": float(row["flurryScoreVenueAdjustedxGoalsFor"]),
                "shots_on_goal_for": int(row["shotsOnGoalFor"]),
                "missed_shots_for": int(row["missedShotsFor"]),
                "blocked_shot_attempts_for": int(row["blockedShotAttemptsFor"]),
                "shot_attempts_for": int(row["shotAttemptsFor"]),
                "goals_for": int(row["goalsFor"]),
                "rebounds_for": int(row["reboundsFor"]),
                "rebound_goals_for": int(row["reboundGoalsFor"]),
                "freeze_for": int(row["freezeFor"]),
                "play_stopped_for": int(row["playStoppedFor"]),
                "play_continued_in_zone_for": int(row["playContinuedInZoneFor"]),
                "play_continued_outside_zone_for": int(row["playContinuedOutsideZoneFor"]),
                "saved_shots_on_goal_for": int(row["savedShotsOnGoalFor"]),
                "saved_unblocked_shot_attempts_for": int(row["savedUnblockedShotAttemptsFor"]),
                "penalties_for": int(row["penaltiesFor"]),
                "penalty_minutes_for": int(row["penalityMinutesFor"]),
                "face_offs_won_for": int(row["faceOffsWonFor"]),
                "hits_for": int(row["hitsFor"]),
                "takeaways_for": int(row["takeawaysFor"]),
                "giveaways_for": int(row["giveawaysFor"]),
                "player1ID": player1ID,
                "player2ID": player2ID,
                "player3ID": player3ID,
            }


            all_line_data.append(line_data)
