import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "food_wastage.db"

st.set_page_config(page_title="Local Food Wastage Management System", layout="wide")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def load_csv_to_db():
    conn = get_connection()
    providers = pd.read_csv(DATA_DIR / "providers_data.csv")
    receivers = pd.read_csv(DATA_DIR / "receivers_data.csv")
    food = pd.read_csv(DATA_DIR / "food_listings_data.csv")
    claims = pd.read_csv(DATA_DIR / "claims_data.csv")

    providers.to_sql("providers", conn, if_exists="replace", index=False)
    receivers.to_sql("receivers", conn, if_exists="replace", index=False)
    food.to_sql("food_listings", conn, if_exists="replace", index=False)
    claims.to_sql("claims", conn, if_exists="replace", index=False)
    conn.close()

def run_query(query, params=None):
    conn = get_connection()
    result = pd.read_sql_query(query, conn, params=params or {})
    conn.close()
    return result

def execute_sql(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params or {})
    conn.commit()
    conn.close()

if not DB_PATH.exists():
    load_csv_to_db()

st.title("Local Food Wastage Management System")
st.caption("Python + SQL + Streamlit project for food donation management, waste reduction, CRUD operations, filtering, and analysis.")

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Food Listings", "Provider Contacts", "SQL Analysis", "CRUD Operations", "About Project"]
)

if st.sidebar.button("Reload CSV Data"):
    load_csv_to_db()
    st.sidebar.success("CSV data loaded into SQLite database.")

if menu == "Dashboard":
    st.header("Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Providers", int(run_query("SELECT COUNT(*) AS c FROM providers").iloc[0]["c"]))
    col2.metric("Receivers", int(run_query("SELECT COUNT(*) AS c FROM receivers").iloc[0]["c"]))
    col3.metric("Food Listings", int(run_query("SELECT COUNT(*) AS c FROM food_listings").iloc[0]["c"]))
    col4.metric("Claims", int(run_query("SELECT COUNT(*) AS c FROM claims").iloc[0]["c"]))

    st.subheader("Food Quantity by City")
    city_qty = run_query("""
        SELECT Location AS City, SUM(Quantity) AS Total_Quantity
        FROM food_listings
        GROUP BY Location
        ORDER BY Total_Quantity DESC
    """)
    st.bar_chart(city_qty.set_index("City"))

    st.subheader("Claims by Status")
    status_df = run_query("SELECT Status, COUNT(*) AS Count FROM claims GROUP BY Status")
    st.dataframe(status_df, use_container_width=True)

elif menu == "Food Listings":
    st.header("Available Food Listings")

    df = run_query("SELECT * FROM food_listings")
    cities = ["All"] + sorted(df["Location"].dropna().unique().tolist())
    provider_types = ["All"] + sorted(df["Provider_Type"].dropna().unique().tolist())
    food_types = ["All"] + sorted(df["Food_Type"].dropna().unique().tolist())
    meal_types = ["All"] + sorted(df["Meal_Type"].dropna().unique().tolist())

    c1, c2, c3, c4 = st.columns(4)
    city = c1.selectbox("City", cities)
    provider_type = c2.selectbox("Provider Type", provider_types)
    food_type = c3.selectbox("Food Type", food_types)
    meal_type = c4.selectbox("Meal Type", meal_types)

    query = "SELECT * FROM food_listings WHERE 1=1"
    params = {}
    if city != "All":
        query += " AND Location = :city"
        params["city"] = city
    if provider_type != "All":
        query += " AND Provider_Type = :provider_type"
        params["provider_type"] = provider_type
    if food_type != "All":
        query += " AND Food_Type = :food_type"
        params["food_type"] = food_type
    if meal_type != "All":
        query += " AND Meal_Type = :meal_type"
        params["meal_type"] = meal_type

    st.dataframe(run_query(query, params), use_container_width=True)

elif menu == "Provider Contacts":
    st.header("Provider Contact Details")
    city_df = run_query("SELECT DISTINCT City FROM providers ORDER BY City")
    selected_city = st.selectbox("Select City", city_df["City"].tolist())
    providers_df = run_query(
        "SELECT Name, Type, Address, City, Contact FROM providers WHERE City = :city",
        {"city": selected_city}
    )
    st.dataframe(providers_df, use_container_width=True)

