# -*- coding: utf-8 -*-
"""Nobel_Prize_Analysis_Day_78

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Wg8c6PBqVTdxDYTVCzeZaTVx4lKgKn03

# Setup and Context

### Introduction

On November 27, 1895, Alfred Nobel signed his last will in Paris. When it was opened after his death, the will caused a lot of controversy, as Nobel had left much of his wealth for the establishment of a prize.

Alfred Nobel dictates that his entire remaining estate should be used to endow “prizes to those who, during the preceding year, have conferred the greatest benefit to humankind”.

Every year the Nobel Prize is given to scientists and scholars in the categories chemistry, literature, physics, physiology or medicine, economics, and peace. 

<img src=https://i.imgur.com/36pCx5Q.jpg>

Let's see what patterns we can find in the data of the past Nobel laureates. What can we learn about the Nobel prize and our world more generally?

### Upgrade plotly (only Google Colab Notebook)

Google Colab may not be running the latest version of plotly. If you're working in Google Colab, uncomment the line below, run the cell, and restart your notebook server.
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install --upgrade plotly

"""### Import Statements"""

import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

"""### Notebook Presentation"""

pd.options.display.float_format = '{:,.2f}'.format

"""### Read the Data"""

df_data = pd.read_csv('nobel_prize_data.csv')

"""Caveats: The exact birth dates for Michael Houghton, Venkatraman Ramakrishnan, and Nadia Murad are unknown. I've substituted them with mid-year estimate of July 2nd.

# Data Exploration & Cleaning

**Challenge**: Preliminary data exploration. 
* What is the shape of `df_data`? How many rows and columns?
* What are the column names?
* In which year was the Nobel prize first awarded?
* Which year is the latest year included in the dataset?
"""

print(f'Shape: {df_data.shape}')
df_data.head()

df_data.describe()

"""**Challange**: 
* Are there any duplicate values in the dataset?
* Are there NaN values in the dataset?
* Which columns tend to have NaN values?
* How many NaN values are there per column? 
* Why do these columns have NaN values?

### Check for Duplicates
"""

print(f'Duplicated? {df_data.duplicated().values.any()}')
print(f"Double check: {df_data.duplicated(subset=['year', 'category', 'full_name']).values.any()}")

"""### Check for NaN Values"""

df_data.isna().values.any()

# Looks like duplicates, but the index number is the same
# When a row has multiple NaN values, it shows up as a separate row in the duplicates display
nan_rows = df_data[df_data.isna().values == True]
nan_rows.tail()

df_data.isna().sum()

# Her way of looking through more specifically at the NaNs: Only pulls results that have a NaN in one of the subset columns
# Since birth_date was included, and most organizations have a NaN for it, then it shows Organizations
col_subset = ['year','category', 'laureate_type',
              'birth_date','full_name', 'organization_name']
df_data.loc[df_data.birth_date.isna()][col_subset]

# Not looking for birth_date NaNs, so it changes the results to mostly people
col_subset = ['year','category', 'laureate_type','full_name', 'organization_name']
df_data.loc[df_data.organization_name.isna()][col_subset]

"""### Type Conversions

**Challenge**: 
* Convert the `birth_date` column to Pandas `Datetime` objects
* Add a Column called `share_pct` which has the laureates' share as a percentage in the form of a floating-point number.

#### Convert Year to Integer and Birth Date to Datetime
"""

df_data.year = pd.to_numeric(df_data.year)
df_data.birth_date = pd.to_datetime(df_data.birth_date)
df_data.info()

"""#### Add a Column with the Prize Share as a Percentage"""

df_data.prize_share.nunique()

share_percent = [int(row[0])/int(row[2]) for row in df_data.prize_share]
pd_col = pd.to_numeric(share_percent)
df_data['share_percent'] = pd_col
df_data.sample(10)

# Her Way:
# separated_values = df_data.prize_share.str.split('/', expand=True)
# print(separated_values)
# numerator = pd.to_numeric(separated_values[0])
# denomenator = pd.to_numeric(separated_values[1])
# df_data['share_pct'] = numerator / denomenator

"""# Plotly Donut Chart: Percentage of Male vs. Female Laureates

**Challenge**: Create a [donut chart using plotly](https://plotly.com/python/pie-charts/) which shows how many prizes went to men compared to how many prizes went to women. What percentage of all the prizes went to women?
"""

