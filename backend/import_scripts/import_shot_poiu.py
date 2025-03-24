def import_shot_poiu (db, text, Shot, POIU, insert, ShotPOIU):
    print("Importing Shot Data with POIU...")

    sql = text("""

with ot_check as (
    SELECT ot.game_id, ot.shift_period, ot.team_abbrev, ot.start_shift_number, ot.end_shift_number, poiu_id
    FROM public.game_shift_track ot
    INNER JOIN (
                SELECT game_id, team_abbrev, shift_period, MAX(start_shift_number) last_ot_shift
                FROM public.game_shift_track
                WHERE shift_period = 4
                GROUP BY game_id, team_abbrev, shift_period) iso_last
        ON ot.game_id = iso_last.game_id
        AND ot.shift_period = iso_last.shift_period
        AND ot.team_abbrev = iso_last.team_abbrev
        AND ot.start_shift_number = iso_last.last_ot_shift
)
SELECT distinct get_opp.auto_gen_id, 
COALESCE(gs_off.poiu_id, ot_check.poiu_id ) off_poiu,  
COALESCE(gs_def.poiu_id, ot_opp.poiu_id ) def_poiu

FROM (SELECT s.*, 
		CASE 
		WHEN s."teamCode" = s."homeTeamCode" THEN s."awayTeamCode" 
		ELSE s."homeTeamCode" 
		END AS oppTeamCode 
		FROM public.shot s) get_opp
LEFT JOIN public.game_shift_track gs_off
	ON cast(cast(get_opp.season as varchar) || '0' || cast(get_opp.game_id as varchar) as integer) = gs_off.game_id
	AND period = gs_off.shift_period
	AND time >= gs_off.start_shift_number + ((period - 1) * 1200)
	AND time < gs_off.end_shift_number + ((period - 1) * 1200)
	AND get_opp."teamCode" = gs_off.team_abbrev
LEFT JOIN public.game_shift_track gs_def
	ON cast(cast(get_opp.season as varchar) || '0' || cast(get_opp.game_id as varchar) as integer) = gs_def.game_id
	AND get_opp.oppTeamCode = gs_def.team_abbrev
	AND period = gs_def.shift_period
		AND time  >= gs_def.start_shift_number  + ((period - 1) * 1200)
		AND time < gs_def.end_shift_number + ((period - 1) * 1200)
LEFT JOIN ot_check
	ON cast(cast(get_opp.season as varchar) || '0' || cast(get_opp.game_id as varchar) as integer) = ot_check.game_id
	AND get_opp."teamCode" = ot_check.team_abbrev
	AND period = ot_check.shift_period
	AND time  >= ot_check.start_shift_number + ((period - 1) * 1200)
	AND time <= ot_check.end_shift_number + ((period - 1) * 1200)

LEFT JOIN ot_check ot_opp
	ON cast(cast(get_opp.season as varchar) || '0' || cast(get_opp.game_id as varchar) as integer) = ot_opp.game_id
	AND get_opp.oppTeamCode = ot_opp.team_abbrev
	AND period = ot_opp.shift_period
	AND time  >= ot_opp.start_shift_number + ((period - 1) * 1200)
	AND time <= ot_opp.end_shift_number + ((period - 1) * 1200)
WHERE COALESCE(gs_off.poiu_id, ot_check.poiu_id ) IS NOT NULL AND COALESCE(gs_def.poiu_id, ot_opp.poiu_id ) IS NOT NULL

        """)
    result = db.session.execute(sql)
    
    all_shot_poiu_to_insert = []
    
    for row in result:

        shot = ShotPOIU(
            id = row[0], 
            shooting_poiu_id = row[1],
            defending_poiu_id = row[2]
        )

        all_shot_poiu_to_insert.append(shot)

    try:
        db.session.bulk_save_objects(all_shot_poiu_to_insert)
        db.session.commit()
    except Exception as error:
        print("FIX ME!")
        print(error)

    db.session.commit()