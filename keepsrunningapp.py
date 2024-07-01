from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def monitor_website(url, interval=3):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)  # Initialize Chrome WebDriver

    try:
        while True:
            try:
                driver.get(url)  # Load the URL in the headless browser
                # Optionally, you can add assertions or checks here to verify content or functionality
                print(f"Successfully rendered {url}")
            except Exception as e:
                print(f"Error rendering {url}: {str(e)}")

            time.sleep(interval)  # Adjust this interval (in seconds) as needed

    finally:
        driver.quit()  # Quit the WebDriver when done

if __name__ == "__main__":
    website_url = "https://payslips.onrender.com/"
    monitor_website(website_url)
