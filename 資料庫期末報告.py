import streamlit as st
import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

st.title("NBA 終極球員數據PK台")

# --- 1. 準備球員名單 ---
player_list = ["LeBron James", "Stephen Curry", "Kevin Durant", "Giannis Antetokounmpo", "Luka Dončić", "Nikola Jokić", "Jayson Tatum", "Anthony Edwards", "Shai Gilgeous-Alexander", "Victor Wembanyama"]

player_a = st.selectbox("請選擇球員 A：", player_list)
player_b = st.selectbox("請選擇球員 B：", player_list, index=1)
st.write("---")

# --- 2. 建立一個函數來抓取球員數據 ---
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

    # 🏀 防呆機制：如果總出場數為 0，則所有平均數據皆設為 0 (解決 ZeroDivisionError)
    if total_gp == 0:
        avg_pts = 0.0
        avg_reb = 0.0
        avg_ast = 0.0
    else:
        avg_pts = round(total_pts / total_gp, 1)
        avg_reb = round(total_reb / total_gp, 1)
        avg_ast = round(total_ast / total_gp, 1)

    return {"得分 (PTS)": avg_pts, "籃板 (REB)": avg_reb, "助攻 (AST)": avg_ast}

# --- 3. 執行抓資料的動作並顯示在畫面上 ---
if st.button("開始 PK！"):
    st.write(f"正在抓取 **{player_a}** 和 **{player_b}** 的生涯數據...")
    
    # 呼叫我們剛剛寫的函數
    stats_a = get_player_stats(player_a)
    stats_b = get_player_stats(player_b)
    
    # 把抓回來的資料變成一個漂亮的表格 (DataFrame)
    df_compare = pd.DataFrame([stats_a, stats_b], index=[player_a, player_b])
    
    # 顯示在網頁上！
    st.dataframe(df_compare)
    st.success("資料抓取成功！")
