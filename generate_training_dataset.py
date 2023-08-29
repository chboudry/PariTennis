# 0. match selection decision : only matchs where players has already 6 games played each
# 1. inner join between ATP match and co_uk_data
# 2. cleanup remove missing entries (missing odds)

# 3. add players characeristics
# 4. build features at match date : 
#   - current ATP 
#   - best ATP
#   - Total games
#   - total wins
#   - total games
#   - total surface Type A
#   - total surface type A wins
#   - total surgace type A losses
#   - total surface Type B
#   - total surface type B wins
#   - total surgace type B losses
#   - custom elo
#   - previous wins against other player
#   - previous loss against other player
# Should we do total or mean ? 
# winner_serve_rating
# winner_aces
# winner_double_faults
# winner_first_serves_in
# winner_first_serves_total
# winner_first_serve_points_won
# winner_first_serve_points_total
# winner_second_serve_points_won
# winner_second_serve_points_total
# winner_break_points_saved
# winner_break_points_serve_total
# winner_service_games_played
# winner_return_rating
# winner_first_serve_return_won
# winner_first_serve_return_total
# winner_second_serve_return_won
# winner_second_serve_return_total
# winner_break_points_converted
# winner_break_points_return_total
# winner_return_games_played
# winner_service_points_won
# winner_service_points_total
# winner_return_points_won
# winner_return_points_total
# winner_total_points_won
# winner_total_points_total