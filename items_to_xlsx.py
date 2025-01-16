import openpyxl
from openpyxl.styles import Alignment, Font

# Paths for input .txt and output .xlsx files
input_txt_file = "market_prices.txt"
output_xlsx_file = "market_prices.xlsx"

# Quality mapping
quality_mapping = {
    "0": "Normal",
    "1": "Good",
    "2": "Outstanding",
    "3": "Excellent",
    "4": "Masterpiece"
}

# Function to read and process the .txt file
def read_and_process_txt():
    items = []
    prices = []
    details = []

    with open(input_txt_file, "r") as file:
        lines = file.readlines()

    item_block = []
    price_block = []
    detail_dict = {"Tier": "", "Enchantment": "", "Quality": ""}

    for line in lines:
        line = line.strip()

        if line.startswith("Item Details"):  # Extract tier, enchantment, and quality
            detail_line = line.replace("Item Details - ", "").split(", ")
            for detail in detail_line:
                key, value = detail.split(": ")
                if key == "Quality":
                    value = quality_mapping.get(value, value)  # Map quality number to text
                detail_dict[key] = value
        elif "'" in line or line.isalpha():  # Extract item names
            item_block.append(line.strip("'"))
        elif line.replace(",", "").isdigit():  # Extract prices
            price_block.append(line)

        # Once 4 items and prices are collected, associate them with details
        if len(item_block) == 4 and len(price_block) == 4:
            items.extend(item_block)
            prices.extend(price_block)
            details.extend([detail_dict.copy()] * 4)  # Duplicate details for all 4 items
            item_block, price_block = [], []  # Reset for next block

    return items, prices, details

# Function to append or update data in the Excel sheet
def save_to_xlsx(items, prices, details):
    # Load workbook if it exists; otherwise, create a new one
    try:
        wb = openpyxl.load_workbook(output_xlsx_file)
    except FileNotFoundError:
        wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = "Market Prices"

    # Helper function to find rows with matching headers
    def find_header_row(header):
        for row in ws.iter_rows():
            if row[0].value == header:
                return row[0].row
        return None

    for item, price, detail in zip(items, prices, details):
        # Generate header
        header = f"Tier {detail['Tier']}, Enchantment {detail['Enchantment']}, Quality {detail['Quality']}"
        header_row = find_header_row(header)

        if header_row:  # Header exists, check for matching item
            item_found = False
            for row in ws.iter_rows(min_row=header_row + 1, max_col=2):
                if row[0].value == item:  # Update price if item matches
                    row[1].value = price
                    item_found = True
                    break

            if not item_found:  # If item not found, append it under the header
                ws.append([item, price])
        else:  # Header doesn't exist, append header and new items
            ws.append([header])  # Append header
            ws[f"A{ws.max_row}"].font = Font(bold=True)  # Make header bold
            ws.append([item, price])  # Append item and price

    # Save the workbook
    wb.save(output_xlsx_file)
    print(f"Data saved to {output_xlsx_file}")

# Main function to execute the process
def main():
    items, prices, details = read_and_process_txt()
    save_to_xlsx(items, prices, details)

# Run the program
if __name__ == "__main__":
    main()
