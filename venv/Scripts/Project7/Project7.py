import feedparser
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# Function to extract content from a URL
def fetch_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.RequestException as e:
        return f"Error fetching {url}: {e}"

# Function to process RSS file
def process_rss_file(file_path, output_file):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: RSS file '{file_path}' does not exist.")
        return

    # Parse the RSS file
    feed = feedparser.parse(file_path)

    # Check if the file is empty or invalid
    if not feed.entries:
        print(f"Error: RSS file '{file_path}' is empty or invalid.")
        return

    # Extract links from RSS entries
    links = [entry.link for entry in feed.entries if 'link' in entry]

    if not links:
        print(f"No links found in the RSS feed.")
        return

    # Process links in parallel and write results to output file
    with open(output_file, "w", encoding="utf-8") as file:
        with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust number of threads if needed
            future_to_url = {executor.submit(fetch_content, url): url for url in links}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    content = future.result()
                    file.write(f"Content from {url}:\n{content}\n{'-' * 80}\n")
                except Exception as e:
                    file.write(f"Error processing {url}: {e}\n{'-' * 80}\n")

    print(f"Content extraction completed. Results saved in '{output_file}'.")

# Main function
if __name__ == "__main__":
    rss_file_path = "rss_feed.xml"  # Path to the RSS file
    output_file_path = "output.txt"  # Path to save the extracted content

    # Process the RSS file and extract content
    process_rss_file(rss_file_path, output_file_path)