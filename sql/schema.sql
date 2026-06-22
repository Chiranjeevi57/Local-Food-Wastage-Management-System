-- Local Food Wastage Management System - SQLite Schema

DROP TABLE IF EXISTS claims;
DROP TABLE IF EXISTS food_listings;
DROP TABLE IF EXISTS receivers;
DROP TABLE IF EXISTS providers;

CREATE TABLE providers (
    Provider_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Type TEXT NOT NULL,
    Address TEXT,
    City TEXT NOT NULL,
    Contact TEXT
);

CREATE TABLE receivers (
    Receiver_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Type TEXT NOT NULL,
    City TEXT NOT NULL,
    Contact TEXT
);

CREATE TABLE food_listings (
    Food_ID INTEGER PRIMARY KEY,
    Food_Name TEXT NOT NULL,
    Quantity INTEGER NOT NULL,
    Expiry_Date DATE NOT NULL,
    Provider_ID INTEGER NOT NULL,
    Provider_Type TEXT,
    Location TEXT NOT NULL,
    Food_Type TEXT,
    Meal_Type TEXT,
    FOREIGN KEY (Provider_ID) REFERENCES providers(Provider_ID)
);

CREATE TABLE claims (
    Claim_ID INTEGER PRIMARY KEY,
    Food_ID INTEGER NOT NULL,
    Receiver_ID INTEGER NOT NULL,
    Status TEXT NOT NULL CHECK(Status IN ('Pending', 'Completed', 'Cancelled', 'Canceled')),
    Timestamp DATETIME NOT NULL,
    FOREIGN KEY (Food_ID) REFERENCES food_listings(Food_ID),
    FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID)
);
