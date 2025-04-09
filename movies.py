import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_data ():
    file_path =  os.path.join(os.path.dirname(__file__), "movies.csv")
    try:
        df = pd .read_csv (file_path, encoding = "ISO-8859-1") 
    except Exception as e:
        st .error (f"An error occurred while reading the file: {e}")
        print (f"An error occurred while reading the file.: {e}")
        return None
    return df


df = load_data ()
 
if df is not None:


    st .title ("Movie Analysis Dashboard")
    st .write ("The dashboard is designed to present statistical analyses and reports derived from the given database.")
    st .write ("First, the individual columns of the database are presented in tables for statistical purposes, and sometimes as visualizations.")
    st .write ("Afterwards, textual report additions accompany each process for better understanding.")
    
    ## Movies Data ##

    if st.checkbox ("Movies Data"):
        st.dataframe (df)
    
    st .write ("The table contains a total of 1,000 movies from 1920 to 2022. The films collected here are primarily those rated above average by viewers (with at least an IMDb rating of 7.0 or higher). Thus, this analysis essentially evaluates the more popular movies.")

    
    ## Year column statistics ##

    st .title ("Year column statistics")

    yearly_movie_count = df .groupby ("Year") .size () .reset_index (name = "Number of Films")
    yearly_movie_count = yearly_movie_count .sort_values (by = "Year", ascending = False)
    
    st .dataframe (yearly_movie_count)
    
    fig , ax = plt .subplots (figsize = (10,5))
    ax .bar (yearly_movie_count ["Year"], yearly_movie_count ["Number of Films"], 
             color = '#2E4053')
    ax .set_title ("Number of Films per Year")
    ax .set_xlabel ("Year")
    ax .set_ylabel ("Number of Films")
    ax .yaxis .grid (True, linestyle = "--", alpha = 0.25)
    
    st .pyplot (fig)

    st .write ("We can clearly observe an increasing trend in both the report and the graph. The highest number of above-average-rated movies were released in 2004 and 2014. Following this, the number of above-average-rated films approximately doubled in the 2000s.")
    st .write ("It is also important to note the occasional declines, which occurred between 1960 and 1980 and again around 2020. These downturns may reflect the economic difficulties of those times.")
    st .write ("Overall, it can be said that with technological and film industry advancements, more popular movies have been produced in the period after the 2000s.")

    ## Time column statistics ##

    st .title ("Time column statistics")

    df ["rn"] = df ["Time"] .rank (method = "first")
    df ["tc"] = len (df)

    highest_time = df ["Time"] .max ()
    average_time = df ["Time"] . mean ()
    median_time = df ["Time"] .median ()
    lower_time = df ["Time"] . min ()

    result = pd .DataFrame ({
        "Category" : ["Highest Time", "Average Time", "Median Time", "Lower Time"],
        "Value" : [highest_time, average_time, median_time, lower_time]
        })
    
    st .dataframe (result)

    fig , ax = plt .subplots (figsize = (8, 4))
    sns .boxplot (x = df ["Time"], color = "#EA2010", ax = ax)

    ax .set_title ("Boxplot of Movie Durations", fontsize = 14)
    ax .set_xlabel ("Duration (Minutes)", fontsize = 12)
    ax .grid (True, linestyle = "--", alpha = 0.25)
    
    st .pyplot (fig)


    st .write ("The report shows that the longest film was 321 minutes (5 hours and 35 minutes) long. On average, films lasted 123.75 minutes (2 hours and 6 minutes), which is supported by the median value of 120 minutes (2 hours). This reflects the true average duration. The shortest popular film, on the other hand, is only 45 minutes long.")
    
    # Average Time by Year

    average_time_by_year = df .groupby ("Year", as_index = False) ["Time"] .mean()
    average_time_by_year = average_time_by_year .sort_values (by = "Year", ascending = False)
    
    st .subheader ("Average Time by Year")
    st .dataframe (average_time_by_year)

    fig , ax = plt .subplots ()
    ax .plot (average_time_by_year ["Year"], average_time_by_year ["Time"],
              linewidth = 1, color = "#EA2010")
    ax .set_title("Average Time by Year")
    ax .set_xlabel("Year")
    ax .set_ylabel("Average Time (in minute)")
    ax .xaxis .grid (True, linestyle = "--", alpha = 0.25)
    ax .yaxis .grid (True, linestyle = "--", alpha = 0.25)
    
    st.pyplot(fig)

    st. write ("It is clearly visible that after 100 years, the average film length has shifted from 60 - 90 minutes to a slightly increasing trend within the 120 - 140 minute range. Although runtime is secondary to viewers if the content is of high quality, it seems that we are still pushing these limits.")
    
    ## Rating column statistics ##

    st .title ("Rating column statistics")

    df_sorted = df [["Rating"]] .dropna () .sort_values (by = "Rating") .reset_index (drop = True)

    highest_rating = df_sorted ["Rating"] .max ()
    average_rating = df_sorted ["Rating"] .mean ()
    median_rating = df_sorted ["Rating"] .median ()
    lower_rating = df_sorted ["Rating"] .min ()
    

    rating_summary = pd .DataFrame({
        "Category" : ["Higher Rating", "Average Rating", "Median Rating", "Lower Rating"],
        "Value" : [highest_rating, average_rating, median_rating, lower_rating]
        })
        
    st . dataframe (rating_summary)

    fig , ax = plt .subplots (figsize = (8, 4))
    sns .boxplot (x = df ["Rating"], color = "#F39C12" , ax = ax)
    ax .set_title ("Boxplot of Movie Ratings", fontsize = 14)
    ax .set_xlabel ("Ratings", fontsize = 12)
    ax .grid (True, linestyle = "--", alpha = 0.25)

    st .pyplot (fig)

    st .write ("For IMDb (viewer) ratings, the highest score is 9.3, followed by an average of 7.9627 and a median of 7.9. The difference between the two is 0.0627, which is relatively low, indicating that the average rating accurately represents the overall trend. The lowest rating is 7.6.")
    
    # Rating Category Counts 

    def categorize_rating (rating) :
        if rating <= 7.7 :
           return "Low Rating"
        elif 7.8 <= rating <= 8.6 :
            return "Average Rating"
        else:
            return "High Rating"
        
    df ["Category"] = df ["Rating"] .apply (categorize_rating)

    rating_counts = df ["Category"] .value_counts () .reset_index()
    rating_counts .columns = ["Category", "Count"]
    rating_counts = rating_counts .sort_values (by = "Count", ascending = True)

    st .subheader ("Rating Category Counts")
    st .dataframe (rating_counts)

    fig , ax = plt .subplots()
    wedges, texts, autotexts = ax .pie(
        rating_counts["Count"], labels = rating_counts["Category"], autopct =lambda p: '{:.1f} %\n ({:,.0f})' .format (p, p * sum (rating_counts ["Count"]) / 100), startangle = 90,
        colors = ['#FDEBD0', '#9C640C', '#F39C12'],
        wedgeprops = {'edgecolor': 'black'},
        textprops = {'fontsize': 12})
    ax .set_title ("Rating Category Distribution", fontsize = 14)

    st .pyplot (fig)

    st .write ("Based on the rating categorization, a total of 20 movies achieved a high rating (8.7 and above), 720 movies fell into the average category (with scores between 7.8 and 8.6), and 260 movies received a low rating (below 7.7). Overall, we can conclude that very few movies received a unanimously high rating from viewers. This also reflects how difficult it is to appeal to a large audience and gain widespread approval.")


    # Average Rating by Yers

    average_rating_by_year = df .groupby ("Year") ["Rating"] .mean () .reset_index ()
    average_rating_by_year = average_rating_by_year . sort_values (by = "Year", ascending = False)

    st .subheader (" Average Rating by Year")
    st .dataframe (average_rating_by_year)

    fig , ax = plt .subplots ()
    ax .plot (average_rating_by_year ["Year"], average_rating_by_year ["Rating"],
              color = "#E18c18",linestyle = "--", linewidth = 0.5, marker = "o", markersize = 3)
    ax .set_title ("Average Rating by Year")
    ax .set_xlabel ("Year")
    ax .set_ylabel ("Average Rating")
    ax .xaxis .grid (True, linestyle = "--", alpha = 0.25)
    ax .yaxis .grid (True, linestyle = "--", alpha = 0.25)

    st .pyplot (fig)
    
    st .write ("In this report, we can see that viewer ratings fluctuate within a narrow but slightly declining range, roughly between 7.8 and 8.1, with occasional short-term spikes. One likely reason for this trend is that the increasing volume of film production creates tougher competition, making it more challenging for movies to achieve consistently high ratings.")

    # Average Rating by Time

    average_rating_by_time = df .groupby ("Time") ["Rating"] .mean() .reset_index()
    average_rating_by_time = average_rating_by_time .sort_values (by = "Time", ascending = False)

    st .subheader ("Average Rating by Time")
    st .dataframe (average_rating_by_time)

    fig , ax = plt .subplots()
    ax .plot (average_rating_by_time ["Time"], average_rating_by_time ["Rating"],
              color = "#E18c18", linewidth = 1)
    ax .set_title ("Average Rating by Time")
    ax .set_xlabel ("Time (in minute)")
    ax .set_ylabel ("Average Rating")
    ax .xaxis.grid(True, linestyle="--", alpha=0.25)
    ax .yaxis.grid(True, linestyle="--", alpha=0.25)
    ax .set_axisbelow(True)

    st. pyplot (fig)

    st .write ("In contrast, this report reveals a slight upward trend in the duration of movies over time. While there are also extreme outliers, particularly around the 200-minute mark, this could indicate that viewers tend to appreciate longer films, even those around three hours in length.")


    # Metascore column Statistics

    st .title ("Metascore column Statistics")

    highest_metascore = df ["Metascore"] .max ()
    average_metascore = df ["Metascore"] . mean ()
    median_metascore = df ["Metascore"] .median ()
    lower_metascore = df ["Metascore"] . min ()

    result = pd .DataFrame ({
        "Category" : ["Highest Metascore", "Average Metascore", "Median Metascore", "Lower Metascore"],
        "Value" : [highest_metascore, average_metascore, median_metascore, lower_metascore]
        })
    
    st .dataframe (result)

    fig , ax = plt .subplots (figsize = (8, 4))
    sns .boxplot (x = df ["Metascore"], color = "#BA4A00" , ax = ax)
    ax .set_title ("Boxplot of Movie Metascores", fontsize = 14)
    ax .set_xlabel ("Metascores", fontsize = 12)
    ax .grid (True, linestyle = "--", alpha = 0.25)

    st .pyplot (fig)

    st .write ("On a scale from 0 to 100, the highest-rated film by critics received a perfect score of 100. Following this, the average rating is 78.041, with a median of 78. The low deviation of 0.041 suggests that the average rating is not skewed. However, the lowest rating recorded is 28, which is significantly lower compared to the average.")

    # Metascore count by Category

    def categorize_metascore (metascore) :
        if metascore <= 52 :
            return "Low Metascore"
        elif 53 <= metascore <= 89 :
            return "Average Metascore"
        else:
            return "High Metascore"
            
    df ["Metascore Category"] = df ["Metascore"] .apply (categorize_metascore)

    metascore_counts = df ["Metascore Category"] .value_counts () .reset_index ()
    metascore_counts .columns = ["Category", "Count"]
    metascore_counts = metascore_counts .sort_values (by = "Count", ascending = True )

    st .subheader ("Metascore Category Counts")
    st .dataframe (metascore_counts)

    fig , ax = plt .subplots()
    wedges, texts, autotexts = ax .pie(
        metascore_counts["Count"], labels = metascore_counts["Category"], autopct =lambda p: '{:.1f} %\n ({:,.0f})' .format (p, p * sum (rating_counts ["Count"]) / 100), startangle = 90,
        colors = ['#EDBB99', '#873600', '#DC7633'],
        wedgeprops = {'edgecolor': 'black'},
        textprops = {'fontsize': 12})
    
    ax .set_title ("Metascore Category Distribution", fontsize = 14)

    st .pyplot (fig)
    
    st .write ('A total of 169 films fall into the high Metascore category (90 or above). The average category includes 808 films with scores between 53 and 89, while only 23 films received a low Metascore (below 52). This report may also suggest that critics tend to rate films as nearly "perfect" more often than general audiences do (it is important to note that critics are also fewer in number).')

    # Average Metascore by Year

    average_metascore_by_year = df .groupby ("Year") ["Metascore"] .mean() .reset_index()
    average_metascore_by_year = average_metascore_by_year .sort_values (by = "Year", ascending = False)

    st .subheader ("Average Metascore by Year")
    st .dataframe (average_metascore_by_year)

    fig, ax = plt.subplots()
    ax .plot (average_metascore_by_year ["Year"], average_metascore_by_year ["Metascore"],
              color="#873600",linestyle = "--", linewidth = 0.5, marker = "o", markersize = 3)
    ax .set_title ("Average Metascore by Year")
    ax .set_xlabel ("Year")
    ax .set_ylabel ("Average Metascore")
    ax .xaxis.grid (True, linestyle="--", alpha=0.25)
    ax .yaxis.grid (True, linestyle="--", alpha=0.25)
    ax .set_ylim (average_metascore_by_year ["Metascore"] .min () - 5, 
                  average_metascore_by_year ["Metascore"] .max () + 5)

    st .pyplot(fig)

    st .write ("The average annual Metascore shows a continuously declining trend within a stable range. Critics rated films from before the 1980s higher than those from the 2000s and beyond.")

    # Average Metascore by Time

    average_metascore_by_time = df .groupby ("Time", as_index=False) ["Metascore"] .mean ()
    average_metascore_by_time = average_metascore_by_time .sort_values (by="Time", ascending=False)

    st .subheader("Average Metascore by Time")
    st .dataframe (average_metascore_by_time)

    fig, ax = plt .subplots()
    ax .plot (average_metascore_by_time ["Time"], average_metascore_by_time ["Metascore"],
              color = "#873600", linewidth = 1)
    ax .set_title ("Average Metascore by Time")
    ax .set_xlabel ("Time")
    ax .set_ylabel ("Average Metascore")
    ax .xaxis.grid (True, linestyle="--", alpha=0.25)
    ax .yaxis.grid (True, linestyle="--", alpha=0.25)
    ax .set_ylim (average_metascore_by_time ["Metascore"].min () - 5, 
                  average_metascore_by_time ["Metascore"].max () + 5)

    st.pyplot(fig)

    st .write ("Regarding film durations, critics showed significantly more varied ratings for films around 60 minutes and those close to 200 minutes.")

    # Profit column statistics
    
    st .title ("Profit column statistics")

    highest_profit = df ["Profit"] .max ()
    average_profit = df ["Profit"] .mean ()
    median_profit = df ["Profit"] .median ()
    lower_profit = df ["Profit"] .min () 

    result = pd .DataFrame({
        "Category": ["Highest Profit", "Average Profit", "Median Profit", "Lower Profit"],
        "Value": [highest_profit, average_profit, median_profit, lower_profit]
        })
    
    st .dataframe (result)
    
    fig , ax = plt .subplots (figsize = (8, 4))
    sns .boxplot (x = df ["Profit"], color = "#27AE60" , ax = ax)
    ax .set_title ("Boxplot of Movie Profits", fontsize = 14)
    ax .set_xlabel ("Profits (in billion)", fontsize = 12)
    ax .grid (True, linestyle = "--", alpha = 0.25)

    st .pyplot (fig)

    st .write ("In the Profit Report, we can see that the highest profit is 1,495,000,000. However, if we consider the average profit of 65,353,324.402 and the median profit of 17,630,000, we notice a significant difference of 47,723,324.402 between them.")
    st .write ("The BoxPlot visualization also highlights this disparity. The green area indicates that the median value is closer to the lower end of the profit range. Moreover, a considerable number of data points fall outside the whiskers, particularly on the higher end, between 0.0 and approximately 0.18.")
    st .write ("Therefore, in this case, it is more appropriate to consider a value between the median and the average when interpreting profit trends.")
    st .write ("Additionally, it is important to note that for 17 films, the reported profit is 0. This is due to the lack of publicly available data regarding their profitability.")
   
    # Total Profit by Year
    
    average_profit_by_year = df .groupby ("Year", as_index = False) ["Profit"] .sum ()
    average_profit_by_year = average_profit_by_year .sort_values (by = "Year", ascending = False)

    st .subheader ("Total Profit by Year")
    st .dataframe (average_profit_by_year)

    fig, ax = plt.subplots()
    ax .bar (average_profit_by_year ["Year"], average_profit_by_year ["Profit"], 
             color="#1D8348")
    ax .set_title ("Total Profit by Year")
    ax .set_xlabel ("Year")
    ax .set_ylabel ("Sum of Profit (in billion)")
    ax .yaxis.grid (True, linestyle = "--", alpha = 0.25)

    st .pyplot (fig)    

    st .write ("From the annual total profit, we can observe a consistently increasing trend. Notably, by 1962, the most popular films had already reached an impressive total of 889,934,229, which was a significant amount for that period.")
    st .write ("From that point onward, the total profit surpassed 1.39 billion for the first time in 1988, marking the first instance of profits exceeding a billion. From the 2000s onwards, this amount practically doubled or even quadrupled.")
    st .write ("However, the years 1978, 1996, and 2020 saw drastically lower total profits. This was likely influenced by the economic situation at the time.")

   # Average Profit by Year
    
    average_profit_by_year = df .groupby ("Year", as_index = False) ["Profit"] .mean ()
    average_profit_by_year = average_profit_by_year .sort_values (by = "Year", ascending = False)

    st .subheader ("Average Profit by Year")
    st .dataframe (average_profit_by_year)

    fig, ax = plt.subplots()
    ax .bar (average_profit_by_year ["Year"], average_profit_by_year ["Profit"], 
             color="#1D8348")
    ax .set_title ("Average Profit by Year")
    ax .set_xlabel ("Year")
    ax .set_ylabel ("Average Profit (in hundred million)")
    ax .yaxis.grid (True, linestyle = "--", alpha = 0.25)

    st .pyplot (fig)    

    st .write ("In terms of average annual profit, we can observe a trend of lower growth. The 100-million average annual value was most often achieved after the 2000s. In 1977, the average annual 100-million mark was broken for the first time, and in 2022, the evaluation shows an outstanding average exceeding 400 million. However, this is due to one film that had exceptionally high total revenue that year.")

    # Average Profit by Decade
    
    df ["Decade"] = (df ["Year"] // 10) * 10
    average_profit_by_decade = df .groupby ("Decade", as_index = False)["Profit"] .mean ()
    average_profit_by_decade = average_profit_by_decade .sort_values(by = "Decade", ascending = False)

    st .subheader ("Average Profit by Decade")
    st .dataframe (average_profit_by_decade)

    fig , ax = plt .subplots()
    bar_width = 5
    ax.bar(average_profit_by_decade["Decade"], average_profit_by_decade["Profit"], 
           color="#1D8348", width = bar_width)
    ax .set_title ("Average Profit by Decade")
    ax .set_xlabel ("Decade")
    ax .set_ylabel ("Average Profit (in hundred million)")
    ax .yaxis .grid (True, linestyle = "--", alpha = 0.25)

    st .pyplot (fig)

    st. write ("The average profit measured over decades clearly demonstrates the trend of steadily increasing revenue.")

    # Average Profit by Rating

    average_profit_by_rating = df .groupby ("Rating", as_index=False) ["Profit"] .mean ()
    average_profit_by_rating = average_profit_by_rating .sort_values (by = "Rating", ascending = False)
    
    st .subheader ("Average Profit by Rating")
    st .dataframe (average_profit_by_rating)
    
    fig , ax = plt .subplots()
    ax .scatter (average_profit_by_rating ["Rating"], average_profit_by_rating ["Profit"], 
              color = "#1D8348", s = 200)
    ax.set_title("Average Profit by Rating")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Average Profit (in hundred million)")
    ax.xaxis.grid(True, linestyle="--", alpha=0.25)
    ax.yaxis.grid(True, linestyle="--", alpha=0.25)
    
    st.pyplot(fig)

    st .write ("Regarding the average profit and viewer ratings, we can see that, in some cases, high ratings justify the high average profit. However, it is essential to note that quite extreme values can be observed between 8.50 and 9.3. At ratings of 8.8 and 9, the average profit exceeded 200 million, while at ratings of 8.9 and 9.3, it was only 28 and 56 million on average. Furthermore, ratings below 8.3 did not reach an average of 100 million.")

    # Average Profit by Metascore

    average_profit_by_metascore = df .groupby("Metascore", as_index=False) ["Profit"] .mean ()
    average_profit_by_metascore = average_profit_by_metascore .sort_values (by = "Metascore", ascending = False)

    st .subheader ("Average Profit by Metascore")
    st .dataframe (average_profit_by_metascore)

    fig, ax = plt.subplots()
    ax.plot (average_profit_by_metascore ["Metascore"], average_profit_by_metascore ["Profit"],
           color="#1D8348", linewidth = 1)

    ax .set_title ("Average Profit by Metascore")
    ax .set_xlabel ("Metascore")
    ax .set_ylabel ("Average Profit (in hundred million)")
    ax .xaxis.grid (True, linestyle="--", alpha=0.25)
    ax .yaxis.grid (True, linestyle="--", alpha=0.25)

    st .pyplot (fig)

    st .write ("In terms of average profit and Metascore evaluations, we can see that most films range between 40 million and 100 million. The most outstanding average profit reached 160 million with a Metascore of 65. Overall, it can be said that critics clearly evaluate films from a different perspective than viewers, and in most cases, this is not directly proportional to the revenues.")

    ## Additional Analysis ##

    st. title ("Additional Analysis")

    # High Rating Movies

    high_rating_movies = df [df ["Rating"] >= 8.7] [["Movie", "Rating"]]
    high_rating_movies = high_rating_movies .sort_values (by = "Rating", ascending = False)
    st .subheader ("High Rating Movies")
    st .dataframe (high_rating_movies)

    st .write ("The table includes the 20 films whose IMDb (viewer rating) score is at least 8.7 or higher.")

    # Top 10 Highest-grossing film

    top_10_profit_movies = df [["Movie", "Profit"]] .sort_values (by = "Profit", ascending = False) .head (10)
    st .subheader ("Top 10 Movies by Profit")
    st .dataframe (top_10_profit_movies)

    st .write ("This table features the TOP 10 films that have achieved the highest profits")

    # Highest-grossing films by Decades

    df['Decade'] = (df['Year'] // 10) * 10
    df['Rank'] = df.groupby('Decade')['Profit'].rank(method='first', ascending=False)
    
    top_profit_movies_per_decade = df [df['Rank'] == 1] [['Decade', 'Movie', 'Profit']]
    top_profit_movies_per_decade = top_profit_movies_per_decade .sort_values (by = 'Decade', ascending = False)

    st.subheader ("Top Profited Movies by Decade")
    st.dataframe (top_profit_movies_per_decade)

    st .write ("The highest-grossing films by decade")

    # Best Rated Movies by Decades

    df['Decade'] = (df['Year'] // 10) * 10
    df['Rank'] = df .groupby('Decade') ['Rating'] .rank (method = 'first', ascending = False)
    
    top_rated_movies_per_decade = df [df['Rank'] == 1] [['Decade', 'Movie', 'Rating']]
    top_rated_movies_per_decade = top_rated_movies_per_decade .sort_values(by = 'Rating', ascending = False)

    st .subheader ("Top Rated Movies by Decade")
    st .dataframe (top_rated_movies_per_decade)

    st .write ("Movies rated highest by viewers, decade by decade.")

    # Best Metascored Movies by Decades

    df['Decade'] = (df['Year'] // 10) * 10
    df['Rank'] = df .groupby('Decade') ['Metascore'] .rank (method = 'first', ascending = False)
    
    top_metascore_movies_per_decade = df [df['Rank'] == 1] [['Decade', 'Movie', 'Metascore']]
    top_metascore_movies_per_decade = top_metascore_movies_per_decade .sort_values(by = 'Metascore', ascending = False)

    st .subheader ("Top Metascored Movies by Decade")
    st .dataframe (top_metascore_movies_per_decade)

    st .write ("The best films rated by critics, decade by decade.")

    st .title ("Final assessment of the analysis")

    # Top 10 Longes Movies

    top_10_time_movies = df [["Movie", "Time"]] .sort_values (by = "Time", ascending = False) .head (10)

    st .subheader ("Top 10 Movies by Time")
    st .dataframe (top_10_time_movies)

    st .write ("This table features the 10 longest films.")

    st .title ("Final evaluation")
    st .write ("The various analyses have highlighted certain facts about the film industry. First and foremost, we have learned that, unsurprisingly, the production of films has been increasing decade by decade. This trend brings tighter competition to the market.")
    st. write ("The duration of films also shows a certain degree of increase. Recently, short multi-episode miniseries have gained significant popularity, as they allow for film-length content to be divided into multiple episodes in greater detail. Feedback indicates that viewers still find these a comfortable way to spend their time.")
    st .write ("In terms of ratings, we can see that feedback from viewers rarely reaches the maximum scores on the scale. This is partly due to the fact based on the number of viewers, as in large averages there are almost certainly some who will give opposing ratings even to the best films, resulting in not completely extreme scores.")
    st .write ("This is partly supported by critical ratings, who, although fewer in number, are often brave enough to unanimously award even maximum scores to films they analyze. No matter how you look at it, there is a significant proportional difference between them and the general audience, particularly in the fact that, out of 1,000 films, only 2% (20 films) received high ratings from viewers, while 16.9% (169 films) received high ratings from critics.")
    st .write ("In terms of profit, we see an upward trend, partly thanks to the emerging trends in the film industry but also due to the effects of inflation. Over time, increasingly larger sums and revenues are being concentrated within the industry.")
    st .write ("While it cannot be unanimously concluded from the analysis that it is solely the duration or ratings that reflect the large profits achieved, it does suggest that people tend to favor longer films, especially if they offer enriching experiences. Broadly speaking, the film industry has perhaps been striving in recent decades to make its movies appealing to as wide an audience as possible, thereby achieving higher revenues and increasing the likelihood of receiving above-average ratings. However, what exactly justifies these ratings would be a question for another study.")

else:
    st .error("The file could not be loaded.")