use movies;

select top 10 movie, year, rating, metascore
from list
order by year desc;

select movie, rating
from list
where rating >= 9
order by rating desc;

select	min(rating) as Lowest_Rating,
		avg(rating) as Average_Rating,
		max(rating) as Highest_Rating
from list;

select	min(metascore) as Lowest_metascore,
		avg(metascore) as Average_metascore,
		max(metascore) as Highest_metascore
from list;

select	min(profit) as Lowest_profit,
		avg(profit) as Average_profit,
		max(profit) as Highest_profit
from list;

select floor(year / 10) * 10 as Decade, 
       avg(rating) as Average_Rating,
       avg(rating) as Average_Profit
from list
group by floor(year / 10) * 10
order by Decade;

select	floor(year / 10) * 10 as Decade,
		avg(rating) as Average_Rating
from list
group by floor(Year / 10)
having avg(rating) >= 7.5
order by Decade;

select movie, rating,
	case
		when rating >= 8.7 then 'Top Rated'
		when rating <= 8.6 and rating >= 7.8 then 'Average Rated'
		else 'Low Rated'
	end as  rating_category
from list;

select movie, metascore,
	case
		when rating >= 8.7 then 'Top Rated'
		when rating <= 8.6 and rating >= 7.8 then 'Average Rated'
		else 'Low Rated'
	end as  rating_category
from list;

select movie, year, metascore, rating,
	rank() over (partition by year order by rating desc) as Rank
from list
where year >= 2000;

select top 50 movie, profit,
	rank() over (order by profit desc) as Profit_Rank
from list;

select movie, profit
from list
where profit > (select avg(profit) from list)
order by profit desc;

select movie, year, profit
from list i1
where profit = (
	select max (profit)
	from list i2
	where floor (i2. year /10) = floor (i1. year /10) 
	)
order by year;

select year, movie, profit,
	sum(profit) over (partition by year order by profit desc) as Cumulative_Profit
from list;


select top 10 movie, rating, profit
from list
where profit > 66000000			   
order by rating desc;

select top 10 movie, rating, profit
from list
where rating < 7.8
order by profit desc;