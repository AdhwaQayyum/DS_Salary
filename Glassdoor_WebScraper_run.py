# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 13:18:14 2023

@author: ADHWA' QAYYUM
"""

import Glassdoor_WebScraper as gs 
import pandas as pd 

path = "C:/Users/ADHWA' QAYYUM/Documents/DS_Project_Salary/chromedriver"

df = gs.get_jobs('Data Scientist',5, False, path, 2)


df.to_csv('Raw_glassdoor_US_jobs.csv', index = False)