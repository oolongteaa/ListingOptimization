# Airbnb Listing Analyzer

A Python app that scrapes, parses, and evaluates an Airbnb listing to help optimize it for online travel agency (OTA) platforms like Airbnb, Vrbo, and more.

---

## Features

-  Scrapes public listing data from Airbnb
-  Parses and extracts structured details (title, description, pricing, amenities, etc.)
-  Sends data to a Poe bot for OTA optimization analysis
-  Outputs clean, formatted results to text files

---

## How It Works

1. User enters an Airbnb listing URL
2. Listing details are scraped using `pyairbnb`
3. Data is parsed with `airbnbParser`
4. Poe bot performs analysis using reference PDFs
5. Results are saved locally

---

