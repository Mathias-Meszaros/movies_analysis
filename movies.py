import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Adatbetöltő függvény
def load_data():
    file_path = "C:\\Users\\mesza\\Desktop\\Portfolio\\movies_analysis\\movies.csv"
    try:
        df = pd.read_csv(file_path, encoding="ISO-8859-1")  # Kódolási hiba esetén próbáld meg "ISO-8859-1"-et
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
    if st.checkbox("Show Data"):
        st.dataframe(df)

    # Rating és Metascore kategorizálása
    def categorize_rating(rating):
        if rating >= 8.7:
            return "Top Rated"
        elif 7.8 <= rating <= 8.6:
            return "Average Rated"
        else:
            return "Low Rated"

    df["Rating Category"] = df["Rating"].apply(categorize_rating)

    def categorize_metascore(rating):
        if rating >= 8.7:
            return "Top Rated"
        elif 7.8 <= rating <= 8.6:
            return "Average Rated"
        else:
            return "Low Rated"

    df["Metascore Category"] = df["Metascore"].apply(categorize_metascore)

    # SQL lekérdezések a pandas segítségével
    # 1. Top 10 filmek megjelenítése év szerint rendezve
    top_10_movies = df[['Movie', 'Year', 'Rating', 'Metascore']].sort_values(by='Year', ascending=False).head(10)
    st.subheader("Top 10 Movies by Year")
    st.dataframe(top_10_movies)

    # 2. Filmek, amelyek értékelése ≥ 9
    high_rating_movies = df[df['Rating'] >= 9][['Movie', 'Rating']].sort_values(by='Rating', ascending=False)
    st.subheader("Movies with Rating ≥ 9")
    st.dataframe(high_rating_movies)

    # 3. Minimum, átlag és maximum rating
    rating_stats = df[['Rating']].agg(['min', 'mean', 'max'])
    st.subheader("Rating Statistics")
    st.dataframe(rating_stats)

    # 4. Minimum, átlag és maximum metascore
    metascore_stats = df[['Metascore']].agg(['min', 'mean', 'max'])
    st.subheader("Metascore Statistics")
    st.dataframe(metascore_stats)

    # 5. Minimum, átlag és maximum profit
    profit_stats = df[['Profit']].agg(['min', 'mean', 'max'])
    st.subheader("Profit Statistics")
    st.dataframe(profit_stats)

    # 6. Decade szerinti átlag rating és profit
    df['Decade'] = (df['Year'] // 10) * 10  # Decade oszlop létrehozása
    decade_stats = df.groupby('Decade').agg({'Rating': 'mean', 'Profit': 'mean'}).reset_index()
    st.subheader("Decade-wise Average Rating and Profit")
    st.dataframe(decade_stats)

    # 7. Decade szerinti átlag rating, ahol a rating ≥ 7.5
    high_rating_decades = decade_stats[decade_stats['Rating'] >= 7.5]
    st.subheader("Decades with Average Rating ≥ 7.5")
    st.dataframe(high_rating_decades)

    # 8. Rating Category Distribution
    rating_category_counts = df["Rating Category"].value_counts()
    st.subheader("Rating Category Distribution")
    st.write(rating_category_counts)

    # 9. Metascore Category Distribution
    metascore_category_counts = df["Metascore Category"].value_counts()
    st.subheader("Metascore Category Distribution")
    st.write(metascore_category_counts)

    # 10. Rank a filmek között, rangsorolva rating alapján
    df['Rank'] = df.groupby('Year')['Rating'].rank(method='first', ascending=False)
    top_rated_by_year = df[['Movie', 'Year', 'Rating', 'Rank']].query('Year >= 2000')
    st.subheader("Movies Ranked by Rating (Post 2000)")
    st.dataframe(top_rated_by_year)

    # 11. Top 50 profit rangsorolása
    top_profit_movies = df[['Movie', 'Profit']].sort_values(by='Profit', ascending=False).head(50)
    st.subheader("Top 50 Movies by Profit")
    st.dataframe(top_profit_movies)

    # 12. Profit, amely nagyobb mint az átlagos profit
    avg_profit = df['Profit'].mean()
    high_profit_movies = df[df['Profit'] > avg_profit][['Movie', 'Profit']].sort_values(by='Profit', ascending=False)
    st.subheader("Movies with Profit Above Average")
    st.dataframe(high_profit_movies)

    # 13. Legnagyobb profit a hasonló években (decád alapján)
    highest_profit_in_decade = df.loc[df.groupby(df['Decade'])['Profit'].idxmax()][['Movie', 'Year', 'Profit']]
    st.subheader("Highest Profit Movies per Decade")
    st.dataframe(highest_profit_in_decade)

    # Grafikák:

    # 1. Sum of Profit by Year - Stacked Column Chart
    profit_by_year = df.groupby('Year').agg({'Profit': 'sum'}).reset_index()
    fig, ax = plt.subplots()
    ax.bar(profit_by_year['Year'], profit_by_year['Profit'], color='#F22B00')
    ax.set_xlabel('Year')
    ax.set_ylabel('Sum of Profit (in Billions)')
    ax.set_title('Sum of Profit by Year')
    st.pyplot(fig)

    # 2. Average of Profit and Average of Profit by Rating - Scatter Chart
    avg_profit_rating = df.groupby('Rating').agg({'Profit': 'mean'}).reset_index()
    fig, ax = plt.subplots()
    ax.scatter(avg_profit_rating['Rating'], avg_profit_rating['Profit'], color='#E76604', s=500)
    ax.set_xlabel('Rating')
    ax.set_ylabel('Average of Profit (in Billions)')
    ax.set_title('Average of Profit and Average of Profit by Rating')
    st.pyplot(fig)

    # 3. Count of Rating Category by Rating Category - Pie Chart
    fig, ax = plt.subplots()
    def func(pct, allvals):
        absolute = round(pct / 100.*sum(allvals))
        return f"{pct:.1f}% ({absolute})"
    ax.pie(rating_category_counts, labels=rating_category_counts.index, autopct=lambda pct: func(pct, rating_category_counts), startangle=90)
    ax.axis('equal')  # Pie chart kör alakú maradjon
    st.pyplot(fig)

    # 4. Average of Metascore by Decade - Stacked Bar Chart
    avg_metascore_decade = df.groupby('Decade').agg({'Metascore': 'mean'}).reset_index()
    fig, ax = plt.subplots()
    bar_width = 5.0
    ax.barh(avg_metascore_decade['Decade'], avg_metascore_decade['Metascore'], color='#FDB46C', height=bar_width)
    ax.set_xlabel('Decade')
    ax.set_ylabel('Average of Metascore')
    ax.set_title('Average of Metascore by Decade')
    st.pyplot(fig)

else:
    st.error("The file could not be loaded.")
