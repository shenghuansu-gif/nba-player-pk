@st.cache_data
def get_player_stats(player_name):
    # a. 先從名字找到這個球員的專屬 ID
    nba_players = players.get_players()
    player_dict = [player for player in nba_players if player['full_name'] == player_name][0]
    player_id = player_dict['id']

    # b. 用這個 ID 去跟 NBA 總部要他整個生涯的數據表
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    df = career.get_data_frames()[0]

    # c. 計算他生涯的總平均 (拿總數除以上場場次)
    total_pts = df['PTS'].sum()
    total_reb = df['REB'].sum()
    total_ast = df['AST'].sum()
    total_gp = df['GP'].sum() # GP = Games Played (出場數)

    # 🏀 新增的防呆機制：如果總出場數為 0，則所有平均數據皆設為 0
    if total_gp == 0:
        avg_pts = 0.0
        avg_reb = 0.0
        avg_ast = 0.0
    else:
        avg_pts = round(total_pts / total_gp, 1)
        avg_reb = round(total_reb / total_gp, 1)
        avg_ast = round(total_ast / total_gp, 1)

    return {"得分 (PTS)": avg_pts, "籃板 (REB)": avg_reb, "助攻 (AST)": avg_ast}