gender_split = df_data.sex.value_counts()
print(gender_split)

fig = px.pie(title="Gender Split of Nobel Prizes",
             names=gender_split.index, 
             labels=gender_split.index, 
             values=gender_split.values,
             hole=0.6)

fig.update_traces(textposition='inside', textfont_size=12, textinfo='percent+label')
fig.show()

"""# Who were the first 3 Women to Win the Nobel Prize?

**Challenge**: 
* What are the names of the first 3 female Nobel laureates? 
* What did the win the prize for? 
* What do you see in their `birth_country`? Were they part of an organisation?
"""

df_data[df_data.sex == 'Female'].head()

"""# Find the Repeat Winners

**Challenge**: Did some people get a Nobel Prize more than once? If so, who were they? 
"""

# Note: keep=False shows the original one, not just the duplicate row
repeat_winners = df_data[df_data.duplicated(subset='full_name', keep=False) == True]
display(repeat_winners)
# cleans up display
col_subset = ['year', 'category', 'laureate_type', 'full_name']
repeat_winners[col_subset]

# Her Way
is_winner = df_data.duplicated(subset=['full_name'], keep=False)
multiple_winners = df_data[is_winner]
print(f'There are {multiple_winners.full_name.nunique()}' \
      ' winners who were awarded the prize more than once.')

# Cleans up the output, fewer categories
col_subset = ['year', 'category', 'laureate_type', 'full_name']
multiple_winners[col_subset]

"""# Number of Prizes per Category

**Challenge**: 
* In how many categories are prizes awarded? 
* Create a plotly bar chart with the number of prizes awarded by category. 
* Use the color scale called `Aggrnyl` to colour the chart, but don't show a color axis.
* Which category has the most number of prizes awarded? 
* Which category has the fewest number of prizes awarded? 
"""

category_counts = df_data.category.value_counts()

# The _r at the end of the color scale is used to reverse the scale
fig = px.bar(x=category_counts.index, 
             y=category_counts.values,
             hover_name=category_counts.index,
             title="Nobel Prizes by Category",
             color=category_counts.values,
             color_continuous_scale='agsunset_r')
fig.show()

"""**Challenge**: 
* When was the first prize in the field of Economics awarded?
* Who did the prize go to?
"""

df_data[df_data.category == "Economics"]

"""# Male and Female Winners by Category

**Challenge**: Create a [plotly bar chart](https://plotly.com/python/bar-charts/) that shows the split between men and women by category. 
* Hover over the bar chart. How many prizes went to women in Literature compared to Physics?

<img src=https://i.imgur.com/od8TfOp.png width=650>
"""

gender_by_category = df_data.groupby(['category','sex'], as_index=False).agg({'prize':pd.Series.count})
gender_by_category.sort_values('prize', ascending=False, inplace=True)

# category order and above sorting helped to make the graph look that way (female on top, male on bottom)
fig = px.bar(gender_by_category, 
             x='category', 
             y='prize', 
             color='sex',
             title='Male vs Female Nobel Prizes by Category')

fig.update_xaxes(categoryorder='total descending')
fig.update_layout(xaxis_title='Category',
                  yaxis_title='Nobel Prizes Awarded')
fig.show()

"""# Number of Prizes Awarded Over Time

**Challenge**: Are more prizes awarded recently than when the prize was first created? Show the trend in awards visually. 
* Count the number of prizes awarded every year. 
* Create a 5 year rolling average of the number of prizes (Hint: see previous lessons analysing Google Trends).
* Using Matplotlib superimpose the rolling average on a scatter plot.
* Show a tick mark on the x-axis for every 5 years from 1900 to 2020. (Hint: you'll need to use NumPy). 

<img src=https://i.imgur.com/4jqYuWC.png width=650>

* Use the [named colours](https://matplotlib.org/3.1.0/gallery/color/named_colors.html) to draw the data points in `dogerblue` while the rolling average is coloured in `crimson`. 

<img src=https://i.imgur.com/u3RlcJn.png width=350>

* Looking at the chart, did the first and second world wars have an impact on the number of prizes being given out? 
* What could be the reason for the trend in the chart?

"""

# Don't always need to .agg after a .groupby. Can also call count() and then the column to count
# Her way:
time_series = df_data.groupby('year').count().prize
display(time_series)

