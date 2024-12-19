import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI")  # MongoDB connection string
if "tlsAllowInvalidCertificates=true" not in MONGODB_URI:
    MONGODB_URI += "&tlsAllowInvalidCertificates=true"

DATABASE_NAME = "your_database_name"  # Replace with your database name

# Initialize MongoDB client
client = MongoClient(
    MONGODB_URI,
    tls=True,
    tlsAllowInvalidCertificates=True  # Explicitly allow invalid certificates
)

db = client[DATABASE_NAME]

# Load the Excel file
FILE_PATH = "/Users/hrushik/Downloads/ClimateImpactLab_USData_20March2023.xlsx"  # Replace with your file path
excel_data = pd.ExcelFile(FILE_PATH)

# Upload each sheet as a separate collection
for sheet_name in excel_data.sheet_names:
    print(f"Uploading sheet: {sheet_name}")
    # Parse the sheet into a DataFrame
    data = excel_data.parse(sheet_name)
    # Convert DataFrame to a list of dictionaries
    data_dict = data.to_dict("records")
    # Insert into MongoDB
    collection = db[sheet_name]
    try:
        if data_dict:  # Check if the sheet is not empty
            result = collection.insert_many(data_dict)
            print(f"Successfully inserted {len(result.inserted_ids)} records into collection: {sheet_name}")
        else:
            print(f"Sheet {sheet_name} is empty. Skipping.")
    except Exception as e:
        print(f"Error uploading sheet {sheet_name}: {e}")

# Close the MongoDB connection
client.close()
