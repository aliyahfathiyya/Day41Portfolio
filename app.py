import streamlit as st
import pandas as pd 
import plotly.express as px

st.set_page_config(
    page_title="Portofolio Day 41 Fathiyya",
    page_icon="👩🌟",
    layout="wide"
)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("marketing_AB.csv")
    except FileNotFoundError:
        df = pd.read_csv("data/marketing_AB.csv")
        
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    return df

df = load_data()


# 3. SIDEBAR 
st.sidebar.header("Navigasi")
pilihan_halaman = st.sidebar.radio(
    "Pilih Halaman:",
    ("Profil", "Analisis A/B Testing", "Analisis Waktu Iklan")
)

if pilihan_halaman == "Profil":
    st.title("👩 Profil")
    st.write("Halo! Saya Fathiyya, sedang berlatih untuk menjadi analis data. Portfolio ini menjelaskan terkait Analisis efektivitas iklan terhadap konversi user menggunakan dataset Marketing A/B Testing yang saya lakukan dalam bootcamp")
    st.dataframe(df.head())

elif pilihan_halaman == "Analisis A/B Testing":
    st.title("Dashboard Marketing A/B Testing")
    
    if df.empty:
        st.warning("Data kosong! Silakan sesuaikan filter di sidebar.")
    else:
        # Buat Tab
        tab1, tab2 = st.tabs(["Conversion Rate", "Statistik Total Ads"])

        with tab1:
            st.write("### Conversion Rate per Group")
            conv_rate = df.groupby('test_group')['converted'].mean().reset_index()
            
            fig_conv = px.bar(conv_rate, x='test_group', y='converted', 
                              color='test_group',
                              title="Ad vs PSA Conversion")
            st.plotly_chart(fig_conv, use_container_width=True)

        with tab2:
            st.write("### Statistik Total Ads")
            # Tetap menggunakan bar_chart bawaan streamlit sesuai keinginanmu
            data_ads = df['total_ads'].value_counts().head(20).sort_index()
            st.bar_chart(data_ads)

elif pilihan_halaman == "Analisis Waktu Iklan":
    st.title("Analisis Waktu Paparan Iklan")
    
    # Visualisasi Per Hari
    st.subheader("1. Intensitas Iklan Berdasarkan Hari")
    urutan_hari = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    data_hari = df['most_ads_day'].value_counts().reindex(urutan_hari).reset_index()
    data_hari.columns = ['hari', 'jumlah_user']

    fig_day = px.bar(data_hari, x='hari', y='jumlah_user', color='jumlah_user',
                     color_continuous_scale='Blues')
    st.plotly_chart(fig_day, use_container_width=True)

    # Visualisasi Jam
    st.subheader("2. Tren Paparan Iklan Berdasarkan Jam")
    data_jam = df['most_ads_hour'].value_counts().sort_index().reset_index()
    data_jam.columns = ['jam', 'jumlah_user']

    fig_hour = px.line(data_jam, x='jam', y='jumlah_user', markers=True)
    fig_hour.update_layout(xaxis=dict(tickmode='linear'))
    st.plotly_chart(fig_hour, use_container_width=True)

    with st.expander("Lihat Insight"):
        hari_tertinggi = data_hari.loc[data_hari['jumlah_user'].idxmax(), 'hari']
        jam_tertinggi = data_jam.loc[data_jam['jumlah_user'].idxmax(), 'jam']
        st.write(f"- User paling banyak melihat iklan pada hari **{hari_tertinggi}**.")
        st.write(f"- Puncak aktivitas paparan iklan berada pada jam **{jam_tertinggi}:00**.")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")

# Filter
list_group = df['test_group'].unique().tolist()
selected_group = st.sidebar.multiselect("Pilih Group:", list_group, default=list_group)