elif menu == "SQL Analysis":
    st.header("15 SQL Queries and Outputs")

    queries = {
        "1. Providers and receivers in each city": """
            SELECT City, SUM(Providers) AS Providers, SUM(Receivers) AS Receivers
            FROM (
                SELECT City, COUNT(*) AS Providers, 0 AS Receivers FROM providers GROUP BY City
                UNION ALL
                SELECT City, 0 AS Providers, COUNT(*) AS Receivers FROM receivers GROUP BY City
            )
            GROUP BY City
            ORDER BY City
        """,
        "2. Provider type contributing most food": """
            SELECT Provider_Type, SUM(Quantity) AS Total_Quantity
            FROM food_listings
            GROUP BY Provider_Type
            ORDER BY Total_Quantity DESC
        """,
        "3. Provider contacts in Mumbai": """
            SELECT Name, Type, Address, City, Contact
            FROM providers
            WHERE City = 'Mumbai'
        """,
        "4. Receivers who claimed most food": """
            SELECT r.Name, r.Type, r.City, COUNT(c.Claim_ID) AS Total_Claims
            FROM receivers r
            JOIN claims c ON r.Receiver_ID = c.Receiver_ID
            GROUP BY r.Receiver_ID, r.Name, r.Type, r.City
            ORDER BY Total_Claims DESC
        """,
        "5. Total quantity of food available": """
            SELECT SUM(Quantity) AS Total_Available_Quantity
            FROM food_listings
        """,
        "6. City with highest number of listings": """
            SELECT Location AS City, COUNT(*) AS Total_Listings
            FROM food_listings
            GROUP BY Location
            ORDER BY Total_Listings DESC
        """,
        "7. Most commonly available food types": """
            SELECT Food_Type, COUNT(*) AS Total_Items
            FROM food_listings
            GROUP BY Food_Type
            ORDER BY Total_Items DESC
        """,
        "8. Claims made for each food item": """
            SELECT f.Food_Name, COUNT(c.Claim_ID) AS Total_Claims
            FROM food_listings f
            LEFT JOIN claims c ON f.Food_ID = c.Food_ID
            GROUP BY f.Food_ID, f.Food_Name
            ORDER BY Total_Claims DESC
        """,
        "9. Provider with highest successful claims": """
            SELECT p.Name, p.Type, COUNT(c.Claim_ID) AS Successful_Claims
            FROM providers p
            JOIN food_listings f ON p.Provider_ID = f.Provider_ID
            JOIN claims c ON f.Food_ID = c.Food_ID
            WHERE c.Status = 'Completed'
            GROUP BY p.Provider_ID, p.Name, p.Type
            ORDER BY Successful_Claims DESC
        """,
        "10. Claim status percentage": """
            SELECT Status,
                   COUNT(*) AS Claim_Count,
                   ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Percentage
            FROM claims
            GROUP BY Status
        """,
        "11. Average quantity claimed per receiver": """
            SELECT r.Name, ROUND(AVG(f.Quantity), 2) AS Avg_Quantity_Claimed
            FROM receivers r
            JOIN claims c ON r.Receiver_ID = c.Receiver_ID
            JOIN food_listings f ON c.Food_ID = f.Food_ID
            WHERE c.Status = 'Completed'
            GROUP BY r.Receiver_ID, r.Name
            ORDER BY Avg_Quantity_Claimed DESC
        """,
        "12. Meal type claimed most": """
            SELECT f.Meal_Type, COUNT(c.Claim_ID) AS Total_Claims
            FROM food_listings f
            JOIN claims c ON f.Food_ID = c.Food_ID
            GROUP BY f.Meal_Type
            ORDER BY Total_Claims DESC
        """,
        "13. Quantity donated by each provider": """
            SELECT p.Name, p.Type, SUM(f.Quantity) AS Total_Donated_Quantity
            FROM providers p
            JOIN food_listings f ON p.Provider_ID = f.Provider_ID
            GROUP BY p.Provider_ID, p.Name, p.Type
            ORDER BY Total_Donated_Quantity DESC
        """,
        "14. Food items expiring soon": """
            SELECT Food_Name, Quantity, Expiry_Date, Location, Food_Type, Meal_Type
            FROM food_listings
            WHERE DATE(Expiry_Date) <= DATE('now', '+2 day')
            ORDER BY Expiry_Date ASC
        """,
        "15. Highest demand locations": """
            SELECT f.Location, COUNT(c.Claim_ID) AS Completed_Claims
            FROM food_listings f
            JOIN claims c ON f.Food_ID = c.Food_ID
            WHERE c.Status = 'Completed'
            GROUP BY f.Location
            ORDER BY Completed_Claims DESC
        """
    }

    for title, query in queries.items():
        with st.expander(title):
            st.code(query, language="sql")
            st.dataframe(run_query(query), use_container_width=True)