# My way
time_series2 = df_data.groupby('year').agg({'prize':pd.Series.count})
display(time_series2)
# rolling_time_series = time_series.rolling(window=5).mean()

# # Year scale will be used below for the x-axis ticks
# year_scale = np.arange(1900, 2021, 5, )
# year_scale



# alpha=transparency, s=dot size

plt.figure(figsize=(12,7), dpi=200)

plt.xticks(year_scale,
           rotation=-45,
           fontsize=14)
plt.yticks(fontsize=14)


plt.scatter(x=time_series.index, 
            y=time_series, 
            color='dodgerblue',
            alpha=0.6,
            s=100)
plt.plot(time_series.index,
         rolling_time_series,
         color='crimson',
         linewidth=3)

plt.figure(figsize=(16,8), dpi=200)
plt.title('Nobel Prizes by Year\n',
          fontsize=22)
plt.xticks(year_scale,
           rotation=-45,
           fontsize=14)
plt.yticks(fontsize=14)

ax = plt.gca() # get current axis
ax.set_xlim(1900, 2022)

ax.scatter(x=time_series.index, 
            y=time_series, 
            color='dodgerblue',
            alpha=0.6,
            s=100)
ax.plot(time_series.index,
         rolling_time_series,
         color='crimson',
         linewidth=3)

"""# Are More Prizes Shared Than Before?

**Challenge**: Investigate if more prizes are shared than before. 

* Calculate the average prize share of the winners on a year by year basis.
* Calculate the 5 year rolling average of the percentage share.
* Copy-paste the cell from the chart you created above.
* Modify the code to add a secondary axis to your Matplotlib chart.
* Plot the rolling average of the prize share on this chart. 
* See if you can invert the secondary y-axis to make the relationship even more clear. 
"""

prize_sharing = df_data.groupby('year').agg({'share_percent':pd.Series.mean})
rolling_prize_sharing = prize_sharing.rolling(window=5).mean()

plt.figure(figsize=(16,8), dpi=200)
plt.title('Nobel Prizes by Year\n',
          fontsize=22)
plt.xticks(year_scale,
           rotation=-45,
           fontsize=14)
plt.yticks(fontsize=14)

ax = plt.gca() # get current axis
ax.set_xlim(1900, 2022)

ax.scatter(x=time_series.index, 
            y=time_series, 
            color='dodgerblue',
            alpha=0.6,
            s=100)
ax.plot(time_series.index,
         rolling_time_series,
         color='crimson',
         linewidth=3)

ax2 = ax.twinx() # copies x-axis, allows us to have different y axis

ax2.plot(prize_sharing.index,
         rolling_prize_sharing,
         c='grey',
         linewidth=3)

# Graph above shows an obvious relationship between number of awards given out and the share percentage.
# Let's invert the axis for the share graph to match the lines up better (less to more awards, less to more sharing)
plt.figure(figsize=(16,8), dpi=200)
plt.title('Nobel Prizes by Year\n',
          fontsize=22)
plt.xticks(year_scale,
           rotation=-45,
           fontsize=14)
plt.yticks(fontsize=14)

ax = plt.gca() # get current axis
ax.set_xlim(1900, 2022)

ax.scatter(x=time_series.index, 
            y=time_series, 
            color='dodgerblue',
            alpha=0.6,
            s=100)
ax.plot(time_series.index,
         rolling_time_series,
         color='crimson',
         linewidth=3)

ax2 = ax.twinx() 
ax2.invert_yaxis() # Inverts the share percent axis, making it congruent with the award number axis

ax2.plot(prize_sharing.index,
         rolling_prize_sharing,
         c='grey',
         linewidth=3)

"""# The Countries with the Most Nobel Prizes

**Challenge**: 
* Create a Pandas DataFrame called `top20_countries` that has the two columns. The `prize` column should contain the total number of prizes won. 

<img src=https://i.imgur.com/6HM8rfB.png width=350>

* Is it best to use `birth_country`, `birth_country_current` or `organization_country`? 
* What are some potential problems when using `birth_country` or any of the others? Which column is the least problematic? 
* Then use plotly to create a horizontal bar chart showing the number of prizes won by each country. Here's what you're after:

<img src=https://i.imgur.com/agcJdRS.png width=750>

* What is the ranking for the top 20 countries in terms of the number of prizes?
"""

