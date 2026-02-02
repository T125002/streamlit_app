import streamlit as st
import pandas as pd
import plotly.express as px

st.title('北海道 4大都市の人口比較分析')

df = pd.read_csv('streamlit_app/hokkaido_pop.csv', encoding='shift_jis')

df_2020 = df[df['調査年'] == '2020年度'].copy()

if df_2020['総人口'].dtype == 'object':
    df_2020['総人口'] = df_2020['総人口'].str.replace(',', '').astype(int)

selected_cities = st.multiselect(
    '比較したい市町村を選択してください',
    options=df_2020['地域'].unique(),
    default=['北海道 札幌市', '北海道 函館市', '北海道 旭川市', '北海道 帯広市']
)

df_selection = df_2020[df_2020['地域'].isin(selected_cities)]

if not df_selection.empty:
    # 棒グラフ
    st.subheader("都市別の人口規模（棒グラフ）")
    fig_bar = px.bar(
        df_selection, 
        x='地域', 
        y='総人口', 
        color='地域',
        text_auto=',', 
        title="2020年度 人口比較"
    )
    st.plotly_chart(fig_bar)

    # 円グラフ
    st.subheader("4都市内の人口比率（円グラフ）")
    fig_pie = px.pie(
        df_selection, 
        values='総人口', 
        names='地域', 
        title='人口シェア'
    )
    st.plotly_chart(fig_pie)

    # メトリック表示
    st.subheader("詳細数値")
    cols = st.columns(len(selected_cities))
    for i, city in enumerate(selected_cities):
        pop = df_selection[df_selection['地域'] == city]['総人口'].values[0]
        cols[i].metric(label=city.replace('北海道 ', ''), value=f"{int(pop):,} 人")

st.divider() 
st.subheader("考察")

user_note = st.text_area(
    "分析して気づいたことなどを書いてください：",
    placeholder="例：圧倒的な札幌、頑張ってる旭川、没落した函館、帯広？？？？？？？？？"
)

if user_note:
    st.info(f"【保存されたメモ】\n\n{user_note}")