elif menu == "CRUD Operations":
    st.header("CRUD Operations")

    tab1, tab2, tab3, tab4 = st.tabs(["Add Food", "Update Food", "Delete Food", "Add Claim"])

    with tab1:
        st.subheader("Add New Food Listing")
        with st.form("add_food_form"):
            food_id = st.number_input("Food ID", min_value=1, step=1)
            food_name = st.text_input("Food Name")
            quantity = st.number_input("Quantity", min_value=1, step=1)
            expiry_date = st.date_input("Expiry Date")
            provider_id = st.number_input("Provider ID", min_value=1, step=1)
            provider_type = st.text_input("Provider Type")
            location = st.text_input("Location/City")
            food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
            meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
            submitted = st.form_submit_button("Add Food")
            if submitted:
                execute_sql("""
                    INSERT INTO food_listings
                    VALUES (:food_id, :food_name, :quantity, :expiry_date, :provider_id,
                            :provider_type, :location, :food_type, :meal_type)
                """, {
                    "food_id": food_id, "food_name": food_name, "quantity": quantity,
                    "expiry_date": str(expiry_date), "provider_id": provider_id,
                    "provider_type": provider_type, "location": location,
                    "food_type": food_type, "meal_type": meal_type
                })
                st.success("Food listing added successfully.")

    with tab2:
        st.subheader("Update Food Quantity")
        with st.form("update_food_form"):
            food_id = st.number_input("Food ID to Update", min_value=1, step=1)
            quantity = st.number_input("New Quantity", min_value=0, step=1)
            submitted = st.form_submit_button("Update Quantity")
            if submitted:
                execute_sql("UPDATE food_listings SET Quantity = :quantity WHERE Food_ID = :food_id",
                            {"quantity": quantity, "food_id": food_id})
                st.success("Food quantity updated successfully.")

    with tab3:
        st.subheader("Delete Food Listing")
        with st.form("delete_food_form"):
            food_id = st.number_input("Food ID to Delete", min_value=1, step=1)
            submitted = st.form_submit_button("Delete Food")
            if submitted:
                execute_sql("DELETE FROM food_listings WHERE Food_ID = :food_id", {"food_id": food_id})
                st.success("Food listing deleted successfully.")

    with tab4:
        st.subheader("Add Claim")
        with st.form("add_claim_form"):
            claim_id = st.number_input("Claim ID", min_value=1, step=1)
            food_id = st.number_input("Food ID", min_value=1, step=1)
            receiver_id = st.number_input("Receiver ID", min_value=1, step=1)
            status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])
            timestamp = st.text_input("Timestamp", value=pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
            submitted = st.form_submit_button("Add Claim")
            if submitted:
                execute_sql("INSERT INTO claims VALUES (:claim_id, :food_id, :receiver_id, :status, :timestamp)",
                            {"claim_id": claim_id, "food_id": food_id, "receiver_id": receiver_id,
                             "status": status, "timestamp": timestamp})
                st.success("Claim added successfully.")

    st.subheader("Current Food Listings")
    st.dataframe(run_query("SELECT * FROM food_listings ORDER BY Food_ID"), use_container_width=True)

elif menu == "About Project":
    st.header("About Project")
    st.write("""
    This project connects surplus food providers with NGOs, community centers, and individuals in need.
    Restaurants, grocery stores, and supermarkets can list extra food. Receivers can view and claim available food.
    SQL is used for data storage and analysis, while Streamlit provides the user interface.
    """)
    st.write("Technical Tags: Python, SQL, Streamlit, Data Analysis, Food Management")