df_data.info()

list = ['birth_country', 'birth_country_current', 'organization_country']
for country in list:
  print(df_data.groupby(country).agg({'prize':pd.Series.count}))

organizations = df_data[df_data.laureate_type == 'Organization']
organizations.shape

organizations

# birth_country has too many multiples and weird data (europe changing nations, etc.)
# organization_country ironically is only filled in for individuals!
# birth_country_current is the Goldilocks

top_20_countries = df_data.groupby('birth_country_current', as_index=False).agg({'prize':pd.Series.count})
top_20_countries.sort_values('prize', ascending=False, inplace=True)
top_20_countries = top_20_countries[:20]
top_20_countries

# Had to reverse y-axis to get it like hers (since the [-20:] is ugly)
fig = px.bar(top_20_countries,
             orientation='h',
             y='birth_country_current',
             x='prize')
fig.update_yaxes(autorange="reversed")
fig.show()

"""# Use a Choropleth Map to Show the Number of Prizes Won by Country

* Create this choropleth map using [the plotly documentation](https://plotly.com/python/choropleth-maps/):

<img src=https://i.imgur.com/s4lqYZH.png>

* Experiment with [plotly's available colours](https://plotly.com/python/builtin-colorscales/). I quite like the sequential colour `matter` on this map. 

Hint: You'll need to use a 3 letter country code for each country. 

"""

countries = df_data.groupby('birth_country_current', as_index=False).agg({'prize':pd.Series.count,'ISO':pd.Series.unique})
countries.sort_values('prize', ascending=False)

# Must pass in an ISO for locations in order to work with this ready loaded world map choropleth
fig = px.choropleth(countries, locations="ISO",
                    color="prize",
                    hover_name="birth_country_current",
                    color_continuous_scale=px.colors.sequential.YlGn)
fig.show()

# Her Way:
df_countries = df_data.groupby(['birth_country_current', 'ISO'], 
                               as_index=False).agg({'prize': pd.Series.count})
df_countries.sort_values('prize', ascending=False)

world_map = px.choropleth(df_countries,
                          locations='ISO',
                          color='prize', 
                          hover_name='birth_country_current', 
                          color_continuous_scale=px.colors.sequential.matter)
 
world_map.update_layout(coloraxis_showscale=True,)
 
world_map.show()

"""# In Which Categories are the Different Countries Winning Prizes? 

**Challenge**: See if you can divide up the plotly bar chart you created above to show the which categories made up the total number of prizes. Here's what you're aiming for:

<img src=https://i.imgur.com/iGaIKCL.png>

* In which category are Germany and Japan the weakest compared to the United States?
* In which category does Germany have more prizes than the UK?
* In which categories does France have more prizes than Germany?
* Which category makes up most of Australia's nobel prizes?
* Which category makes up half of the prizes in the Netherlands?
* Does the United States have more prizes in Economics than all of France? What about in Physics or Medicine?


The hard part is preparing the data for this chart! 


*Hint*: Take a two-step approach. The first step is grouping the data by country and category. Then you can create a DataFrame that looks something like this:

<img src=https://i.imgur.com/VKjzKa1.png width=450>

"""

# My way without the hint, doing it in one step
# Problem is this only has the category counts, not the total country counts, so the graph isn't sorted/ordered properly
detailed_country = df_data.groupby(['birth_country_current','category'], as_index=False).agg({'prize':pd.Series.count})
detailed_country.sort_values('prize', ascending=False, inplace=True)

fig = px.bar(detailed_country,
             orientation='h',
             y='birth_country_current',
             x='prize',
             color='category',
             width=1400,
             height=800,)
fig.update_yaxes(range=[-1,20])

fig.show()

# My way, with hint, the two step process:
# narrow it down to 20 countries here, since category df will have multiple rows for a single country, harder to slice
total_prize_country = df_data.groupby('birth_country_current', as_index=False).agg({'prize':pd.Series.count})
total_prize_country = total_prize_country.sort_values('prize')[-20:]

category_prize_country = df_data.groupby(['birth_country_current','category'], as_index=False).agg({'prize':pd.Series.count})

