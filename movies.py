import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    file_path = "C:\\Users\\mesza\\Desktop\\Portfolio\\movies_analysis\\movies_cvs.csv"
    try:
       
        df = pd.read_csv(file_path, encoding="ISO-8859-1")  # Próbálkozás ISO-8859-1 kódolással
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
        print(f"An error occurred while reading the file.: {e}")
        return None
    return df

# Adatok betöltése
df = load_data()

# Ha a dataframe nem üres, folytathatjuk
if df is not None:
    # Streamlit alkalmazás beállítása
    st.title("Movie Analysis Dashboard")
    st.write("Statistical analysis and visualizations of films")

    # Adatok megjelenítése
    if st.checkbox("Database"):
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
    df["Rating Category"] = df["Rating"].apply(categorize_rating)
    category_counts = df["Rating Category"].value_counts()

    # Pie chart a filmek kategóriáiról
    fig, ax = plt.subplots()
    ax.pie(category_counts, labels=category_counts.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")  # A pie chart kör alakú maradjon
    st.pyplot(fig)

    # Éves megjelenés elemzése
    year_counts = df["Year"].value_counts().sort_index()
    fig, ax = plt.subplots()
    ax.bar(year_counts.index, year_counts.values, color="skyblue")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of movies")
    ax.set_title("Number of publications per year")
    st.pyplot(fig)

    # Legnagyobb profitot termelő filmek megjelenítése
    top_profit_movies = df.sort_values(by="Profit", ascending=False).head(10)
    st.subheader("Top 10 highest-grossing films")
    st.dataframe(top_profit_movies)
else:
    st.error("The file could not be loaded.")
