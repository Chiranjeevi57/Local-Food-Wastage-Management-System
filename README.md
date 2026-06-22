# Local Food Wastage Management System

## Project Description
This project helps reduce food wastage by connecting surplus food providers such as restaurants, grocery stores, and supermarkets with NGOs, community centers, and individuals who need food.

The application uses:
- Python
- SQL / SQLite
- Streamlit
- Data Analysis

## Features
- View available food donations
- Filter food by city, provider type, food type, and meal type
- View provider contact details
- Run 15 SQL analysis queries
- Add, update, and delete food listings
- Add food claims
- View dashboard metrics and charts

## Folder Structure
```text
local_food_wastage_management_system/
│
├── data/
│   ├── providers_data.csv
│   ├── receivers_data.csv
│   ├── food_listings_data.csv
│   └── claims_data.csv
│
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
│
├── src/
│   └── app.py
│
├── requirements.txt
└── README.md
```

## Installation Steps

### 1. Install Python
Install Python 3.10 or above.

### 2. Install Required Libraries
Open terminal in this project folder and run:

```bash
pip install -r requirements.txt
```

### 3. Run Streamlit App
```bash
streamlit run src/app.py
```

### 4. Open Application
After running the command, Streamlit will open the app in your browser.

## Dataset Details

### Providers Dataset
Stores provider details:
- Provider_ID
- Name
- Type
- Address
- City
- Contact

### Receivers Dataset
Stores receiver details:
- Receiver_ID
- Name
- Type
- City
- Contact

### Food Listings Dataset
Stores available food:
- Food_ID
- Food_Name
- Quantity
- Expiry_Date
- Provider_ID
- Provider_Type
- Location
- Food_Type
- Meal_Type

### Claims Dataset
Stores claim details:
- Claim_ID
- Food_ID
- Receiver_ID
- Status
- Timestamp

## SQL Analysis Questions Included
1. Providers and receivers in each city
2. Provider type contributing the most food
3. Contact information of providers in a city
4. Receivers who claimed the most food
5. Total quantity of food available
6. City with highest number of food listings
7. Most commonly available food types
8. Claims made for each food item
9. Provider with highest successful claims
10. Completed vs pending vs cancelled claim percentage
11. Average quantity claimed per receiver
12. Meal type claimed the most
13. Total quantity donated by each provider
14. Food items expiring soon
15. Highest demand locations based on completed claims

## Live Evaluation Explanation
This project solves the problem of food wastage by creating a digital system where providers can list extra food and receivers can claim it. The SQL database stores provider, receiver, food listing, and claim information. The Streamlit app displays food listings, allows filtering, shows provider contact details, supports CRUD operations, and displays SQL analysis results.
