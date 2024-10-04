import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_drugbank_targets(target_name):
    # Base URL for DrugBank targets
    base_url = f"https://go.drugbank.com/targets?approved=0&nutraceutical=0&illicit=0&investigational=0&withdrawn=0&experimental=0&us=0&ca=0&eu=0&q%5Bdrug%5D=&q%5Bassociation_type%5D=&q%5Bpolypeptides.name%5D={target_name}&button="
    
    # Initialize a list to hold the table data
    data = []

    # Loop through the pages
    page_number = 1
    while True:
        # Construct the URL for the current page
        url = f"{base_url}&page={page_number}"
        print(f"Fetching data from: {url}")

        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table
        table = soup.find('table', {'id': 'targets-table'})

        # Break the loop if no table is found
        if not table:
            print("No more pages to scrape or table not found.")
            break

        # Iterate over table rows
        for row in table.find_all('tr')[1:]:  # Skip the header row
            cols = row.find_all('td')
            if len(cols) >= 4:
                drug_name = cols[0].text.strip()
                association_type = cols[1].text.strip()
                association_name = cols[2].text.strip()
                details_link = 'https://go.drugbank.com' + cols[0].find('a')['href']  # Construct the full URL
                data.append([drug_name, association_type, association_name, details_link])

        # Check for the presence of a "Next" button
        next_button = soup.find('li', class_='next')
        if not next_button or 'disabled' in next_button['class']:
            print("No more pages to scrape.")
            break

        # Increment the page number
        page_number += 1

    # Create a DataFrame
    df = pd.DataFrame(data, columns=['Drug Name', 'Type', 'Association Name', 'Details Link'])

    # Save the DataFrame to an Excel file
    output_file = f'drugbank_targets_{target_name}.xlsx'
    df.to_excel(output_file, index=False)

    print(f"Data has been saved to {output_file}.")

# Example usage
target_name_input = input("Enter the target name to fetch data: ")
fetch_drugbank_targets(target_name_input)
