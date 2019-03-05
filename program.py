import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time


URL = "https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=10"
page = requests.get(URL)
soup = BeautifulSoup(page.text, "html.parser")
print(soup.prettify())



def extract_job_title_from_result(soup): 
  jobs = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
      for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
        jobs.append(a["title"])
  return(jobs)
extract_job_title_from_result(soup)



def extract_company_from_result(soup): 
  companies = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    company = div.find_all(name="span", attrs={"class":"company"})
    if len(company) > 0:
      for b in company:
        companies.append(b.text.strip())
    else:
      sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
      for span in sec_try:
          companies.append(span.text.strip())
  return(companies)
extract_company_from_result(soup)



def extract_location_from_result(soup): 
  locations = []
  spans = soup.findAll('span', attrs={'class': 'location'})
  for span in spans:
    locations.append(span.text)
  return(locations)
extract_location_from_result(soup)




def extract_salary_from_result(soup): 
  salaries = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    try:
      salaries.append(div.find('nobr').text)
    except:
      try:
        div_two = div.find(name="div", attrs={"class":"sjcl"})
        div_three = div_two.find("div")
        salaries.append(div_three.text.strip())
      except:
        salaries.append("Nothing_found")
  return(salaries)
extract_salary_from_result(soup)



def extract_summary_from_result(soup): 
  summaries = []
  spans = soup.findAll('span', attrs={'class': 'summary'})
  for span in spans:
    summaries.append(span.text.strip())
  return(summaries)
extract_summary_from_result(soup)



max_results_per_city = 1000
city_set = ['New+York','Chicago','San+Francisco', 'Austin', 'Seattle', 'Los+Angeles', 'Philadelphia', 'Atlanta', 'Dallas', 'Pittsburgh', 'Portland', 'Phoenix', 'Denver', 'Houston', 'Miami', 'Washington+DC', 'Boulder']
columns = ["city", "job_title", "company_name", "location", "summary", "salary"]
sample_df = pd.DataFrame(columns = columns)



for city in city_set:
  for start in range(0, max_results_per_city, 10):
    page = requests.get('http://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=' + str(city) + '&start=' + str(start))
  time.sleep(1)  #ensuring at least 1 second between page grabs
  soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
  for div in soup.find_all(name="div", attrs={"class":"row"}): 
    num = (len(sample_df) + 1) 
    job_post = [] 
    job_post.append(city) 
    for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
      job_post.append(a["title"]) 
    company = div.find_all(name="span", attrs={"class":"company"}) 
    if len(company) > 0: 
      for b in company:
        job_post.append(b.text.strip()) 
    else: 
      sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
      for span in sec_try:
        job_post.append(span.text) 
    c = div.findAll('span', attrs={'class': 'location'}) 
    for span in c: 
      job_post.append(span.text) 
    d = div.findAll('span', attrs={'class': 'summary'}) 
    for span in d:
        job_post.append(span.text.strip()) 
    try:
      job_post.append(div.find('nobr').text) 
    except:
      try:
        div_two = div.find(name="div", attrs={"class":"sjcl"}) 
        div_three = div_two.find("div") 
        job_post.append(div_three.text.strip())
      except:
        job_post.append("Nothing_found") 
    sample_df.loc[num] = job_post

sample_df.to_cvs("C:\Users\VARALAKSHMI\Documents\DataScientist.cvs", encoding='utf-8')
