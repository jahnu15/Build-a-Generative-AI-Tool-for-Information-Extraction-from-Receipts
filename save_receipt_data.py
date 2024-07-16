import pandas as pd

# Actual extracted information from the receipt image
extracted_information = {
    "vendor_name": "Maaharaja Restaurant",
    "vendor_address": "Dakuria, Kolkata - 700031",
    "datetime": "22/10/16",
    "items_purchased": [
        {"item_name": "water bottle", "quantity": 1, "item_cost": 30},
        {"item_name": "Baby Corn", "quantity": 1, "item_cost": 170},
        {"item_name": "Kashmiri Pulao", "quantity": 1, "item_cost": 130},
        {"item_name": "Kadai Chicken", "quantity": 1, "item_cost": 250},
        {"item_name": "Biryani Mutton", "quantity": 1, "item_cost": 220},
        {"item_name": "Soft Drinks", "quantity": 1, "item_cost": 40}
    ],
    "Total Qty": 6,
    "subtotal": 840,
}

# Convert main receipt information to DataFrame
data = {
    "Vendor Name": [extracted_information["vendor_name"]],
    "Vendor Address": [extracted_information["vendor_address"]],
    "Date and Time": [extracted_information["datetime"]],
    "Subtotal": [extracted_information["subtotal"]],
    "Tax Rate": [0.07],  # Assuming no separate tax rate given on receipt; subtotal equals total after tax.
    "Total After Tax": [extracted_information["subtotal"]],
}

# Create DataFrame for the purchased items
items_df = pd.DataFrame(extracted_information["items_purchased"])

# Create a DataFrame for the main receipt information
receipt_df = pd.DataFrame(data)

# Save the data to an Excel file with multiple sheets
with pd.ExcelWriter('receipt_data.xlsx') as writer:
    receipt_df.to_excel(writer, index=False, sheet_name='Receipt Info')
    items_df.to_excel(writer, index=False, sheet_name='Items Purchased')

# Save the data to CSV files
receipt_df.to_csv('receipt_info.csv', index=False)
items_df.to_csv('items_purchased.csv', index=False)

print("Data has been saved to receipt_data.xlsx and CSV files.")

# Function to query the data
def query_data():
    while True:
        print("\nWhat information would you like to know? Options:")
        print("1. Vendor Name")
        print("2. Vendor Address")
        print("3. Date and Time")
        print("4. Subtotal")
        print("5. Tax Rate")
        print("6. Total After Tax")
        print("7. Individual Item Costs")
        print("8. Exit")
        choice = input("Enter the number of your choice: ")

        if choice == "1":
            print(f"Vendor Name: {extracted_information['vendor_name']}")
        elif choice == "2":
            print(f"Vendor Address: {extracted_information['vendor_address']}")
        elif choice == "3":
            print(f"Date and Time: {extracted_information['datetime']}")
        elif choice == "4":
            print(f"Subtotal: {extracted_information['subtotal']}")
        elif choice == "5":
            print(f"Tax Rate: {0.07}")  # Tax rate as a placeholder
        elif choice == "6":
            print(f"Total After Tax: {extracted_information['subtotal']}")
        elif choice == "7":
            print("Individual Item Costs:")
            for item in extracted_information['items_purchased']:
                print(f" - {item['item_name']} (Quantity: {item['quantity']}): ${item['item_cost']}")
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the query function
query_data()