# Even with different amount of rows, can still merge on the country column
# Each table had a column named 'prize', so they got auto-renamed to prize_x and prize_y
# Order matters for merging. I used the total prize df first, my columns got split. She did the reverse, came out neater
df_merged = pd.merge(total_prize_country, category_prize_country, on='birth_country_current')
df_merged.rename(columns={"prize_x": "total_prize", "prize_y": "category_prize"}, inplace=True)

df_merged

# Just for aethestics, make the column order better:
new_cols = ["birth_country_current","category","category_prize","total_prize"]
df_merged = df_merged[new_cols]
#or
# df_merged = df_merged.reindex(columns=new_cols)
df_merged

# arranging it above through proper ascending/sorted, no need for the reversing of the yaxis or window parameters
fig = px.bar(df_merged,
             orientation='h',
             y='birth_country_current',
             x='category_prize',
             color='category'
            #  width=1400,
            #  height=600,
            )
# fig.update_yaxes(autorange='reversed')

fig.show()

# Her Way:
top_countries = df_data.groupby(['birth_country_current'], 
                                  as_index=False).agg({'prize': pd.Series.count})
 
top_countries.sort_values(by='prize', inplace=True)
top20_countries = top_countries[-20:]

# Her Way:
cat_country = df_data.groupby(['birth_country_current', 'category'], 
                               as_index=False).agg({'prize': pd.Series.count})
cat_country.sort_values(by='prize', ascending=False, inplace=True)
merged_df = pd.merge(cat_country, top20_countries, on='birth_country_current')
display(merged_df)
# Note: order matter with merging df in terms of column placement
# change column names
merged_df.columns = ['birth_country_current', 'category', 'cat_prize', 'total_prize'] 
merged_df.sort_values(by='total_prize', inplace=True)

# Her Way:
cat_cntry_bar = px.bar(x=merged_df.cat_prize,
                       y=merged_df.birth_country_current,
                       color=merged_df.category,
                       orientation='h',
                       title='Top 20 Countries by Number of Prizes and Category')
 
cat_cntry_bar.update_layout(xaxis_title='Number of Prizes', 
                            yaxis_title='Country')
cat_cntry_bar.show()

"""### Number of Prizes Won by Each Country Over Time

* When did the United States eclipse every other country in terms of the number of prizes won? 
* Which country or countries were leading previously?
* Calculate the cumulative number of prizes won by each country in every year. Again, use the `birth_country_current` of the winner to calculate this. 
* Create a [plotly line chart](https://plotly.com/python/line-charts/) where each country is a coloured line. 
"""

df_data.info()

# Since year and share_percent are the only numeric Series, running .cumsum() on the df_data can only total those, not prizes.
df_data.groupby(['birth_country_current']).cumsum()

# First need to count the prizes, turning it into a numeric, then can run .cumsum() on it.
year_country_total = df_data.groupby(['year','birth_country_current'], as_index=False).agg({'prize':pd.Series.count})
year_country_total

# Help from google: df[['Type', 'Sales']].groupby('Type').cumsum(), had to modify it
# This .cumsum() works since the table it already ordered by year, ascending from earliest
cumulative = year_country_total.groupby(['birth_country_current']).cumsum()
display(cumulative)

# Note: cumsum() added up the years too, but we don't care. Just pull the 'prize' info out and add it to the previous table
year_country_total['cumulative_prize'] = cumulative['prize']

year_country_total

fig = px.line(year_country_total,
              x='year',
              y='cumulative_prize',
              color='birth_country_current',
              hover_name='birth_country_current')

fig.update_layout(xaxis_title='Year',
                  yaxis_title='Number of Prizes')
fig.show()

# Her Way:
# what is going on with cumulative_prizes! lol, double groupby with sum() and cumsum(), then need to reset index! Crazy stuff

# She is turning the prizes into a numeric by counting after grouping. By not specifying an .agg({'prize'}), it counts everything!
prize_by_year = df_data.groupby(by=['birth_country_current', 'year'], as_index=False).count()
prize_by_year = prize_by_year.sort_values('year')
display(prize_by_year)
# Sorts it by year and narrows down the columns (since it counted all the columns earlier)
prize_by_year = prize_by_year.sort_values('year')[['year', 'birth_country_current', 'prize']]
display(prize_by_year)

