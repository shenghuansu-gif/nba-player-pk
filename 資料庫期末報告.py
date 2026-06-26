import streamlit as st
import pandas as pd
import time  # 👈 新增這行
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
# --- 3. 執行抓資料的動作並顯示在畫面上 ---
if st.button("開始 PK！"):
    st.write(f"正在抓取 **{player_a}** 和 **{player_b}** 的生涯數據...")
    
    # 呼叫我們剛剛寫的函數
    stats_a = get_player_stats(player_a)
    
    # 👈 新增這行：讓程式睡 1 秒，避免連續發送請求被 NBA 官網擋掉
    time.sleep(1) 
    
    stats_b = get_player_stats(player_b)
    
    # 把抓回來的資料變成一個漂亮的表格 (DataFrame)
    df_compare = pd.DataFrame([stats_a, stats_b], index=[player_a, player_b])
    
    # 顯示在網頁上！
    st.dataframe(df_compare)
    st.success("資料抓取成功！")
