# 1. 最上面一定要先引入所有需要的套件！
import streamlit as st
import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

# 2. 接著可以放標題或全域變數
st.title("NBA 終極球員數據PK台")

player_list = ["LeBron James", "Stephen Curry", "Kevin Durant", "Giannis Antetokounmpo", "Luka Dončić", "Nikola Jokić", "Jayson Tatum", "Anthony Edwards", "Shai Gilgeous-Alexander", "Victor Wembanyama"]

player_a = st.selectbox("請選擇球員 A：", player_list)
player_b = st.selectbox("請選擇球員 B：", player_list, index=1)
st.write("---")

# 3. 再來才是放加上了 @st.cache_data 的函數
@st.cache_data
def get_player_stats(player_name):
    nba_players = players.get_players()
    player_dict = [player for player in nba_players if player['full_name'] == player_name][0]
    player_id = player_dict['id']

    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    df = career.get_data_frames()[0]

    total_pts = df['PTS'].sum()
    total_reb = df['REB'].sum()
    total_ast = df['AST'].sum()
    total_gp = df['GP'].sum() 

    # 防呆機制
    if total_gp == 0:
        avg_pts = 0.0
        avg_reb = 0.0
        avg_ast = 0.0
    else:
        avg_pts = round(total_pts / total_gp, 1)
        avg_reb = round(total_reb / total_gp, 1)
        avg_ast = round(total_ast / total_gp, 1)

    return {"得分 (PTS)": avg_pts, "籃板 (REB)": avg_reb, "助攻 (AST)": avg_ast}

# 4. 最後是執行按鈕與畫面顯示
if st.button("開始 PK！"):
    # ... (下略原本的按鈕執行程式碼) ...
