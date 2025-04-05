import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here
#load in state data and survey data as dataframes
states_data = pd.read_csv('cache/states.csv')
survey_data = pd.read_csv('cache/survey.csv')

#make a list of unique years from the survey data
u_years = survey_data["year"].unique()
#attach the col data to the list of unique years
#col_data = pd.read_csv(f'cache/col_{year}.csv')

# load col data from cache
cols = []
for year in u_years:
    col = pd.read_csv(f'cache/col_{year}.csv')
    cols.append(col)

#combine all col data into one dataframe
col_data = pd.concat(cols, ignore_index=True)

#clean the country column
survey_data['_country'] = survey_data['What country do you work in?'].apply(pl.clean_country_usa)

#changing state format to abbreviation
survey_states_combined = survey_data.merge(states_data, left_on = " If you're in the U.S., what state do you work in?", right_on = 'State', how = 'inner')

#new column for full city
survey_states_combined['_full_city'] = survey_states_combined['What city do you work in?'] + ', ' + survey_states_combined['Abbreviation'] + ', ' + survey_states_combined['_country']

#merge the survey data with the col data
combined = survey_states_combined.merge(col_data, left_on=['year', '_full_city'], right_on=['year', 'City'], how='inner')

#normalizing the annual salary based on cost of living
combined["_annual_salary_cleaned"] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency)

combined['_annual_salary_adjusted'] = combined.apply(lambda row: row["_annual_salary_cleaned"] * (100 / row['Cost of Living Index']), axis=1)

#new csv file for combined data
combined.to_csv('cache/survey_dataset.csv', index=False)

#reporting the data w streamlit
#annual salary adjusted for location and age
annual_salary_adjusted_by_location_and_age = combined.pivot_table(index='_full_city', columns='How old are you?', values='_annual_salary_adjusted', aggfunc='mean')
annual_salary_adjusted_by_location_and_age.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')
st.write(annual_salary_adjusted_by_location_and_age)

#annual salary adjusted for location and education
annual_salary_adjusted_by_location_and_education = combined.pivot_table(index='_full_city', columns='What is your highest level of education completed?', values='_annual_salary_adjusted', aggfunc='mean')
annual_salary_adjusted_by_location_and_age.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')
st.write(annual_salary_adjusted_by_location_and_education)
