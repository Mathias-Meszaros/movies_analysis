-- Database -- 
use Movies


-- Year column statistics --

select distinct Year, count(year) as 'Number of Films'
from list
group by year
order by year desc;

-- Time column statistics --

with data as (
select 
	Time, 
	row_number() over(order by Time) as rn, 
	count(*) over () as tc 
from list)
select 
	min(Time) as 'Lower Time', 
	avg(Time) as 'Average Time',
	avg(case when rn in ((tc+1)/2,(tc+2)/2) then Time end) as 'Median Time',
	max(Time) as 'Highest Time'
from data;

-- Average Time by Years
select distinct Year, avg(Time) as 'Average Time'
from list
group by Year
order by Year desc;

-- Rating column statistics --

with data as (
select 
	Rating, 
	row_number() over(order by Rating) as rn, 
	count(*) over () as tc
from list)
select 
	min(Rating) as 'Lower Rating', 
	avg(case when rn in ((tc+1)/2,(tc+2)/2) then Rating end) as 'Median Rating', 
	avg(Rating) as 'Average Rating',
	max(Rating) as 'Highest Rating' 
from data;

-- Rating category counts

select 
	case
		when Rating <= 7.7 then 'Low Rating'
		when Rating between 7.8 and 8.6 then 'Average Rating'
		when Rating >= 8.7 then 'High Rating'
	end as Category, count(*) as Count
from list
group by
	case 
		when Rating <= 7.7 then 'Low Rating'
		when Rating between 7.8 and 8.6 then 'Average Rating'
		when Rating >= 8.7 then 'High Rating'
	end
order by Count asc;

-- Average Rating by Years

select distinct Year, avg(Rating) as 'Average Rating'
from list
group by Year
order by Year desc;

-- Average Rating by Time

select distinct Time, avg(Rating) as 'Average Rating'
from list
group by Time
order by Time desc;


-- Metascore column statistics
with data as (
select 
	Metascore,
	row_number() over(order by Metascore) as rn,
	count(*) over() as tc
from list)
select
	min(Metascore) as 'Lower Metascore',
	avg(case when rn in ((tc+1)/2,(tc+2)/2) then Metascore end) as 'Median Metascore',
	avg(Metascore) as 'Average Metascore',
	max(Metascore) as 'Highest Metascore'
from data;

-- Metascore count by Category
select
	case
		when Metascore <= 52 then 'Low Metascore'
		when Metascore Between 53 and 89 then 'Average Metascore'
		when Metascore >= 90 then 'High Metascore'
	end as Category, count(*) as Count
from list
group by
	case
		when Metascore <= 52 then 'Low Metascore'
		when Metascore Between 53 and 89 then 'Average Metascore'
		when Metascore >= 90 then 'High Metascore'
	end
order by Count asc;

-- Average Metascore by Year
select distinct Year, avg(Metascore) as 'Average Metascore'
from list
group by Year
order by Year desc;

-- Average Metascore by Time
select distinct Time, avg(Metascore) as 'Average Metascore'
from list
group by Time
order by Time desc;

-- Profit column statistics --
;with data as (
    select 
		Profit,
        row_number() over(order by Profit) as rn,
        count(*) over() as tc
    from list)
select 
    min(Profit) as 'Lowest Profit',
    avg(case when rn in ((tc+1)/2,(tc+2)/2) then Profit else null end) as 'Median Profit',
    avg(Profit) AS 'Average Profit',
    max(Profit) AS 'Highest Profit'
from data;

-- Total Profit by Year
select distinct Year, sum(Profit) as 'Total Profit'
from list
group by Year
order by Year desc;

-- Average Profit by Year
select distinct Year, avg(Profit) as 'Average Profit'
from list
group by Year
order by Year desc;

-- Average Profit by Rating
select distinct Rating, avg(profit) as 'Average Profit'
from list
group by Rating
order by Rating desc;

-- Average Profit by Metascore
select distinct Metascore, avg(profit) as 'Average Profit'
from list
group by Metascore
order by Metascore desc;

-- Average Profit by Decade
select (year/10)*10 as Decade, avg(Profit) as 'Average Profit'
from list
group by (year/10)*10
order by Decade desc;

-- Additional Analysis --

-- High Rating Movies
select Movie, Rating
from list
where Rating >= 8.7
order by Rating desc

-- High Metascore Movies
select Movie, Metascore
from list
where Metascore >= 90
order by Metascore desc;

-- Top 10 Highest-grossing film
select top 10 Movie, Profit
from list
order by Profit desc;

-- Top 10 Longest Movies
select top 10 Movie, Time
from list
order by Time desc;

-- Highest-grossing films by Decades
;with Decade as (
	select 
		Movie, 
		Profit, 
		(Year/10)*10 as Decade
	from list),

Ranked as (
	select
		Movie,
		Profit,
		Decade,
		row_number() over (partition by Decade order by Profit desc) as rn
	from Decade)

select
	Decade,
	Movie,
	Profit
from Ranked
where rn = 1
order by Decade desc;

-- Best Rated Movies by Decades
with Decade as (
	select 
		Movie,
		Rating,
		(Year/10)*10 as Decade
	from list),

Ranked as (
	select
		Movie,
		Rating,
		Decade,
		row_number() over (partition by Decade order by Rating desc) as rn
	from Decade)

select
	Decade,
	Movie,
	Rating
from Ranked
where rn = 1
order by Decade desc;

-- Best Metascored Movies by Decades
with Decade as (
	select
		Movie,
		Metascore,
		(Year/10)*10 as Decade
	from list),

Ranked as (
	select
		Movie,
		Metascore,
		Decade,
		row_number() over (partition by Decade order by Metascore desc) as rn
	from Decade)

select 
	Decade,
	Movie,
	Metascore
from Ranked
where rn = 1
order by Metascore desc;