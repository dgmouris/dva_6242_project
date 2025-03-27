def update_shot_poiu (db, text, Shot, update):
    print("Updating Shot Data with POIU...")
    
    current_season = 2007

    while current_season < 2024:
    
        all_game_shots = []

        #Edit to loop through seasons
        sql = text("""

    SELECT distinct get_opp.ID,
    gs_off.poiu_id off_poiu

    FROM (SELECT s.*, 
            CASE 
            WHEN s."teamCode" = s."homeTeamCode" THEN s."awayTeamCode" 
            ELSE s."homeTeamCode" 
            END AS oppTeamCode 
            FROM public.shot s
            WHERE s.season = {season}) get_opp
    LEFT JOIN public.game_shift_track gs_off
        ON cast(cast(get_opp.season as varchar) || '0' || cast(get_opp.game_id as varchar) as integer) = gs_off.game_id
        AND period = gs_off.shift_period
        AND time >= gs_off.start_shift_number + ((period - 1) * 1200)
        AND time < gs_off.end_shift_number + ((period - 1) * 1200)
        AND get_opp."teamCode" = gs_off.team_abbrev

            """).format(season=current_season)
        result = db.session.execute(sql)
        
        for row in result:
            all_game_shots.append({"id": row[0], "shooting_poiu_id": row[1]})

        db.session.execute(
            update(Shot),
            all_game_shots
        )

        db.session.commit()


        current_season = current_season + 1