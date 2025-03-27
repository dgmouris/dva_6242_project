def import_shot_poiu (db, text):
    print("Aggregating POIU Metrics...")


    sql = text("""
with all_seasons as (
SELECT left(cast(game_id as varchar), 4) season, situation, poiu_id, SUM(duration_number) seconds_on_ice, COUNT(distinct CAST(game_id as varchar)) games_played
--situation, poiu_id, SUM(duration_number)
FROM public.game_shift_track
GROUP BY left(cast(game_id as varchar), 4), situation, poiu_id
),
limit_time as (
SELECT *
FROM all_seasons
WHERE situation in ('6 on 6', '6 on 5', '6 on 4', '6 on 3', '5 on 6', '4 on 6', '3 on 6', '5 on 5', '4 on 4', '4 on 5', '5 on 4', '3 on 5', '5 on 3', '3 on 5', '3 on 4', '4 on 3', '3 on 3')
AND poiu_id IS NOT NULL
AND seconds_on_ice >= 600
),
off_metrics as (
SELECT distinct lt.situation, lt.season, lt.poiu_id, --s.event, 
COALESCE(s.goal,0) goal, --s.location, 
COALESCE(s."shotDistance",0) "shotDistance", 
CASE WHEN s."shotType" = 'BACK' THEN 1 ELSE 0 END as shot_back, 
CASE WHEN s."shotType" = 'SNAP' THEN 1 ELSE 0 END as shot_snap, 
CASE WHEN s."shotType" = 'DEFL' THEN 1 ELSE 0 END as shot_defl, 
CASE WHEN s."shotType" = 'TIP' THEN 1 ELSE 0 END as shot_tip, 
CASE WHEN s."shotType" = 'WRAP' THEN 1 ELSE 0 END as shot_wrap, 
CASE WHEN s."shotType" = 'SLAP' THEN 1 ELSE 0 END as shot_slap,
CASE WHEN s."shotType" = 'WRIST' THEN 1 ELSE 0 END as shot_wrist,
CASE WHEN COALESCE(s."shotType",'') = '' THEN 1 ELSE 0 END as shot_na,
COALESCE(s."shotWasOnGoal",0) "shotWasOnGoal", COALESCE(s."shotRebound",0) "shotRebound", 
CASE WHEN s.team = 'HOME' then s.goal ELSE 0 END AS home_goal,
CASE WHEN s.team = 'AWAY' then s.goal ELSE 0 END AS away_goal,
s."xGoal"
FROM (SELECT distinct poiu_id, situation, season FROM limit_time) lt
LEFT JOIN public.shot_poiu offense
	ON lt.poiu_id = offense.shooting_poiu_id
LEFT JOIN public.shot s
	ON offense.id = s.id
),
def_metrics as (
SELECT distinct lt2.situation, lt2.season, lt2.poiu_id, --s.event, 
COALESCE(s2.goal,0) goal, --s.location, 
COALESCE(s2."shotDistance",0) "shotDistance", 
CASE WHEN s2."shotType" = 'BACK' THEN 1 ELSE 0 END as shot_back, 
CASE WHEN s2."shotType" = 'SNAP' THEN 1 ELSE 0 END as shot_snap, 
CASE WHEN s2."shotType" = 'DEFL' THEN 1 ELSE 0 END as shot_defl, 
CASE WHEN s2."shotType" = 'TIP' THEN 1 ELSE 0 END as shot_tip, 
CASE WHEN s2."shotType" = 'WRAP' THEN 1 ELSE 0 END as shot_wrap, 
CASE WHEN s2."shotType" = 'SLAP' THEN 1 ELSE 0 END as shot_slap,
CASE WHEN s2."shotType" = 'WRIST' THEN 1 ELSE 0 END as shot_wrist,
CASE WHEN COALESCE(s2."shotType",'') = '' THEN 1 ELSE 0 END as shot_na,
COALESCE(s2."shotWasOnGoal",0) "shotWasOnGoal", COALESCE(s2."shotRebound",0) "shotRebound", 
CASE WHEN s2.team = 'HOME' then s2.goal ELSE 0 END AS home_goal,
CASE WHEN s2.team = 'AWAY' then s2.goal ELSE 0 END AS away_goal,
s2."xGoal"
FROM (SELECT distinct poiu_id, situation, season FROM limit_time) lt2
LEFT JOIN public.shot_poiu defense
	ON lt2.poiu_id = defense.defending_poiu_id
LEFT JOIN public.shot s2
	ON defense.id = s2.id
),
agg_offense as (
SELECT situation, season, poiu_id, SUM(goal) goal_for, AVG("shotDistance") shot_distance_for, SUM(shot_back) shot_back_for, SUM(shot_snap) shot_snap_for, SUM(shot_defl) shot_defl_for, SUM(shot_tip) shot_tip_for, SUM(shot_wrap) shot_wrap_for, SUM(shot_slap) shot_slap_for, SUM(shot_wrist) shot_wrist_for, SUM("shotWasOnGoal") shot_on_goal_for, SUM("shotRebound") shot_rebound_for, SUM(home_goal) home_goal_for, SUM(away_goal) away_goal_for
FROM off_metrics
GROUP BY situation, season, poiu_id
),
agg_defense as (
SELECT situation, season, poiu_id, SUM(goal) goal_against, AVG("shotDistance") shot_distance_against, SUM("shotWasOnGoal") shot_on_goal_against, SUM("shotRebound") shot_rebound_against, SUM(home_goal) home_goal_against, SUM(away_goal) away_goal_against
FROM def_metrics
GROUP BY situation, season, poiu_id
),
combine_sides as (
SELECT COALESCE(agg_offense.situation, agg_defense.situation) situation,
COALESCE(agg_offense.poiu_id, agg_defense.poiu_id) poiu_id,
COALESCE(agg_offense.season, agg_defense.season) season, 
goal_for, shot_distance_for, shot_back_for, shot_snap_for, shot_defl_for, shot_tip_for, shot_wrap_for, shot_slap_for, shot_wrist_for, shot_on_goal_for, shot_rebound_for, home_goal_for, away_goal_for, 
goal_against, shot_distance_against, shot_on_goal_against, shot_rebound_against, home_goal_against, away_goal_against, seconds_on_ice, games_played
FROM agg_offense
FULL OUTER JOIN agg_defense
	ON agg_offense.situation = agg_defense.situation
	AND agg_offense.season = agg_defense.season
	AND agg_offense.poiu_id = agg_defense.poiu_id
LEFT JOIN all_seasons
	ON COALESCE(agg_offense.situation, agg_defense.situation) = all_seasons.situation
	AND COALESCE(agg_offense.poiu_id, agg_defense.poiu_id) = all_seasons.poiu_id
	AND COALESCE(agg_offense.season, agg_defense.season) = all_seasons.season
)
SELECT *
FROM combine_sides
ORDER BY seconds_on_ice DESC

            """)