# grouping and .sum make it so the countries are the main group, subgroup is years, and the the prizes for the years
cumulative_prizes1 = prize_by_year.groupby(by=['birth_country_current','year']).sum()
display(cumulative_prizes1)
print("\n-----\n")
# By adding the second groupby, and specifying the level as [0], which is the first column (the country), nonw she can do .cumsum()
cumulative_prizes = prize_by_year.groupby(by=['birth_country_current','year']).sum().groupby(level=[0]).cumsum()
display(cumulative_prizes)
# Her method of grouping left the table without an index; this adds it back
cumulative_prizes.reset_index(inplace=True) 
display(cumulative_prizes)

l_chart = px.line(cumulative_prizes,
                  x='year', 
                  y='prize',
                  color='birth_country_current',
                  hover_name='birth_country_current')
 
l_chart.update_layout(xaxis_title='Year',
                      yaxis_title='Number of Prizes')
 
l_chart.show()

# Note her legend is alphabetized, which doesn't match the graphs! The top 5 aren't even on the list!!

# For once, I think my method and results were better!! :D

"""# What are the Top Research Organisations?

**Challenge**: Create a bar chart showing the organisations affiliated with the Nobel laureates. It should looks something like this:

<img src=https://i.imgur.com/zZihj2p.png width=600>

* Which organisations make up the top 20?
* How many Nobel prize winners are affiliated with the University of Chicago and Harvard University?
"""

df_data.isna().sum()

# Note: 255 missing values for 'organization_name'!!! Definitely affects the data
organization_total = df_data.groupby('organization_name', as_index=False).agg({'prize':pd.Series.count})
top_20_organizations = organization_total.sort_values('prize')[-20:]

fig = px.bar(top_20_organizations,
             x='prize',
             y='organization_name',
             orientation='h',
             color='prize',
             title='Nobel Prizes by Institution',
             hover_name='organization_name')
fig.update_layout(xaxis_title='Number of Prizes',
                  yaxis_title='Institution')

fig.show()

# Her Way:
top20_orgs = df_data.organization_name.value_counts()[:20]
print(top20_orgs)
top20_orgs.sort_values(ascending=True, inplace=True)

org_bar = px.bar(x = top20_orgs.values,
                 y = top20_orgs.index,
                 orientation='h',
                 color=top20_orgs.values,
                 color_continuous_scale=px.colors.sequential.haline_r,
                 title='Top 20 Research Institutions by Number of Prizes')
 
org_bar.update_layout(xaxis_title='Number of Prizes', 
                      yaxis_title='Institution',
                      coloraxis_showscale=False)
org_bar.show()

"""# Which Cities Make the Most Discoveries? 

Where do major discoveries take place?  

**Challenge**: 
* Create another plotly bar chart graphing the top 20 organisation cities of the research institutions associated with a Nobel laureate. 
* Where is the number one hotspot for discoveries in the world?
* Which city in Europe has had the most discoveries?
"""

# Don't need to make an agg, can just use the value_counts() like she did above
# NOTE: sort_values doesn't need a input if there is only one column to sort
top_20_cities = df_data.organization_city.value_counts()[:20]
top_20_cities.sort_values(ascending=True, inplace=True)

city_bar = px.bar(x = top_20_cities.values,
                 y = top_20_cities.index,
                 orientation='h',
                 color=top_20_cities.values,
                 color_continuous_scale=px.colors.sequential.haline_r,
                 title='Top 20 Research Cities by Number of Prizes')
 
city_bar.update_layout(xaxis_title='Number of Prizes', 
                      yaxis_title='City',
                      coloraxis_showscale=False)
city_bar.show()

"""# Where are Nobel Laureates Born? Chart the Laureate Birth Cities 

**Challenge**: 
* Create a plotly bar chart graphing the top 20 birth cities of Nobel laureates. 
* Use a named colour scale called `Plasma` for the chart.
* What percentage of the United States prizes came from Nobel laureates born in New York? 
* How many Nobel laureates were born in London, Paris and Vienna? 
* Out of the top 5 cities, how many are in the United States?

"""

top_birth_cities = df_data.birth_city.value_counts()[:20]
top_birth_cities.sort_values(ascending=True, inplace=True)

