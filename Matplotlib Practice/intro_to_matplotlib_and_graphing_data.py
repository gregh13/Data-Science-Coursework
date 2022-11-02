# -*- coding: utf-8 -*-
"""Intro to MatPlotLib and Graphing Data

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CqVUd-ggIjK3JdZQsQfqiOXtK1PeAwTU

## Get the Data

Either use the provided .csv file or (optionally) get fresh (the freshest?) data from running an SQL query on StackExchange: 

Follow this link to run the query from [StackExchange](https://data.stackexchange.com/stackoverflow/query/675441/popular-programming-languages-per-over-time-eversql-com) to get your own .csv file

<code>
select dateadd(month, datediff(month, 0, q.CreationDate), 0) m, TagName, count(*)
from PostTags pt
join Posts q on q.Id=pt.PostId
join Tags t on t.Id=pt.TagId
where TagName in ('java','c','c++','python','c#','javascript','assembly','php','perl','ruby','visual basic','swift','r','object-c','scratch','go','swift','delphi')
and q.CreationDate < dateadd(month, datediff(month, 0, getdate()), 0)
group by dateadd(month, datediff(month, 0, q.CreationDate), 0), TagName
order by dateadd(month, datediff(month, 0, q.CreationDate), 0)
</code>

## Import Statements
"""

import pandas as pd
import matplotlib.pyplot as plt

"""## Data Exploration

**Challenge**: Read the .csv file and store it in a Pandas dataframe
"""

# Can rename columns when making df
raw_df = pd.read_csv('QueryResults.csv', header=0, names=["DATE", "TAG", "POSTS"])

"""**Challenge**: Examine the first 5 rows and the last 5 rows of the of the dataframe"""

display(raw_df.head())
display(raw_df.tail())
raw_df

"""**Challenge:** Check how many rows and how many columns there are. 
What are the dimensions of the dataframe?
"""

raw_df.shape

"""**Challenge**: Count the number of entries in each column of the dataframe"""

display(raw_df.count())
group_counted = raw_df.groupby('TAG').count()
group_counted

"""**Challenge**: Calculate the total number of post per language.
Which Programming language has had the highest total number of posts of all time?
"""

pd.options.display.float_format = '{:,.0f}'.format
group_tag = raw_df.groupby('TAG')
mean_count = group_tag.mean()
display(mean_count)
sum_count = group_tag.sum()
display(sum_count)
sum_count.sort_values('POSTS', ascending=False)

"""Some languages are older (e.g., C) and other languages are newer (e.g., Swift). The dataset starts in September 2008.

**Challenge**: How many months of data exist per language? Which language had the fewest months with an entry? 

"""

group_counted.sort_values('DATE')

"""## Data Cleaning

Let's fix the date format to make it more readable. We need to use Pandas to change format from a string of "2008-07-01 00:00:00" to a datetime object with the format of "2008-07-01"
"""

type(raw_df.DATE[1])

# Changes the string date values in the column into Pandas Datetime objects/Series
raw_df.DATE = pd.to_datetime(raw_df['DATE'])

type(raw_df.DATE[1])

raw_df

raw_df.info()

"""## Data Manipulation


"""

test_df = pd.DataFrame({'Age': ['Young', 'Young', 'Young', 'Young', 'Old', 'Old', 'Old', 'Old'],
                        'Actor': ['Jack', 'Arnold', 'Keanu', 'Sylvester', 'Jack', 'Arnold', 'Keanu', 'Sylvester'],
                        'Power': [100, 80, 25, 50, 99, 75, 5, 30]})
display(test_df)
test_df.pivot(index="Age", columns="Actor", values="Power").sort_values('Age', ascending=False)

"""**Challenge**: Pivot our dataframe about Programming Languages. What are the dimensions of our new dataframe? How many rows and columns does it have? Print out the column names and print out the first 5 rows of the dataframe."""



reshaped_df = raw_df.pivot(index='DATE', columns='TAG', values='POSTS')
# Note that by pivoting the table, we created some NaN. Need to clean it up in next step
reshaped_df

reshaped_df.shape

"""**Challenge**: Count the number of entries per programming language. Why might the number of entries be different? """

reshaped_df.count()

# Fill in NaN with the .fillna() - change NaN to value of 0
# inplace=True helps to actually save the changes to our table (instead of df = df.filna())
reshaped_df.fillna(0, inplace=True) 
reshaped_df.count()

# We can look through to double_check there are no more NaN values:
reshaped_df.isna().values.any()

"""## Data Visualisaton with with Matplotlib

**Challenge**: Use the [matplotlib documentation](https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot) to plot a single programming language (e.g., java) on a chart.
"""

# you can include the index as the x-axis
plt.plot(reshaped_df.index, reshaped_df['java'])

# Or just leave it blank and it defaults to using the index
plt.plot(reshaped_df['java'])
# We can do things to change the graph:
# figsize makes it bigger (x,y)
plt.figure(figsize=(16,10))
# with a bigger graph, axis increment ticks need to be adjusted
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
# Can add labels to axis (even recognizes \n :D)
plt.xlabel("\nDate", fontsize=18)
plt.ylabel("Number of Posts\n", fontsize=18)
# Limit the plot window based on values on axis:
plt.ylim(0,35000)
plt.plot(reshaped_df['python'])

"""**Challenge**: Show two line (e.g. for Java and Python) on the same chart."""

plt.plot(reshaped_df['java'])
plt.plot(reshaped_df['python'])

# Here's how to plot all the columns in a graph

for column in reshaped_df.columns:
    plt.plot(reshaped_df.index, reshaped_df[column])

# Note that plot modifications are contained to specific plots

plt.figure(figsize=(16,10))
# with a bigger graph, axis increment ticks need to be adjusted
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
# Can add labels to axis (even recognizes \n :D)
plt.xlabel("\nDate", fontsize=18)
plt.ylabel("Number of Posts\n", fontsize=18)
# Limit the plot window based on values on axis:
plt.ylim(0,35000)
plt.plot(reshaped_df['python'])

# Make graph easier to read with linewidth and legend changes
for column in reshaped_df.columns:
    plt.plot(reshaped_df.index, reshaped_df[column], linewidth=3, label=reshaped_df[column].name)

plt.legend(fontsize=18)

"""# Smoothing out Time Series Data

Time series data can be quite noisy, with a lot of up and down spikes. To better see a trend we can plot an average of, say 6 or 12 observations. This is called the rolling mean. We calculate the average in a window of time and move it forward by one overservation. Pandas has two handy methods already built in to work this out: [rolling()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rolling.html) and [mean()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.window.rolling.Rolling.mean.html). 
"""

rolling_mean_java = reshaped_df['java'].rolling(window=6).mean()
rolling_mean_python = reshaped_df['python'].rolling(window=6).mean()

plt.plot(rolling_mean_java)

plt.plot(rolling_mean_java)
plt.plot(rolling_mean_python)

# You can do it individually, or just make a whole new table and go from there:

roll_df = reshaped_df.rolling(window=6).mean()
 
plt.figure(figsize=(16,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)
 
# plot the roll_df instead
for column in roll_df.columns:
    plt.plot(roll_df.index, roll_df[column], 
             linewidth=3, label=roll_df[column].name)
 
plt.legend(fontsize=16)