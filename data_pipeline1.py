#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
import logging
from bs4 import BeautifulSoup


# In[3]:


url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

print(response.status_code)

data = response.json()

print(data[0])


# In[4]:


extracted_data = []

for user in data:
    extracted_data.append({
        "name": user["name"],
        "username": user["username"],
        "email": user["email"],
        "city": user["address"]["city"],        
        "company": user["company"]["name"]      
    })


# In[6]:


df = pd.DataFrame(extracted_data)


# In[7]:


df.head()


# In[8]:


df.tail()


# In[10]:


df.to_csv("users.csv", index=False)


# In[ ]:





# In[14]:


url = "https://books.toscrape.com/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

print(soup.title.text)


# In[16]:


books = []


# In[17]:


for page in range(1, 6):
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    all_books = soup.find_all("article", class_="product_pod")

    for book in all_books:
        # Title
        title = book.h3.a["title"]

        # Price
        price = book.find("p", class_="price_color").text

        # Rating
        rating = book.p["class"][1]

        books.append({
            "Book Title": title,
            "Price": price,
            "Rating": rating
        })


# In[18]:


df = pd.DataFrame(books)


# In[19]:


df.head()


# In[20]:


df.tail()


# In[22]:


# map word rating to a number
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["Rating"] = df["Rating"].map(rating_map)


# In[24]:


# replace spaces with underscores and converts all columns to lowercase
df.columns = df.columns.str.lower().str.replace(" ", "_")


# In[25]:


# handles missing values
df.isnull().sum()


# In[26]:


# data type of each column in the data frame
print(df.dtypes)


# In[27]:


df.head()


# In[28]:


# Saves the DataFrame to a csv file and names the file "books.csv"
df.to_csv("books.csv", index=False)


# In[ ]:





# In[29]:


# Configure logging
logging.basicConfig(
    level=logging.INFO,  # log all INFO and higher level messages
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Pipeline started")  # Log start of pipeline


# In[30]:


# Fetches data from an API and processes
try:
    api_url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(api_url)     # makes a get request
    response.raise_for_status()  # raises error if status != 200
    api_data = response.json()

    # Extract required fields
    api_extracted = []
    for user in api_data:
        try:
            api_extracted.append({
                "name": user["name"],
                "username": user["username"],
                "email": user["email"],
                "city": user["address"]["city"],
                "company": user["company"]["name"]
            })
        except KeyError as e:   # gets a key error
            logging.error(f"Missing field in API data: {e}")  # handles missing fields with logging

    df_api = pd.DataFrame(api_extracted)    # converts extracted data to a dataframe
    logging.info("API extraction success")

except requests.RequestException as e:
    logging.error(f"API request failed: {e}")


# In[ ]:





# In[ ]:





# In[48]:


def fetch_api_data():
    logging.info("Starting API extraction") #
    api_url = "https://jsonplaceholder.typicode.com/users"
    extracted = []   #empty list where each data will be stored as a dictionary

    try:
        response = requests.get(api_url)       # sends a GET request to the api to fetch data
        response.raise_for_status()            # raises an error if there is a bad ststus code; 404
        data = response.json()                 # converts json response to dictionary lists

        for user in data:                # loops through dictionary in the list
            try:
                extracted.append({           # adds a new dictionary to the extracted list with fields needed
                    "name": user["name"],
                    "username": user["username"],
                    "email": user["email"],
                    "city": user["address"]["city"],
                    "company": user["company"]["name"]
                })
            except KeyError as e:
                logging.error(f"Missing field in API data: {e}")      # if a field is missing, instead of crashing the program. It logs an error

        logging.info("API extraction success")

    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")      # if the get get request fails (bad status code). Log the error

    return pd.DataFrame(extracted)                    # converts exctracted list to dataframe


# In[ ]:





# In[36]:


def scrape_books_data(pages=5):  #defines a number of pages to be scraped
    logging.info("Starting web scraping")
    books = []

    for page in range(1, pages+1):     # loops throuugh pages and ensures its starts from 1 and the last page
        try:
            url = f"https://books.toscrape.com/catalogue/page-{page}.html"    # sends get request to the website 
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")    # parses  the html so python can read it
            all_books = soup.find_all("article", class_="product_pod")  # each book on the page is an article tag withclass as 'product_pod'

            for book in all_books:
                try:
                    title = book.h3.a["title"]   #gets book  title from the 'a' tag inside 'h3'
                    price = book.find("p", class_="price_color").text      # gets price as text
                    rating = book.p["class"][1]       # gets rating as a word
                    books.append({"Book Title": title, "Price": price, "Rating": rating})   #stores books in a list
                except AttributeError as e:
                    logging.error(f"Scraping error for a book: {e}")

            logging.info(f"Scraping success for page {page}") # logs an info message when a page is scraped successfully

        except requests.RequestException as e:
            logging.error(f"Failed to scrape page {page}: {e}") # if a particular page is not loading /fails, log an error and conitinue with other pages

    return pd.DataFrame(books)


# In[49]:


def clean_data(df, type="books"):
    logging.info(f"Starting data cleaning for {type}")     # log the start
    if df.empty: # cecks if dataframe has no rows
        logging.warning(f"The {type} dataset is empty!")   #logs a warning if its empty
        return df

    try:
        if type == "books":
            # Convert rating: converts rating words to numbers
            rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            df["Rating"] = df["Rating"].map(rating_map)
            # Rename columns: converts to lower cases and replaces space with underscores
            df.columns = df.columns.str.lower().str.replace(" ", "_")
        else:  # users data
            df.columns = df.columns.str.lower().str.replace(" ", "_")

        # Handle missing values: drops rows with missing vaues and makes sure datasets has no empty fields
        df.dropna(inplace=True)
        logging.info(f"Data cleaning completed for {type}")

    except Exception as e:
        logging.error(f"Data cleaning error for {type}: {e}")

    return df


# In[62]:


def save_data(df, filename):   #defines a reusable function so you can save dataset without rewriting code
    try:
        if df.empty:          # checks if dataframe has no empty rows
            logging.warning(f"{filename} is empty. Skipping save.")   # logs a warning if its empty and skips saving 
            return
        df.to_csv(filename, index=False)    #saves dataframe as a csv
        logging.info(f"Saved {filename} successfully")    #
    except Exception as e:
        logging.error(f"Error saving {filename}: {e}")    


# In[63]:


def main():
    logging.info("Pipeline started")

    users = fetch_api_data()   # calls the fetch api data defined earlier and fetches user data from the api. Returns dataframe stored in the variable
    books = scrape_books_data()   #scrapes book title, price and rating from the first 5 pages of the website

    clean_users = clean_data(users, type="users") #renmes columns to lowercase , remove spaces and handle missing values and returns clean dataset
    clean_books = clean_data(books, type="books")

    save_data(clean_users, "users.csv")  #calls save data to save the cleaned users dataframe as users.csv in jupyter folder
    save_data(clean_books, "books.csv")

    logging.info("Pipeline completed successfully")    # helps you know all steps (API, scraping, cleaning,saving) are complete


# In[64]:


main()


# 
