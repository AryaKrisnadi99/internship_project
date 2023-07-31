import pandas as pd
import streamlit as st
import numpy as np
import plotly
import plotly_express as px
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import altair as alt

st.set_page_config(
    page_title="Internship Project",
    layout="wide"
)

opt = option_menu(
    menu_title = None,
    options = ["Introduction", "Analytics"],
    orientation = "horizontal"
)

if opt == "Introduction":
    st.write(" asd ")

else:
    df1 = pd.read_excel("data_project.xlsx", "ig_A")
    df2 = pd.read_excel("data_project.xlsx", "ig_B")
    df3 = pd.read_excel("data_project.xlsx", "ig_C")
    df4 = pd.read_excel("data_project.xlsx", "ER_IG")
    df5 = pd.read_excel("data_project.xlsx", "ER_IG2")

    grafik = st.selectbox("", ["Engagement Instagram", "Comments"])

    if grafik == "Engagement Instagram":
        st.subheader("Perbandingan Jumlah Post")
        col7, col8 = st.columns(2)
        with col7:
            #Grafik engadmen by post
            EngadmenIG = df5.groupby("Perusahaan", as_index=False).agg({"Jumlah_Post":"sum"})
            ENG1 = px.pie(EngadmenIG, names="Perusahaan", values="Jumlah_Post", color="Perusahaan")
            layout = go.Layout(
                autosize=False,
                width=400,
                height=400,
            )
            # ENG1.update_layout(layout)  # Penyesuaian gap grafik dan legend
            ENG1.update_layout(layout,legend=dict(orientation="h",x=0.5, y=-0.1, xanchor='center', yanchor='top'))
            ENG1.update_layout(margin=dict(t=20, b=20, l=50, r=50))
            st.plotly_chart(ENG1, use_container_width=True)

        with col8:
            EngadmenIG = df5.groupby("Perusahaan", as_index=False).agg({"Jumlah_Post":"sum"})
            EngadmenIG_sorted = EngadmenIG.sort_values(by="Jumlah_Post", ascending=False)
            perusahaan_terbesar = EngadmenIG_sorted.iloc[0]["Perusahaan"]
            # css_center_text = '''
            #     <style>
            #         .center-text {
            #             display: flex;
            #             justify-content: center;
            #         }
            #     </style>
            # '''
            teks = f'''Berdasarkan grafik disamping dapat dilihat bahwa dalam rentan waktu 26 Juni 2023 hingga 17 Juni 2023, Perusahaan 
                    {perusahaan_terbesar} memiliki jumlah post terbanyak. Kemudian bagaimana dengan pertumbuhan pengikut harian 
                    instagram Perusahaan {perusahaan_terbesar} dibandingkan dengan kompetitor? Untuk perbandingannya dapat dilihat pada grafik di bawah.'''
            style = "font-size: 18px; text-align: justify; margin-top: 80px; margin-bottom: 20px;"
            # st.markdown("<p style='font-size: 18px; text-align: justify;'>{}</p>".format(teks), unsafe_allow_html=True)
            st.markdown(f"<p style='{style}'>{teks}</p>", unsafe_allow_html=True)
        #Grafik pertumbuhan followers harian
        # Mengubah nama kolom
        df4 = df4.rename(columns={
            'a_day_followers': 'A',
            'b_day_followers': 'B',
            'c_day_followers': 'C'
        })

        # Membuat multiselect untuk memilih kolom yang ingin ditampilkan
        kolom_options = ['A', 'B', 'C']
        multitahun = st.multiselect(
            "Pilih Perusahaan",
            kolom_options,
            default=['A']  # Nilai default saat aplikasi pertama kali dijalankan
        )
        
        # Filter dataframe berdasarkan kolom-kolom yang dipilih
        filtered_df = df4[['date'] + multitahun]
        
        # Melt dataframe menjadi format long untuk line chart dengan Altair
        melted_df = filtered_df.melt('date', var_name='Kolom', value_name='Followers')

        # Membuat line chart dengan Altair
        line_chart = alt.Chart(melted_df).mark_line().encode(
            alt.X('date:T', title='Tanggal'),
            alt.Y('Followers:Q', title='Jumlah Pengikut'),
            color='Kolom:N',
            tooltip=['Kolom:N', 'Followers:Q']
        ).properties(
            title=f"Penambahan Pengikut Instagram Harian Perusahaan {', '.join(map(str, multitahun))}"
        )

        # Menampilkan chart menggunakan Streamlit
        st.altair_chart(line_chart, use_container_width=True)
        st.markdown(
            """
            <div style="text-align: justify;margin-top:-25px">
                Dari hasil visualisasi jumlah pengikut harian ketiga perusahaan. Diperoleh bahwa perusahaan B mempunyai 
                kenaikan yang tinggi pada hari tertentu. Perlu dilakukan peninjauan ulang dalam hari pada saat 
                jumlah pengikut harian tinggi, apakah terdapat suatu acara atau kegiatan yang mengakibatkan kenaikan jumlah pengikut tersebut.
            </div>
            """,
            unsafe_allow_html=True,
        )

        #Proses Grafik Like Instagram
        st.markdown('\n')
        st.subheader("Grafik Perbandingan Jumlah Like")
        freq = st.radio("Frequency", ["Daily", "Monthly"])
        
        df1["Tanggal Upload"] = pd.to_datetime(df1["Tanggal Upload"], format="%d/%m/%Y")
        df2["Tanggal Upload"] = pd.to_datetime(df2["Tanggal Upload"], format="%d/%m/%Y")
        df3["Tanggal Upload"] = pd.to_datetime(df3["Tanggal Upload"], format="%d/%m/%Y")
        if freq == "Daily":
            df1_1 = df1.groupby("Tanggal Upload", as_index=False).agg({"Jumlah Like":"sum"})
            df2_1 = df2.groupby("Tanggal Upload", as_index=False).agg({"Jumlah Like":"sum"})
            df3_1 = df3.groupby("Tanggal Upload", as_index=False).agg({"Jumlah Like":"sum"})
            merged = pd.concat([df1_1, df2_1, df3_1], keys=["A", "B", "C"])
            fig6 = px.line(merged, x="Tanggal Upload", y="Jumlah Like",color=merged.index.get_level_values(0))

        else:
            df1["Month"] = df1["Tanggal Upload"].dt.to_period("M").astype(str)
            df2["Month"] = df2["Tanggal Upload"].dt.to_period("M").astype(str)
            df3["Month"] = df3["Tanggal Upload"].dt.to_period("M").astype(str)
            df1_2 = df1.groupby("Month", as_index=False).agg({"Jumlah Like":"sum"})
            df2_2 = df2.groupby("Month", as_index=False).agg({"Jumlah Like":"sum"})
            df3_2 = df3.groupby("Month", as_index=False).agg({"Jumlah Like":"sum"})
            merged = pd.concat([df1_2, df2_2, df3_2], keys=["A", "B", "C"])
            fig6 = px.line(merged, x="Month", y="Jumlah Like", color=merged.index.get_level_values(0))
        fig6.update_layout(legend_title_text="Perusahaan")
        st.plotly_chart(fig6, use_container_width=True)

        st.markdown(
            """
            <div style="text-align: justify;margin-top:-25px">
                Dari hasil visualisasi perbandingan jumlah like dari ketiga perusahaan, terlihat jelas bahwa perusahaan A 
                memiliki lompatan data jumlah like tertinggi dibandingkan lainnya. Perlu dipertanyakan, pada perusahaan B 
                yang memiliki jumlah kenaikan pengikut naik signifikan akan tetapi jumlah like tidak mencerminkan kenaikan seperti 
                perusahaan A. Asumsi yang dimiliki, jika kenaikan pengikut tinggi maka terdapat suatu post mengenai acara 
                atau kegiatan yang mencerminkan kenaikan pengikut tersebut dan mengakibatkan banyaknya jumlah like pada postingan tersebut.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('\n')
        st.subheader("Top Categories")
    
        col9, col10, col11 = st.columns(3)
        with col9:
            top_a = df1.groupby("Isi Konten", as_index=False).agg({"Jumlah Like":"sum"})
            top_sort = top_a.sort_values(by="Jumlah Like", ascending=False)
            top_cat = top_sort["Isi Konten"].head(5)
            top_sort.loc[~top_sort["Isi Konten"].isin(top_cat), "Isi Konten"]="Others"
            # top1 = px.bar(top_a, x="Isi Konten", y="Jumlah Like", color="Isi Konten")
            top1 = px.pie(top_sort, names="Isi Konten", values="Jumlah Like", color="Isi Konten")
            layout = go.Layout(
                autosize=False,
                width=400,
                height=400,
            )
            top1.update_layout(layout, title="A")
            st.plotly_chart(top1, use_container_width=True)
            st.markdown(
            """
            <div style="text-align: justify;margin-top:-65px">
                Komponen postingan terbanyak berdasarkan like dari perusahaan A yaitu Notifikasi Acara disusul oleh Pameran. 
                Hal ini artinya postingan nontifikasi acara yang di post memiliki dampak baik dalam
                peningkatan antusiasme pengikut sehingga pengikut dapat tau tentang acara apa saja yang akan
                dilaksanakan oleh peruasahaan A. 
            </div>
            """,
            unsafe_allow_html=True,
        )
        with col10:
            top_b = df2.groupby("Isi Konten", as_index=False).agg({"Jumlah Like":"sum"})
            top_sort = top_b.sort_values(by="Jumlah Like", ascending=False)
            top_cat = top_sort["Isi Konten"].head(5)
            top_sort.loc[~top_sort["Isi Konten"].isin(top_cat), "Isi Konten"]="Others"
            # top2 = px.bar(top_B, x="Isi Konten", y="Jumlah Like", color="Isi Konten")
            top2 = px.pie(top_sort, names="Isi Konten", values="Jumlah Like", color="Isi Konten")
            layout = go.Layout(
                autosize=False,
                width=400,
                height=400,
            )
            top2.update_layout(layout, title="B")
            st.plotly_chart(top2, use_container_width=True)
            st.markdown(
            """
            <div style="text-align: justify;margin-top:-65px">
                Komponen postingan terbanyak berdasarkan like dari perusahaan B yaitu Others seperti dokumentasi acara, 
                rapat suatu acara penting seperti kenegaraan, upacara pembukaan kegiatan, dll.
           </div>
            """,
            unsafe_allow_html=True,
        )
        with col11:
            top_c = df3.groupby("Isi Konten", as_index=False).agg({"Jumlah Like":"sum"})
            top_sort = top_c.sort_values(by="Jumlah Like", ascending=False)
            top_cat = top_sort["Isi Konten"].head(5)
            top_sort.loc[~top_sort["Isi Konten"].isin(top_cat), "Isi Konten"]="Others"
            # top3 = px.bar(top_c, x="Isi Konten", y="Jumlah Like", color="Isi Konten")
            top3 = px.pie(top_sort, names="Isi Konten", values="Jumlah Like", color="Isi Konten")
            layout = go.Layout(
                autosize=False,
                width=400,
                height=400,
            )
            top3.update_layout(layout, title="C")
            st.plotly_chart(top3, use_container_width=True)
            st.markdown(
            """
            <div style="text-align: justify;margin-top:-65px">
                Komponen postingan terbanyak berdasarkan like dari perusahaan C yaitu Repost. Merepresentasikan dokumentasi 
                atau hal yang di unggah oleh pihak/akun lain kemudian di repost oleh akun perusahaan C.
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    else:
        st.subheader("Grafik Perbandingan Jumlah Comment")
        freq = st.radio("Frequency", ["Daily", "Monthly"])
        
        df1["Tanggal Upload"] = pd.to_datetime(df1["Tanggal Upload"], format="%d/%m/%Y")
        df2["Tanggal Upload"] = pd.to_datetime(df2["Tanggal Upload"], format="%d/%m/%Y")
        df3["Tanggal Upload"] = pd.to_datetime(df3["Tanggal Upload"], format="%d/%m/%Y")
        if freq == "Daily":
            df1_1 = df1.groupby("Tanggal Upload", as_index=False).agg({"Jumlah Komentar":"sum"})
            df2_1 = df2.groupby("Tanggal Upload", as_index=False).agg({"Jumlah Komentar":"sum"})
            df3_1 = df3.groupby("Tanggal Upload", as_index=False).agg({"Jumlah Komentar":"sum"})
            merged = pd.concat([df1_1, df2_1, df3_1], keys=["A", "B", "C"])
            fig6 = px.line(merged, x="Tanggal Upload", y="Jumlah Komentar", color=merged.index.get_level_values(0))
        else:
            df1["Month"] = df1["Tanggal Upload"].dt.to_period("M").astype(str)
            df2["Month"] = df2["Tanggal Upload"].dt.to_period("M").astype(str)
            df3["Month"] = df3["Tanggal Upload"].dt.to_period("M").astype(str)
            df1_2 = df1.groupby("Month", as_index=False).agg({"Jumlah Komentar":"sum"})
            df2_2 = df2.groupby("Month", as_index=False).agg({"Jumlah Komentar":"sum"})
            df3_2 = df3.groupby("Month", as_index=False).agg({"Jumlah Komentar":"sum"})
            merged = pd.concat([df1_2, df2_2, df3_2], keys=["A", "B", "C"])
            fig6 = px.line(merged, x="Month", y="Jumlah Komentar", color=merged.index.get_level_values(0))
        fig6.update_layout(legend_title_text="Perusahaan")
        st.plotly_chart(fig6, use_container_width=True)

        st.markdown(
            """
            <div style="text-align: justify;margin-top:-25px">
                Dari hasil visualisasi perbandingan jumlah komentar, perusahaan A memiliki lonjakan komentar tertinggi 
                pada 29 Maret 2023 dibandingkan dengan kompetitor lainnya. Dari analisis sebelumnya, banyaknya 
                pengikut harusnya akan mempengaruhi banyak like. Berlaku juga dalam hal ini, banyaknya pengikut 
                akan berpengaruh terhadap banyak komentar yang ada dalam postingan tersebut.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('\n')
        st.subheader("Top Categories")
        col9, col10, col11 = st.columns(3)

        with col9:
            top_a = df1.groupby("Isi Konten", as_index=False).agg({"Jumlah Komentar":"sum"})
            top_sort = top_a.sort_values(by="Jumlah Komentar", ascending=False)
            top_cat = top_sort["Isi Konten"].head(5)
            top_sort.loc[~top_sort["Isi Konten"].isin(top_cat), "Isi Konten"]="Others"
            # top1 = px.bar(top_a, x="Isi Konten", y="Jumlah Like", color="Isi Konten")
            top1 = px.pie(top_sort, names="Isi Konten", values="Jumlah Komentar", color="Isi Konten")
            layout = go.Layout(
                autosize=False,
                width=400,
                height=400,
            )
            top1.update_layout(layout, title="A")
            st.plotly_chart(top1, use_container_width=True)
            st.markdown(
            """
            <div style="text-align: justify;margin-top:-65px">
                Komponen postingan terbanyak berdasarkan komentar dari perusahaan A yaitu Notifikasi Acara 
                disusul oleh Pameran yang sama dengan analisis berdasarkan like.
            </div>
            """,
            unsafe_allow_html=True,
        )
        with col10:
            top_b = df2.groupby("Isi Konten", as_index=False).agg({"Jumlah Komentar":"sum"})
            top_sort = top_b.sort_values(by="Jumlah Komentar", ascending=False)
            top_cat = top_sort["Isi Konten"].head(5)
            top_sort.loc[~top_sort["Isi Konten"].isin(top_cat), "Isi Konten"]="Others"
            # top2 = px.bar(top_b, x="Isi Konten", y="Jumlah Like", color="Isi Konten")
            top2 = px.pie(top_sort, names="Isi Konten", values="Jumlah Komentar", color="Isi Konten")
            layout = go.Layout(
                autosize=False,
                width=400,
                height=400,
            )
            top2.update_layout(layout, title="B")
            st.plotly_chart(top2, use_container_width=True)
            st.markdown(
            """
            <div style="text-align: justify;margin-top:-65px">
                Komponen postingan terbanyak berdasarkan like dari perusahaan B yaitu 
                Notifikasi Acara sebagai pengingat akan adanya acara sesuai waktunya.
            </div>
            """,
            unsafe_allow_html=True,
        )
        with col11:
            top_c = df3.groupby("Isi Konten", as_index=False).agg({"Jumlah Komentar":"sum"})
            top_sort = top_c.sort_values(by="Jumlah Komentar", ascending=False)
            top_cat = top_sort["Isi Konten"].head(5)
            top_sort.loc[~top_sort["Isi Konten"].isin(top_cat), "Isi Konten"]="Others"
            # top3 = px.bar(top_c, x="Isi Konten", y="Jumlah Like", color="Isi Konten")
            top3 = px.pie(top_sort, names="Isi Konten", values="Jumlah Komentar", color="Isi Konten")
            layout = go.Layout(
                autosize=False,
                width=400,
                height=400,
            )
            top3.update_layout(layout, title="C")
            st.plotly_chart(top3, use_container_width=True)
            st.markdown(
            """
            <div style="text-align: justify;margin-top:-65px">
                Komponen postingan terbanyak berdasarkan like dari perusahaan C yaitu Repost sama dengan analisis berdasarkan jumlah like.
            </div>
            """,
            unsafe_allow_html=True,
        )