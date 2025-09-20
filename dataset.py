import pandas as pd

# Define data with CONSISTENT column names for reliability
data = [
    {
        "Name": "Charu Pramod Biriya",
        "ID_Type": "Aadhaar",
        "ID_Number": "820773092057",
        "PAN_Number": "FQLPB1769P",
        "Role": "Tenant",
        "Associated_Name": "VALMIK GANGADHAR MURKUTE",
        "Amount": 9000,
        "Notes": "Rental agreement from 01/11/2024 to 30/09/2025."
    },
    {
        "Name": "JAY YOGRAJ PAWAR",
        "ID_Type": "Aadhaar",
        "ID_Number": "995921777311",
        "PAN_Number": "IPBPP5852R",
        "Role": "Account Holder",
        "Associated_Name": "Punjab National Bank",
        "Amount": None,
        "Notes": "Bank account opened on 28-08-2014."
    },
    {
        "Name": "SWAPNIL SANJAY KELGANDRE",
        "ID_Type": None,
        "ID_Number": None,
        "PAN_Number": None,
        "Role": "Tenant",
        "Associated_Name": "DATTA ASARAM GANDHALE",
        "Amount": 4000,
        "Notes": "Rental agreement from 13/10/2024 to 12/08/2025."
    },
    {
        "Name": "SHRI POTU RAMA ATRAM",
        "ID_Type": "Meter",
        "ID_Number": "06415094509",
        "PAN_Number": None,
        "Role": "Consumer",
        "Associated_Name": "MSEDCL",
        "Amount": 630,
        "Notes": "Electricity bill for Pandharkawada unit."
    }
]

df = pd.DataFrame(data)

# Create a single searchable column for the best search results
df['Searchable_Details'] = df.apply(lambda row: ' '.join(row.astype(str)), axis=1)

# Save the cleaned dataset as a simple CSV file
df.to_csv("my_data.csv", index=False)

print("✅ Cleaned and consistent dataset saved as my_data.csv.")
