import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    file_path = "C:\\Users\\mesza\\Desktop\\movies_analysis\\movies_cvs.csv"
    try:
       
        df = pd.read_csv(file_path, encoding="ISO-8859-1")  # Próbálkozás ISO-8859-1 kódolással
    except Exception as e:
        st.error(f"Hiba történt a fájl beolvasása közben: {e}")
        print(f"Hiba történt a fájl beolvasása közben: {e}")
        return None
    return df

# Adatok betöltése
df = load_data()

# Ha a dataframe nem üres, folytathatjuk
if df is not None:
    # Streamlit alkalmazás beállítása
    st.title("Filmelemző Dashboard")
    st.write("Bemutatjuk a filmek statisztikai elemzését és vizualizációit.")

    # Adatok megjelenítése
    if st.checkbox("Adatok megjelenítése"):
        st.dataframe(df)

    # Pie chart a filmek értékelési kategóriái alapján
    def categorize_rating(rating):
        if rating >= 8.7:
            return "Top Rated"
        elif 7.8 <= rating <= 8.6:
            return "Average Rated"
        else:
            return "Low Rated"

    # Kategóriák létrehozása a 'Rating' oszlop alapján
    df["Rating_Category"] = df["Rating"].apply(categorize_rating)
    category_counts = df["Rating_Category"].value_counts()

    # Pie chart a filmek kategóriáiról
    fig, ax = plt.subplots()
    ax.pie(category_counts, labels=category_counts.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")  # A pie chart kör alakú maradjon
    st.pyplot(fig)

    # Éves megjelenés elemzése
    year_counts = df["Year"].value_counts().sort_index()
    fig, ax = plt.subplots()
    ax.bar(year_counts.index, year_counts.values, color="skyblue")
    ax.set_xlabel("Év")
    ax.set_ylabel("Film darabszám")
    ax.set_title("Megjelenések száma évenként")
    st.pyplot(fig)

    # Legnagyobb profitot termelő filmek megjelenítése
    top_profit_movies = df.sort_values(by="Profit", ascending=False).head(10)
    st.subheader("Top 10 legtöbb profitot termelő film")
    st.dataframe(top_profit_movies)
else:
    st.error("A fájl betöltése nem sikerült.")
