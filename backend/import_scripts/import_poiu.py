# important! you need to run the script to download all the shift data to the games

def import_poiu_all (db, text, POIU):
    print("Gathering POIU...")
    all_poiu = []
    sql = text("""
                SELECT distinct player_id_1, player_id_2, player_id_3, player_id_4, player_id_5, player_id_6
                FROM (
                        SELECT player_id_1, player_id_2, player_id_3, player_id_4, player_id_5, player_id_6, all_players
                        FROM (
                                SELECT 
                                distinct player_id_1, player_id_2, player_id_3, player_id_4, player_id_5, player_id_6,  
                                CASE 
                                WHEN player_id_3 IS NOT NULL AND player_id_4 IS NULL
                                THEN CAST(player_id_1 as varchar) || ',' || CAST(player_id_2 as varchar) || ',' || COALESCE(CAST(player_id_3 as varchar),'') 
                                
                                WHEN player_id_4 IS NOT NULL AND player_id_5 IS NULL
                                THEN CAST(player_id_1 as varchar) || ',' || CAST(player_id_2 as varchar) || ',' || COALESCE(CAST(player_id_3 as varchar),'') || ',' || COALESCE(CAST(player_id_4 as varchar),'')
                                
                                WHEN player_id_5 IS NOT NULL AND player_id_6 IS NULL
                                THEN CAST(player_id_1 as varchar) || ',' || CAST(player_id_2 as varchar) || ',' || COALESCE(CAST(player_id_3 as varchar),'') || ',' || COALESCE(CAST(player_id_4 as varchar),'') || ',' || COALESCE(CAST(player_id_5 as varchar),'')
                                
                                ELSE
                                CAST(player_id_1 as varchar) || ',' || CAST(player_id_2 as varchar) || ',' || COALESCE(CAST(player_id_3 as varchar),'') || ',' || COALESCE(CAST(player_id_4 as varchar),'') || ',' || COALESCE(CAST(player_id_5 as varchar),'') || ',' || COALESCE(CAST(player_id_6 as varchar),'') 
                                END AS all_players
                                FROM public.game_shift_track
                                )
                        WHERE all_players is not null
		)

        """)
    result = db.session.execute(sql)

    for row in result:
        get_poiu = POIU(
                    player_one_id = row[0],
                    player_two_id = row[1],
                    player_three_id = row[2],
                    player_four_id = row[3],
                    player_five_id = row[4],
                    player_six_id = row[5]
                )
        all_poiu.append(get_poiu)

    try:
        db.session.bulk_save_objects(all_poiu)
        db.session.commit()
    except Exception as error:
        print("FIX ME!")
        print(error)


