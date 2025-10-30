import json
from pymongo import MongoClient

# --- IMPORTANT ---
# Paste your MongoDB Atlas connection string here.
# Replace <username> and <password> with your actual database user credentials.
MONGO_CONNECTION_STRING = "mongodb+srv://rjbijumass:lj5cMiQDHJcLBvnq@cluster0.bktha79.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# --- Configuration ---
DATABASE_NAME = "farmhands"
COLLECTION_NAME = "plants"
JSON_FILE_PATH = "plant_data.json"

def import_data():
    """Reads data from a local JSON file and uploads it to a MongoDB collection."""
    try:
        # 1. Connect to the MongoDB cluster
        print("Connecting to MongoDB Atlas...")
        client = MongoClient(MONGO_CONNECTION_STRING)
        
        # 2. Get the database and collection
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        
        # 3. Read the local JSON file
        print(f"Reading data from {JSON_FILE_PATH}...")
        with open(JSON_FILE_PATH, 'r') as f:
            plant_data = json.load(f)
            
        # 4. Clear existing data in the collection (optional, but good for clean imports)
        print(f"Deleting existing documents in '{COLLECTION_NAME}' collection...")
        collection.delete_many({})
        
        # 5. Insert the new data
        print(f"Inserting {len(plant_data)} documents into the collection...")
        collection.insert_many(plant_data)
        
        print("\n✅ Data import successful!")
        print(f"Check your '{DATABASE_NAME}' database in MongoDB Atlas.")

    except FileNotFoundError:
        print(f"Error: The file {JSON_FILE_PATH} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    import_data()
