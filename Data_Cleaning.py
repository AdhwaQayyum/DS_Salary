# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 02:12:56 2023

@author: ADHWA' QAYYUM
"""

import pandas as pd

df= pd.read_csv('glassdoor_jobs.csv')

#Salary Parsing

#Create new column and Find if there is salary 'per hour' or 'employer provided' in the dataset
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)


#Overwrite dataframe with only Datasets that containing the salary estimate (Taking from column 'Salary Estimate')
df = df[df['Salary Estimate'] !='-1']
#Create new dataframe named 'salary' to take only the value from column 'Salary Estimate'. zero in the end to take left side of the split
salary = df['Salary Estimate'].apply(lambda x: x.split('(') [0])
#Remove the 'k' and '$' sign
salary_minus_units = salary.apply(lambda x: x.replace('K','').replace('$',''))
#remove the the wording of 'hourly' and 'employer provided salary:'
minus_hourly_eps = salary_minus_units.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

#Seperate minimum and maximum salary (create new column in original dataframe, value getting from the minus_hourly_eps)
df['min_salary']= minus_hourly_eps.apply(lambda x: int(x.split('-')[0]))
df['max_salary']= minus_hourly_eps.apply(lambda x: int(x.split('-')[1]))
#Create column on average salary
df['avg_salary']= (df.min_salary + df.max_salary)/2

#Salary Standardization
#Change hourly wage to annual wage
#Context: 2000 = 8hrs/day * 5 days/week * 50 weeks.  The year has 52 weeks but 2 of those weeks are assigned to holidays and vacation time.
#let hourly salary= 10. thus, 10 x 8 x 5 x 50 = 20,000. Technically will multiply by 2
df['min_salary']= df.apply(lambda x: x.min_salary*2 if x.hourly ==1 else x.min_salary, axis=1)
df['max_salary']= df.apply(lambda x: x.max_salary*2 if x.hourly ==1 else x.max_salary, axis=1)


#Taking company name only

#by only remove last 3 text (axis =1 because we didn't specify the series,,, and 1 indicate the row)
df['Company_text']= df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis = 1)

#State field
df['job_state']= df['Location'].apply(lambda x: x.split(',')[1])
df.job_state.value_counts()

#If the location and headquarters are in the same place =1 else 0
df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)

#Age of the company
df['age']= df.Founded.apply(lambda x: x if x <1 else 2023-x)

#Parsing of job description

#python
df['python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
#r studio 
df['R_language'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df.R_language.value_counts()
#spark
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark.value_counts()
#aws 
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws.value_counts()
#excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.excel.value_counts()
#SQL
df['SQL'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)
df.excel.value_counts()

def title_simplifier(title):
    if 'data scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'analyst'
    elif 'machine learning' in title.lower():
        return 'mle'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'na'
    
def seniority(title):
    if 'sr' in title.lower() or 'senior' in title.lower() or 'sr' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
            return 'senior'
    elif 'jr' in title.lower() or 'jr.' in title.lower():
        return 'jr'
    else:
        return 'na'

df['job_simplified'] = df['Job Title'].apply(title_simplifier)

df.job_simplified.value_counts()

df['seniority'] = df['Job Title'].apply(seniority)
df.seniority.value_counts()

# Fix state Los Angeles (x.strip remove spaces)
df['job_state']= df.job_state.apply(lambda x: x.strip() if x.strip().lower() != 'los angeles' else 'CA')
df.job_state.value_counts()


#  Job description length 
df['desc_len'] = df['Job Description'].apply(lambda x: len(x))
df['desc_len']

#Competitor count
df['num_comp'] = df['Competitors'].apply(lambda x: len(x.split(',')) if x != '-1' else 0)
df['num_comp']




df_out = df.drop(['Unnamed: 0'], axis =1)

df_out.to_csv('salary_data_cleaned.csv',index = False)







