# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 14:57:42 2023

@author: ADHWA' QAYYUM
"""


from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By

def get_jobs( keyword, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = "https://www.glassdoor.com/Job/united-states-"+keyword+"-jobs-SRCH_IL.0,13_IN1_KO14,28.htm?sortBy=date_desc"
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element(By.CLASS_NAME,"selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(0.1)

        try:
            driver.find_element(By.CSS_SELECTOR,'[alt="Close"]').click() #clicking to the X.
            print(' x out worked')
        except NoSuchElementException:
            print(' x out failed')
            pass
        
        
        #Going through each job in this page
        job_buttons = driver.find_elements(By.XPATH,'.//a[@data-test="job-link"]')  #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            time.sleep(0.3)
            collected_successfully = False
            
            
            while not collected_successfully:    

                try:
                    company_name = driver.find_element(By.XPATH,'.//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]').text
                    location = driver.find_element(By.XPATH,'.//div[@data-test="location"]').text
                    job_title = driver.find_element(By.XPATH,'.//div[(@data-test="jobTitle")]').text
                    job_description = driver.find_element(By.XPATH,'.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element(By.XPATH,'.//span[@data-test="detailSalary"]').text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
                
            try:
                rating = driver.find_element(By.XPATH,'.//span[@data-test="detailRating"]').text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."

            
            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div/div[2]/section/div/div/article/div/div[2]/div[1]/div[3]/div').click()
               
                try:
                    #<div class="infoEntity">
                    #    <label>Headquarters</label>
                    #    <span class="value">San Francisco, CA</span>
                    #</div>
                    company_size = driver.find_element(By.XPATH,'.//*[@id="EmpBasicInfo"]/div[1]/div/div[1]/span[2]').text
                except NoSuchElementException:
                    company_size = -1
                
                try:
                    company_founded = driver.find_element(By.XPATH,'.//*[@id="EmpBasicInfo"]/div[1]/div/div[2]/span[2]').text
                except NoSuchElementException:
                    company_founded = -1
                
                try:
                    company_type = driver.find_element(By.XPATH,'.//*[@id="EmpBasicInfo"]/div[1]/div/div[3]/span[2]').text
                except NoSuchElementException:
                    company_type = -1
                
                try:
                    company_industry = driver.find_element(By.XPATH,'.//*[@id="EmpBasicInfo"]/div[1]/div/div[4]/span[2]').text
                except NoSuchElementException:
                    company_industry = -1
                
                try:
                    company_sector = driver.find_element(By.XPATH,'.//*[@id="EmpBasicInfo"]/div[1]/div/div[5]/span[2]').text
                except NoSuchElementException:
                    company_sector = -1
                
                try:
                    company_revenue = driver.find_element(By.XPATH,'.//*[@id="EmpBasicInfo"]/div[1]/div/div[6]/span[2]').text
                except NoSuchElementException:
                    company_revenue = -1
                
                    
            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                        company_size = -1
            except NoSuchElementException:
                        company_founded = -1
            except NoSuchElementException:
                        company_type = -1
            except NoSuchElementException:
                        company_industry = -1
            except NoSuchElementException:
                        company_sector = -1
            except NoSuchElementException:
                        company_revenue = -1
                
                        
            if verbose:
                print("Size: {}".format(company_size))
                print("Founded: {}".format(company_founded))
                print("Type: {}".format(company_type))
                print("Industry: {}".format(company_industry))
                print("Sector: {}".format(company_sector))
                print("Revenue: {}".format(company_revenue))
                
            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Size" : company_size,
            "Founded" : company_founded,
            "Type" : company_type,
            "Industry" : company_industry,
            "Sector" : company_sector,
            "Revenue" : company_revenue})

            
            
        #Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH,'.//button[@aria-label="Next"]').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
