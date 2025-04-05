import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
'''- For each file you extract save it in `.csv` format with a header to the `cache` folder. The basic process is to read the file, add lineage, then write as a `.csv` to the `cache` folder. 
- Extract the states with codes google sheet. Save as `cache/states.csv`
- Extract the survey google sheet, and engineer a `year` column from the `Timestamp` using the `extract_year_mdy` function in `pandaslib.py`. Then save as `cache/survey.csv`
- For each unique year in the surveys: extract the cost of living for that year from the website, engineer a `year` column for that year, then save as `cache/col_{year}.csv` for example for `2024` it would be `cache/col_2024.csv`'''
#TODO Write your extraction code here

#load income data
st.write("raw income data")
base = "https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv"
survey = pd.read_csv(base)
survey['year'] = survey['Timestamp'].apply(pl.extract_year_mdy)
# save to cache
survey.to_csv('cache/survey.csv', index=False)
#getting every unique year in survey data
years = survey["year"].unique()
#display years for double checking
st.write("years")
st.write(years)
for year in years:
    #get cost of living data for each year
    income = f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0"
    col_year = col_year[1]
    # add year col
    col_year['year'] = year
    # save the data to a csv file in the cache
    col_year.to_csv(f'cache/col_{year}.csv', index=False)

#load state data
st.write("raw state data")
base = "https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv"
state_df = pd.read_csv(base)
#stores in the cache
state_table.to_csv('cache/states.csv', index=False)
#try to display the first 10 rows of the state data
st.write(state_df.head(10))

#three things stores in the cache now: survey data, cost of living data, and state data
