# RCAutomate.com 
# Scrape ICO files from discmaster on archive.org from Archived CD-Rs

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://discmaster.textfiles.com/search?formatid=ico&itemid=13310&pageNum="
OUTPUT_DIR = "ico_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_icons():
    for page_num in range(0, 207):  # Adjust range for actual page count
        print(f"Processing page {page_num}...")
        response = requests.get(f"{BASE_URL}{page_num}")
        if response.status_code != 200:
            print(f"Failed to load page {page_num}. Skipping.")
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        ico_links = [urljoin(BASE_URL, link['href']) for link in links if link['href'].endswith('.ico')]
        print(f"Found {len(ico_links)} .ico files on page {page_num}.")
        print("Links found:")
        for link in ico_links:
            print(link)

        for index, ico_url in enumerate(ico_links):
            # Replace '/view/' with '/file/' in the URL
            ico_url = ico_url.replace("/view/", "/file/")
            try:
                # Extract the last folder and file name
                path_parts = ico_url.split("/")
                last_folder = path_parts[-2]  # Second-to-last segment
                file_name = path_parts[-1]   # Last segment (filename)

                # Create the custom filename
                custom_file_name = f"{last_folder}.{file_name}"
                destination_path = os.path.join(OUTPUT_DIR, custom_file_name)

                # Skip if the file already exists
                if os.path.exists(destination_path):
                    print(f"File {custom_file_name} already exists. Skipping.")
                    continue

                print(f"Downloading {ico_url}...")
                ico_data = requests.get(ico_url)
                if ico_data.status_code == 200:
                            
                    # Save the file
                    with open(destination_path, 'wb') as file:
                        file.write(ico_data.content)
                else:
                    print(f"Failed to download {ico_url}")
            except Exception as e:
                print(f"Error downloading {ico_url}: {e}")
    print("Download complete.")

if __name__ == "__main__":
    fetch_icons()