city_bar = px.bar(x = top_birth_cities.values,
                 y = top_birth_cities.index,
                 orientation='h',
                 color=top_birth_cities.values,
                 color_continuous_scale=px.colors.sequential.matter,
                 title='Where were the Nobel Laureates born?')
 
city_bar.update_layout(xaxis_title='Number of Prizes', 
                      yaxis_title='Birth City',
                      coloraxis_showscale=False)
city_bar.show()

"""# Plotly Sunburst Chart: Combine Country, City, and Organisation

**Challenge**: 

* Create a DataFrame that groups the number of prizes by organisation. 
* Then use the [plotly documentation to create a sunburst chart](https://plotly.com/python/sunburst-charts/)
* Click around in your chart, what do you notice about Germany and France? 


Here's what you're aiming for:

<img src=https://i.imgur.com/cemX4m5.png width=300>


"""

# Changing from birth_country_current to organization_country doesn't change number of prizes, even tho many NaN in org_country
# Number of rows is very different tho!
# Data changes because the award gets credited to the country they were born in, not the country they conducted the research

df_sunburst = df_data.groupby(['birth_country_current', 'organization_city', 'organization_name'], as_index=False).agg({'prize':pd.Series.count})
display(df_sunburst.prize.sum())
df_sunburst

df_sunburst.sample(49)

fig = px.sunburst(df_sunburst,
                  path=['birth_country_current', 'organization_city', 'organization_name'],
                  values='prize',
                  title='Where do Discoveries Take Place?'
                   )
 
fig.update_layout(xaxis_title='Number of Prizes', 
                    yaxis_title='City',
                    coloraxis_showscale=False)
fig.show()

df_sunburst1 = df_data.groupby(['organization_country', 'organization_city', 'organization_name'], as_index=False).agg({'prize':pd.Series.count})
display(df_sunburst1.prize.sum())
df_sunburst1

df_sunburst1.sample(49)

fig = px.sunburst1(df_sunburst1,
                  path=['organization_country', 'organization_city', 'organization_name'],
                  values='prize',
                  title='Where do Discoveries Take Place?'
                   )
 
fig.update_layout(xaxis_title='Number of Prizes', 
                    yaxis_title='City',
                    coloraxis_showscale=False)
fig.show()

# Super cool graphic, you can click on the center choices and it expands!
# The graph changes depending on the groupby (organization_country instead of birth_country_current)
# There were plenty of NaN in the category, so not sure how the totals are accurate.
# TBH, the data set isn't very clean - some areas filled out, some not. Hard to agg

"""# Patterns in the Laureate Age at the Time of the Award

How Old Are the Laureates When the Win the Prize?

**Challenge**: Calculate the age of the laureate in the year of the ceremony and add this as a column called `winning_age` to the `df_data` DataFrame. Hint: you can use [this](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.html) to help you. 


"""

df_data.birth_date.dt.year

df_data['laureate_age'] = (df_data.year - df_data.birth_date.dt.year)

# df_merged.rename(columns={"prize_x": "total_prize", "prize_y": "category_prize"}, inplace=True)
df_data.rename(columns={'laureate_age':'winning_age'}, inplace=True)

"""### Who were the oldest and youngest winners?

**Challenge**: 
* What are the names of the youngest and oldest Nobel laureate? 
* What did they win the prize for?
* What is the average age of a winner?
* 75% of laureates are younger than what age when they receive the prize?
* Use Seaborn to [create histogram](https://seaborn.pydata.org/generated/seaborn.histplot.html) to visualise the distribution of laureate age at the time of winning. Experiment with the number of `bins` to see how the visualisation changes.
"""

# Note: .loc needs a double [[]] if calling something from a df
# Oldest Laureate:
display(df_data.loc[[df_data.winning_age.idxmax()]])
# Youngest Laureate
display(df_data.loc[[df_data.winning_age.idxmin()]])

"""### Descriptive Statistics for the Laureate Age at Time of Award

* Calculate the descriptive statistics for the age at the time of the award. 
* Then visualise the distribution in the form of a histogram using [Seaborn's .histplot() function](https://seaborn.pydata.org/generated/seaborn.histplot.html).
* Experiment with the `bin` size. Try 10, 20, 30, and 50.  
"""

df_data.winning_age

# Some NaN since birth_dates weren't filled in (organizations?)
df_data.winning_age.describe()

