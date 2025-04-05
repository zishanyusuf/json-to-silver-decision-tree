from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

def capture_silver_decision_diagram():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Set up download directory to current working directory
    current_dir = os.getcwd()
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': current_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    })
    
    # Initialize the driver with options
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to Silver Decisions
        driver.get("https://silverdecisions.pl/SilverDecisions.html?lang=en")
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        
        # Click on Open Diagram button
        open_button = wait.until(EC.element_to_be_clickable((By.ID, "open-diagram-button")))
        driver.execute_script("arguments[0].click();", open_button)
        
        # Wait for and handle the confirmation popup
        time.sleep(1)
        alert = wait.until(EC.alert_is_present())
        alert.accept()
        
        # Get absolute path of the JSON file
        json_path = os.path.abspath("reroll_game.json")
        print(f"Looking for JSON file at: {json_path}")
        
        # Verify file exists
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"JSON file not found at {json_path}")
        
        # Find file input and send the file
        file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
        file_input.send_keys(json_path)
        
        # Wait for the diagram to load
        time.sleep(3)
        
        try:
            # Click the save button to download the image
            save_button = wait.until(EC.element_to_be_clickable((By.ID, "saveButton")))
            driver.execute_script("arguments[0].click();", save_button)
            
            # Wait for download to complete
            time.sleep(3)
            print("Diagram has been downloaded successfully")
            
        except Exception as inner_e:
            print(f"Error while downloading diagram: {str(inner_e)}")
            raise
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Error details:", e.__class__.__name__)
        import traceback
        traceback.print_exc()
        
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    capture_silver_decision_diagram()
