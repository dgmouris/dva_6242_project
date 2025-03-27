def import_player_shift_tracking(db, insert, Game, PlayerShiftTrack, GameShiftTrack, text):
    print("Importing shift data for season")

    sql_clear_player = text("""
                TRUNCATE TABLE public.player_shift_track
    """)

    games = db.session.query(Game).all()

    for index, game in enumerate(games):
        all_game_shifts_to_insert = []
        all_game_shifts = games[index].shift_data

        if all_game_shifts:
            for shift in all_game_shifts:

                if (shift['startTime'] != shift['endTime']):
            
                    player_shift = PlayerShiftTrack(
                        id=shift['id'],
                        game_id = shift['gameId'],
                        player_id = shift['playerId'],
                        team_id = shift['teamId'],
                        team_abbrev = shift['teamAbbrev'],
                        shift_number = shift['shiftNumber'],
                        shift_period = shift['period'],
                        start_shift_number = shift['startTimeNumber'],
                        end_shift_number = shift['endTimeNumber'],
                        duration_number = shift['endTimeNumber'] - shift['startTimeNumber']
                    )
                    all_game_shifts_to_insert.append(player_shift)

            try:
                db.session.bulk_save_objects(all_game_shifts_to_insert)
                db.session.commit()
            except Exception as error:
                print("FIX ME!")
                print(error)
                
            sql = text("""
                        with shift_starts as (
                            SELECT distinct shift_period, start_shift_number
                            FROM public.player_shift_track 
                            ),
                            rank_player_id as (
                            SELECT no_goalie.*, rank() over (partition by no_goalie.shift_period, no_goalie.start_shift_number, team_id order by no_goalie.shift_period, no_goalie.start_shift_number, team_id, player_id) rank_player_id
                            FROM (SELECT distinct shift_starts.*, team_id, player_id, team_abbrev
                                    FROM shift_starts
                                    LEFT JOIN public.player_shift_track pst
                                    ON shift_starts.shift_period = pst.shift_period
                                    AND shift_starts.start_shift_number >= pst.start_shift_number
                                    AND shift_starts.start_shift_number < pst.end_shift_number
                                    LEFT JOIN public.player p
                                    ON pst.player_id = p.id
                                    WHERE COALESCE(position,'G') != 'G') no_goalie
                            ),
                            add_poi_to_rank as (
                            SELECT rpi.*, players_on_ice
                            FROM rank_player_id rpi
                            LEFT JOIN (
                            SELECT shift_period, start_shift_number, team_id, count(distinct player_id) players_on_ice
                            FROM rank_player_id
                            GROUP BY  shift_period, start_shift_number, team_id) get_poi

                            ON rpi.shift_period = get_poi.shift_period
                            AND rpi.start_shift_number = get_poi.start_shift_number
                            AND rpi.team_id = get_poi.team_id
                            ),
                            pivot_rows as (

                            SELECT team_id, team_abbrev, shift_period, start_shift_number, players_on_ice, 
                            max(player_id) filter (where rank_player_id = 1) player_1,
                            max(player_id) filter (where rank_player_id = 2) player_2,
                            max(player_id) filter (where rank_player_id = 3) player_3,
                            max(player_id) filter (where rank_player_id = 4) player_4,
                            max(player_id) filter (where rank_player_id = 5) player_5,
                            max(player_id) filter (where rank_player_id = 6) player_6--,
                            --max(player_id) filter (where rank_player_id = 7) player_7
                            FROM add_poi_to_rank
                            GROUP BY team_id, team_abbrev, shift_period, start_shift_number, players_on_ice
                            ),
                            get_opp_players as (
                            SELECT distinct pivot_rows.*, opp_players_on_ice
                            FROM pivot_rows
                            INNER JOIN (SELECT distinct team_id, shift_period, start_shift_number, players_on_ice opp_players_on_ice FROM pivot_rows) get_opp
                            ON pivot_rows.team_id != get_opp.team_id
                            AND pivot_rows.shift_period = get_opp.shift_period
                            AND pivot_rows.start_shift_number = get_opp.start_shift_number
                            ),
                            find_diffs as (
                            SELECT distinct get_opp_players.*,
                            CASE 
                            WHEN COALESCE(LAG(cast(team_id as varchar) || ',' || 
                                        cast(shift_period as varchar) || ',' || 
                                        cast(players_on_ice as varchar) || ',' ||
                                        COALESCE(cast(player_1 as varchar),'-') || ',' ||
                                        COALESCE(cast(player_2 as varchar),'-') || ',' ||
                                        COALESCE(cast(player_3 as varchar),'-') || ',' ||
                                        COALESCE(cast(player_4 as varchar),'-') || ',' ||
                                        COALESCE(cast(player_5 as varchar),'-') || ',' ||
                                        COALESCE(cast(player_6 as varchar),'-') || ',' ||
                                        --COALESCE(cast(player_7 as varchar),'-') ||
                                        cast(opp_players_on_ice as varchar)) 
                                        
                                        OVER 
                                        
                                        (PARTITION BY team_id, shift_period 
                                        ORDER BY team_id, shift_period, start_shift_number),
                                        'first row') 
                                        
                                        != cast(team_id as varchar) || ',' || 
                                            cast(shift_period as varchar) || ',' || 
                                            cast(players_on_ice as varchar) || ',' || 
                                            COALESCE(cast(player_1 as varchar),'-') || ',' || 
                                            COALESCE(cast(player_2 as varchar),'-') || ',' || 
                                            COALESCE(cast(player_3 as varchar),'-') || ',' || 
                                            COALESCE(cast(player_4 as varchar),'-') || ',' || 
                                            COALESCE(cast(player_5 as varchar),'-') || ',' || 
                                            COALESCE(cast(player_6 as varchar),'-') || ',' || 
                                            --COALESCE(cast(player_7 as varchar),'-') || 
                                            cast(opp_players_on_ice as varchar) 
                                        
                                        THEN 1
                            ELSE 0
                            END AS NEW_LINE
                            FROM get_opp_players
                            ),
                            changes_situation as (
                            SELECT team_id, team_abbrev, shift_period, start_shift_number, 
                            cast(players_on_ice as varchar) || ' on ' || cast(opp_players_on_ice as varchar)  situation,
                            player_1, player_2, player_3, player_4, player_5, player_6--, player_7
                            FROM find_diffs
                            WHERE new_line = 1
                            ),
                            get_next as (
                            SELECT changes_situation.*, LEAD(start_shift_number) OVER (PARTITION BY team_id, shift_period ORDER BY team_id, shift_period, start_shift_number) end_shift_number
                            FROM changes_situation
                            ),
                            adj_end as (
                            SELECT get_next.team_id, get_next.team_abbrev, get_next.shift_period, get_next.start_shift_number, COALESCE (get_next.end_shift_number, max_end) end_shift_number, situation, 
                            get_next.player_1, get_next.player_2, get_next.player_3, get_next.player_4, get_next.player_5, get_next.player_6--, get_next.player_7
                            FROM get_next
                            LEFT JOIN (
                            SELECT team_id, team_abbrev, shift_period, MAX(end_shift_number) max_end
                            FROM public.player_shift_track 
                            GROUP BY team_id, team_abbrev, shift_period) get_end_period
                            ON get_next.team_id = get_end_period.team_id
                            AND get_next.team_abbrev = get_end_period.team_abbrev
                            AND get_next.shift_period = get_end_period.shift_period
                            )
                            SELECT adj_end.*, end_shift_number - start_shift_number duration_number
                            FROM adj_end
                            WHERE start_shift_number != end_shift_number
            """)
            result = db.session.execute(sql)
            
            
            all_shifts_from_game_to_insert = []
            
            for row in result:

                game_shift = GameShiftTrack(
                    team_id= row[0], 
                    team_abbrev= row[1], 
                    shift_period= row[2],
                    start_shift_number = row[3],
                    end_shift_number = row[4],
                    situation = row[5],
                    game_id = shift['gameId'],
                    player_id_1 = row[6],
                    player_id_2 = row[7],
                    player_id_3 = row[8],
                    player_id_4 = row[9],
                    player_id_5 = row[10],
                    player_id_6 = row[11],
                    duration_number = row[12]
                )

                all_shifts_from_game_to_insert.append(game_shift)

            try:
                db.session.bulk_save_objects(all_shifts_from_game_to_insert)
                db.session.commit()
            except Exception as error:
                print("FIX ME!")
                print(error)

            try:
                db.session.execute(sql_clear_player)
                db.session.commit()
            except Exception as error:
                print("FIX ME!")
                print(error)
        