# Data-Ingestion-Processing-Pipeline
📊 Data Ingestion & Processing Pipeline

📌 Project Overview

This project implements a data engineering pipeline that extracts, processes, and stores structured data from multiple sources. The goal is to simulate a real-world data workflow where raw data is collected, cleaned, validated, and saved for downstream analysis.

The pipeline integrates:
	•	API data extraction
	•	Web scraping
	•	Data cleaning and transformation
	•	Logging and error handling
	•	Data validation

⸻

🎯 Objective

To build a robust and modular Python pipeline that:
	•	Extracts data from an API
	•	Scrapes data from a website
	•	Cleans and transforms datasets
	•	Logs pipeline activities
	•	Handles errors effectively
	•	Saves clean datasets as CSV files

⸻

🗂️ Data Sources

1. API Data
	•	Source: https://jsonplaceholder.typicode.com/users
	•	Extracted Fields:
	•	name
	•	username
	•	email
	•	city (from address.city)
	•	company (from company.name)

⸻

2. Web Scraped Data
	•	Source: https://books.toscrape.com/
	•	Extracted Fields:
	•	title
	•	price
	•	rating

Scraping Requirements:
	•	Scraped at least 5 pages
	•	Converted:
	•	Price → float (removed currency symbol)
	•	Rating → numeric (e.g., “Three” → 3)

⸻

⚙️ Pipeline Architecture

The pipeline is built using modular functions:
fetch_api_data()
scrape_books_data()
clean_data()
save_data()
main()

🔄 Pipeline Flow
def main():
    users = fetch_api_data()
    books = scrape_books_data()

    clean_users = clean_data(users, type="users")
    clean_books = clean_data(books, type="books")

    save_data(clean_users, "users.csv")
    save_data(clean_books, "books.csv")

    🧹 Data Cleaning

The clean_data() function performs:
	•	Removal of currency symbols from price
	•	Conversion of price to float
	•	Conversion of rating from text to integer
	•	Standardization of column names (lowercase, underscores)
	•	Handling missing values (dropna())

⸻

🛡️ Error Handling

The pipeline uses try/except blocks to handle:
	•	API request failures
	•	Missing fields in API data
	•	Web scraping errors
	•	Data type conversion errors
	•	File saving issues

⸻

📋 Logging

The pipeline uses Python’s logging module to track:
	•	Pipeline start
	•	API extraction success
	•	Scraping success (per page)
	•	Errors encountered
	•	Pipeline completion

Example log output:
INFO - Pipeline started
INFO - API extraction success
INFO - Scraping success for page 1
ERROR - Missing field in API data
INFO - Pipeline completed successfully

Data Validation (Bonus)

Additional validation checks include:
	•	Detecting empty datasets before processing
	•	Ensuring correct data types (e.g., price is numeric)
	•	Verifying required columns exist
	•	Preventing saving of empty files

⸻

📁 Output Files

The pipeline generates the following files:
	•	users.csv → Cleaned API data
	•	books.csv → Cleaned scraped data

⸻

🛠️ Technologies Used
	•	Python 🐍
	•	pandas
	•	requests
	•	BeautifulSoup (bs4)
	•	logging

⸻

🚀 How to Run the Project
	1.	Install required libraries:
  pip install pandas requests beautifulsoup4
  2.	Run the Jupyter Notebook or Python script
	3.	Execute: 
  main()

  4.	Output files will be saved in your working directory

⸻

📌 Deliverables

This repository contains:
	•	Python script (.py)
	•	Jupyter Notebook (.ipynb)
	•	Output CSV files (users.csv, books.csv)
	•	Logging output/screenshots
	•	README documentation

⸻

💡 Conclusion

This project demonstrates a complete data engineering pipeline with:
	•	Modular design
	•	Robust error handling
	•	Detailed logging
	•	Clean and structured outputs

It reflects real-world practices in building scalable and maintainable data pipelines.

