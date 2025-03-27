def update_game_shift_track_poiu (db, text, GameShiftTrack, POIU, update):
    print("Updating Game Shift Data with POIU...")
    
    current_season = 2007

    while current_season < 2024:
    
        all_game_shifts = []
        
        #update to loop through years
        sql = text(
            ("""
                    SELECT g.id, p.id as poiu_id
                    FROM public.game_shift_track g
                    LEFT JOIN public.poiu p
                        ON COALESCE(g.player_id_1,-1) = COALESCE(p.player_one_id,-1)
                        AND COALESCE(g.player_id_2,-1) = COALESCE(p.player_two_id,-1)
                        AND COALESCE(g.player_id_3,-1) = COALESCE(p.player_three_id,-1)
                        AND COALESCE(g.player_id_4,-1) = COALESCE(p.player_four_id,-1)
                        AND COALESCE(g.player_id_5,-1) = COALESCE(p.player_five_id,-1)
                        AND COALESCE(g.player_id_6,-1) = COALESCE(p.player_six_id,-1)
                WHERE CAST(g.game_id as varchar) LIKE '{season}%'
            """).format(season=str(current_season))
        )
        result = db.session.execute(sql)
        
        for row in result:
            all_game_shifts.append({"id": row[0], "poiu_id": row[1]})

        db.session.execute(
            update(GameShiftTrack),
            all_game_shifts
        )

        db.session.commit()
        
        current_season = current_season + 1