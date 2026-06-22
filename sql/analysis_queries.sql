-- 15 SQL Queries for Analysis

-- 1. Food providers and receivers in each city
SELECT City, SUM(Providers) AS Providers, SUM(Receivers) AS Receivers
FROM (
    SELECT City, COUNT(*) AS Providers, 0 AS Receivers FROM providers GROUP BY City
    UNION ALL
    SELECT City, 0 AS Providers, COUNT(*) AS Receivers FROM receivers GROUP BY City
)
GROUP BY City
ORDER BY City;

-- 2. Provider type contributing the most food quantity
SELECT Provider_Type, SUM(Quantity) AS Total_Quantity
FROM food_listings
GROUP BY Provider_Type
ORDER BY Total_Quantity DESC;

-- 3. Contact information of providers in a specific city
SELECT Name, Type, Address, City, Contact
FROM providers
WHERE City = 'Mumbai';

-- 4. Receivers who claimed the most food
SELECT r.Name, r.Type, r.City, COUNT(c.Claim_ID) AS Total_Claims
FROM receivers r
JOIN claims c ON r.Receiver_ID = c.Receiver_ID
GROUP BY r.Receiver_ID, r.Name, r.Type, r.City
ORDER BY Total_Claims DESC;

-- 5. Total quantity of food available
SELECT SUM(Quantity) AS Total_Available_Quantity
FROM food_listings;

-- 6. City with highest number of food listings
SELECT Location AS City, COUNT(*) AS Total_Listings
FROM food_listings
GROUP BY Location
ORDER BY Total_Listings DESC;

-- 7. Most commonly available food types
SELECT Food_Type, COUNT(*) AS Total_Items
FROM food_listings
GROUP BY Food_Type
ORDER BY Total_Items DESC;

-- 8. Number of food claims made for each food item
SELECT f.Food_Name, COUNT(c.Claim_ID) AS Total_Claims
FROM food_listings f
LEFT JOIN claims c ON f.Food_ID = c.Food_ID
GROUP BY f.Food_ID, f.Food_Name
ORDER BY Total_Claims DESC;

-- 9. Provider with highest number of successful claims
SELECT p.Name, p.Type, COUNT(c.Claim_ID) AS Successful_Claims
FROM providers p
JOIN food_listings f ON p.Provider_ID = f.Provider_ID
JOIN claims c ON f.Food_ID = c.Food_ID
WHERE c.Status = 'Completed'
GROUP BY p.Provider_ID, p.Name, p.Type
ORDER BY Successful_Claims DESC;

-- 10. Percentage of claims by status
SELECT Status,
       COUNT(*) AS Claim_Count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Percentage
FROM claims
GROUP BY Status;

-- 11. Average quantity of food claimed per receiver
SELECT r.Name, ROUND(AVG(f.Quantity), 2) AS Avg_Quantity_Claimed
FROM receivers r
JOIN claims c ON r.Receiver_ID = c.Receiver_ID
JOIN food_listings f ON c.Food_ID = f.Food_ID
WHERE c.Status = 'Completed'
GROUP BY r.Receiver_ID, r.Name
ORDER BY Avg_Quantity_Claimed DESC;

-- 12. Meal type claimed the most
SELECT f.Meal_Type, COUNT(c.Claim_ID) AS Total_Claims
FROM food_listings f
JOIN claims c ON f.Food_ID = c.Food_ID
GROUP BY f.Meal_Type
ORDER BY Total_Claims DESC;

-- 13. Total quantity donated/listed by each provider
SELECT p.Name, p.Type, SUM(f.Quantity) AS Total_Donated_Quantity
FROM providers p
JOIN food_listings f ON p.Provider_ID = f.Provider_ID
GROUP BY p.Provider_ID, p.Name, p.Type
ORDER BY Total_Donated_Quantity DESC;

-- 14. Food items expiring soon
SELECT Food_Name, Quantity, Expiry_Date, Location, Food_Type, Meal_Type
FROM food_listings
WHERE DATE(Expiry_Date) <= DATE('now', '+2 day')
ORDER BY Expiry_Date ASC;

-- 15. Highest demand locations based on completed claims
SELECT f.Location, COUNT(c.Claim_ID) AS Completed_Claims
FROM food_listings f
JOIN claims c ON f.Food_ID = c.Food_ID
WHERE c.Status = 'Completed'
GROUP BY f.Location
ORDER BY Completed_Claims DESC;