# Didn't need this as Seaborn Histplot already counts for us
prize_by_age = df_data.winning_age.value_counts()
prize_by_age

# Higher bins means more granular = smaller range in age for a single bar
sns.histplot(df_data.winning_age,
             bins=50
            )

# Her way:
plt.figure(figsize=(8, 4), dpi=200)
sns.histplot(data=df_data,
             x=df_data.winning_age,
             bins=30)
plt.xlabel('Age')
plt.title('Distribution of Age on Receipt of Prize')
plt.show()

"""### Age at Time of Award throughout History

Are Nobel laureates being nominated later in life than before? Have the ages of laureates at the time of the award increased or decreased over time?

**Challenge**

* Use Seaborn to [create a .regplot](https://seaborn.pydata.org/generated/seaborn.regplot.html?highlight=regplot#seaborn.regplot) with a trendline.
* Set the `lowess` parameter to `True` to show a moving average of the linear fit.
* According to the best fit line, how old were Nobel laureates in the years 1900-1940 when they were awarded the prize?
* According to the best fit line, what age would it predict for a Nobel laureate in 2020?

"""

avg_age_yearly = df_data.groupby('year', as_index=False).agg({'winning_age':pd.Series.mean})
avg_age_yearly

fig = px.scatter(avg_age_yearly,
                 x='year',
                 y='winning_age')
fig.show()

# Trend looks upward, but difficult to tell exactly
# Let's get a regression line

sns.regplot(data=avg_age_yearly,
            x='year',
            y='winning_age')

# Lowess = Locally Weighted Linear Regression
sns.regplot(data=avg_age_yearly,
            x='year',
            y='winning_age',
            lowess=True)

# Her Way:
# Note: She uses the original dataset, no need to create a mean() Series like I did above
plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.regplot(data=df_data,
                x='year',
                y='winning_age',
                lowess=True, 
                scatter_kws = {'alpha': 0.4},
                line_kws={'color': 'black'})
 
plt.show()

"""### Winning Age Across the Nobel Prize Categories

How does the age of laureates vary by category? 

* Use Seaborn's [`.boxplot()`](https://seaborn.pydata.org/generated/seaborn.boxplot.html?highlight=boxplot#seaborn.boxplot) to show how the mean, quartiles, max, and minimum values vary across categories. Which category has the longest "whiskers"? 
* In which prize category are the average winners the oldest?
* In which prize category are the average winners the youngest?
"""

plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.boxplot(data=df_data,
                x='category',
                y='winning_age'
                )

plt.show()

"""**Challenge**
* Now use Seaborn's [`.lmplot()`](https://seaborn.pydata.org/generated/seaborn.lmplot.html?highlight=lmplot#seaborn.lmplot) and the `row` parameter to create 6 separate charts for each prize category. Again set `lowess` to `True`.
* What are the winning age trends in each category? 
* Which category has the age trending up and which category has the age trending down? 
* Is this `.lmplot()` telling a different story from the `.boxplot()`?
* Create another chart with Seaborn. This time use `.lmplot()` to put all 6 categories on the same chart using the `hue` parameter. 

"""

# Using the 'row' split
# NOTE: figure(figsize) doesn't work here. Need to use 'aspect' to make it larger

# plt.figure(figsize=(8,4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.lmplot(data=df_data,
                x='year',
                y='winning_age',
               lowess=True,
               row='category',
               aspect=2.2,
               scatter_kws = {'alpha': 0.6},
               line_kws = {'color': 'black'})
plt.show()

# Using the 'col' split
# Smaller aspect since they are all in a line
with sns.axes_style("whitegrid"):
    sns.lmplot(data=df_data,
                x='year',
                y='winning_age',
               lowess=True,
               col='category',
               aspect=1,
               scatter_kws = {'alpha': 0.6},
               line_kws = {'color': 'black'})
plt.show()

# Using the 'hue' split
# Here we don't want to change the regression line color since it tells us which is which, but rather increase linewidth
with sns.axes_style("whitegrid"):
    sns.lmplot(data=df_data,
                x='year',
                y='winning_age',
               lowess=True,
               hue='category',
               aspect=2.2,
               scatter_kws = {'alpha': 0.5},
               line_kws={'linewidth': 5})
              #  line_kws = {'color': 'black'})
plt.show()

# THE END!!! Wow, this assignment was packed!