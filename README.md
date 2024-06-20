# Web-Scraping-Using-Beautiful-Soup-And-MySQL

## Overview
This project is a web scraper designed to extract various pieces of information from a list of websites and store the extracted data into a MySQL database. The information includes meta titles, meta descriptions, social media links, technology stacks, payment gateways, website languages, and categorization based on content.

## Requirements
- Python 3.x
- MySQL server
- Required Python packages (see below)

## Setup Instructions

### Clone the repository:
sh
git clone https://your-repo-link
cd your-repo-directory


## Install Python packages:

sh
pip install -r requirements.txt

## Setup MySQL Database:

Start your MySQL server.
Create a new database called web_scraping.
Execute the provided SQL script to create necessary tables.

sh
mysql -u root -p web_scraping < create_tables.sql

## Update Database Configuration:
Edit the database connection details in web_scraper.py as needed.

python

connection = mysql.connector.connect(
    host='localhost',
    user='your_mysql_user',
    password='your_mysql_password',
    database='web_scraping'
)

## Run the Scraper:

python web_scraper.py

## SQL Script
The create_tables.sql file contains the necessary SQL commands to create the tables used in this project.

## Extracted Information
The scraper extracts the following information from each website:

Meta title
Meta description
Social media links (Facebook, Twitter, LinkedIn, Instagram)
Technology stack (e.g., WordPress, jQuery, React)
Payment gateways (e.g., PayPal, Stripe, Razorpay)
Website language
Category (e.g., ecommerce, education, news, real estate)
