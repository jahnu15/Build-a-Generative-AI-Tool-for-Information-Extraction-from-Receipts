import pytesseract
from PIL import Image
import pandas as pd
import re

# Path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path based on your tesseract installation

# Function to extract text from image
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Function to parse extracted text
def parse_receipt_text(text):
    data = {}
    
    # Extracting shop name and address
    shop_info = re.findall(r'^[A-Z\s&]+', text, re.MULTILINE)
    data['Shop Name'] = shop_info[0] if shop_info else ''
    address_info = re.findall(r'^[0-9]+\s.+$', text, re.MULTILINE)
    data['Address'] = address_info[0] if address_info else ''
    
    # Extracting date and time
    date_info = re.findall(r'\d{2}/\d{2}/\d{4}', text)
    time_info = re.findall(r'\d{2}:\d{2}', text)
    data['Date'] = date_info[0] if date_info else ''
    data['Time'] = time_info[0] if time_info else ''
    
    # Extracting items and prices
    items = re.findall(r'([A-Za-z\s]+)\s+(\d+\.\d{2})', text)
    item_details = [{'Item': item[0].strip(), 'Price': float(item[1])} for item in items]
    data['Items'] = item_details
    
    # Extracting GST and total cost
    gst_info = re.findall(r'GST\s+10%\s+(\d+\.\d{2})', text)
    total_cost_info = re.findall(r'AUD\s+(\d+\.\d{2})', text)
    data['GST'] = float(gst_info[0]) if gst_info else 0.0
    data['Total Cost'] = float(total_cost_info[0]) if total_cost_info else 0.0
    
    return data

# Function to save data to CSV or Excel
def save_to_file(data, file_path, file_type='csv'):
    if file_type == 'csv':
        items_df = pd.DataFrame(data['Items'])
        items_df['Shop Name'] = data['Shop Name']
        items_df['Address'] = data['Address']
        items_df['Date'] = data['Date']
        items_df['Time'] = data['Time']
        items_df['GST'] = data['GST']
        items_df['Total Cost'] = data['Total Cost']
        items_df.to_csv(file_path, index=False)
    elif file_type == 'excel':
        with pd.ExcelWriter(file_path) as writer:
            items_df = pd.DataFrame(data['Items'])
            items_df.to_excel(writer, sheet_name='Items', index=False)
            details_df = pd.DataFrame([{
                'Shop Name': data['Shop Name'],
                'Address': data['Address'],
                'Date': data['Date'],
                'Time': data['Time'],
                'GST': data['GST'],
                'Total Cost': data['Total Cost']
            }])
            details_df.to_excel(writer, sheet_name='Details', index=False)

# Function to prompt for specific details
def prompt_for_details(data):
    while True:
        detail = input("Enter the detail you want to know (Shop Name, Address, Date, Time, GST, Total Cost, Items): ")
        if detail in data:
            print(data[detail])
        elif detail == 'Items':
            for item in data['Items']:
                print(f"Item: {item['Item']}, Price: {item['Price']}")
        else:
            print("Invalid detail. Please try again.")
        another = input("Do you want to check another detail? (yes/no): ")
        if another.lower() != 'yes':
            break

# Main execution
if __name__ == "__main__":
    image_path = r'C:\Users\Gadda\OneDrive\Desktop\new\h&m.jpg'  # Update with your image path
    text = extract_text_from_image(image_path)
    receipt_data = parse_receipt_text(text)
    save_to_file(receipt_data, 'receipt_data.csv', 'csv')
    save_to_file(receipt_data, 'receipt_data.xlsx', 'excel')
    prompt_for_details(receipt_data)
