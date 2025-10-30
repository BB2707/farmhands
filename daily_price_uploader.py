import os
import requests
import pandas as pd
from datetime import datetime
from pymongo import MongoClient, UpdateOne

# ---------------------- CONFIG ----------------------
# Get a free API key by registering at https://data.gov.in
API_KEY = os.getenv('DATA_GOV_API_KEY', '579b464db66ec23bdd0000012bef7ddf77fc46517a5708ca18503c95')  # Replace or set in environment variable
RESOURCE_ID = '9ef84268-d588-465a-a308-a864a43d0070'  # Agmarknet resource for current daily prices
LIMIT = 1000  # Number of records to fetch (max 10000 per request)

# MongoDB config
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://rjbijumass:lj5cMiQDHJcLBvnq@cluster0.bktha79.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
DB_NAME = 'market_db'
COLL_NAME = 'commodity_prices'

# Log file
LOG_FILE = "uploader_log.txt"
# -----------------------------------------------------


def log(message: str):
    """Simple log function that appends timestamped messages to a file."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {message}\n")
    print(f"[{datetime.now()}] {message}")


def fetch_data():
    """Fetch commodity data from data.gov.in JSON API."""
    url = (
        f"https://api.data.gov.in/resource/{RESOURCE_ID}"
        f"?api-key={API_KEY}&format=json&limit={LIMIT}"
    )
    log("Fetching data from API...")
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    data = response.json()

    if "records" not in data or not data["records"]:
        raise ValueError("No records found in API response.")

    df = pd.DataFrame(data["records"])
    log(f"Fetched {len(df)} records successfully.")
    return df


def process_and_upload(df: pd.DataFrame, mongo_collection):
    """Process DataFrame and upload to MongoDB."""
    log("Processing data for MongoDB upload...")
    operations = []

    for _, row in df.iterrows():
        try:
            date_str = row.get("arrival_date") or row.get("arrival_date1") or str(datetime.now().date())
            commodity = row.get("commodity", "").strip()
            state = row.get("state", "").strip()
            district = row.get("district", "").strip()
            market = row.get("market", "").strip()
            min_price = float(row.get("min_price", 0))
            max_price = float(row.get("max_price", 0))
            modal_price = float(row.get("modal_price", (min_price + max_price) / 2))
            variety = row.get("variety", "").strip()
            unit = row.get("commodity_unit", "Quintal").strip()

            # Build unique filter key
            filter_doc = {
                "date": date_str,
                "commodity": commodity,
                "state": state,
                "district": district,
                "market": market,
            }

            update_doc = {
                "$set": {
                    "variety": variety,
                    "min_price": min_price,
                    "max_price": max_price,
                    "modal_price": modal_price,
                    "unit": unit,
                    "updated_at": datetime.utcnow(),
                }
            }

            operations.append(UpdateOne(filter_doc, update_doc, upsert=True))

        except Exception as e:
            log(f"Skipping row due to error: {e}")
            continue

    if operations:
        result = mongo_collection.bulk_write(operations)
        log(f"Upserted: {result.upserted_count}, Modified: {result.modified_count}")
    else:
        log("No valid operations to perform.")


def main():
    log("=== Daily Price Upload Started ===")

    try:
        # MongoDB Connection
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        coll = db[COLL_NAME]

        # Fetch and upload data
        df = fetch_data()
        process_and_upload(df, coll)

        log("=== Upload Completed Successfully ===\n")

    except Exception as e:
        log(f"Error in daily upload: {e}\n")

    finally:
        try:
            client.close()
        except:
            pass


if __name__ == "__main__":
    main()
