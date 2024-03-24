# Import necessary modules
from selenium import webdriver
import time
import json
import os

# Function to load configuration from a JSON file
def load_config():
    with open('config.json') as f:
        return json.load(f)

# Function to activate certain features on a network device 
def ActivateKP(username, password, edge_path):
    
    # Configure Microsoft Edge options
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument("ignore-certificate-errors")

    # Specify capabilities
    capabilities = {
        'acceptInsecureCerts': True
    }

    # Initialize Edge WebDriver with specified options and capabilities
    driver = webdriver.Edge(executable_path=edge_path, options=edge_options, capabilities=capabilities)
    
    # Open login page of the device
    driver.get("https://192.168.1.1/html/login_pldt.html")

    # Find username input field and enter username
    username_input = driver.find_element_by_id("user_name")
    username_input.send_keys(username)

    # Find password input field and enter password
    password_input = driver.find_element_by_id("loginpp")
    password_input.send_keys(password)
    time.sleep(1)

    # Find login button and click to login
    login_button = driver.find_element_by_id("login_btn")
    login_button.click()
    time.sleep(5)

    # Navigate to firewall settings page
    driver.get("https://192.168.1.1/html/firewall_enable_inter.html")

    # Select firewall medium level
    radio_button = driver.find_element_by_id("firewall_medium")
    radio_button.click()
    time.sleep(1)

    # Apply firewall settings
    apply_button = driver.find_element_by_xpath("//input[@type='button' and @value='Apply']")
    apply_button.click()
    time.sleep(1)

    # Navigate to parental control settings page
    driver.get("https://192.168.1.1/html/parental_control_inter.html")

    # Enable parental control
    radio_button = driver.find_element_by_xpath("//input[@type='radio' and @name='parent_control_enable' and @value='1']")
    radio_button.click()
    time.sleep(1)

    # Apply parental control settings
    apply_button = driver.find_element_by_xpath("//input[@type='button' and @value='Apply']")
    apply_button.click()

    # Close the WebDriver
    driver.quit()

# Function to deactivate certain features on a network device
def DeactivateKP(username, password, edge_path):

    # Similar to ActivateKP function, but with different actions to deactivate features
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument("ignore-certificate-errors")

    capabilities = {
        'acceptInsecureCerts': True
    }

    driver = webdriver.Edge(executable_path=edge_path, options=edge_options, capabilities=capabilities)

    driver.get("https://192.168.1.1/html/login_pldt.html")

    username_input = driver.find_element_by_id("user_name")
    username_input.send_keys(username)


    password_input = driver.find_element_by_id("loginpp")
    password_input.send_keys(password)
    time.sleep(1)

    login_button = driver.find_element_by_id("login_btn")
    login_button.click()
    time.sleep(5)

    driver.get("https://192.168.1.1/html/firewall_enable_inter.html")

    radio_button = driver.find_element_by_id("firewall_low")
    radio_button.click()
    time.sleep(1)

    apply_button = driver.find_element_by_xpath("//input[@type='button' and @value='Apply']")
    apply_button.click()

    time.sleep(1)
    driver.get("https://192.168.1.1/html/parental_control_inter.html")


    radio_button = driver.find_element_by_xpath("//input[@type='radio' and @name='parent_control_enable' and @value='0']")
    radio_button.click()
    time.sleep(1)
    apply_button = driver.find_element_by_xpath("//input[@type='button' and @value='Apply']")
    apply_button.click()
    driver.quit()

# Function to clear the terminal screen
def clear_terminal():
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display a menu for user interaction
def display_menu():
    # Clear the terminal screen
    clear_terminal()

    # Display menu options
    print("""
-------------------------------------------------------------------------------- 

  _____   _____    ____        _  ______  _____  _______            _  __ _____  
 |  __ \ |  __ \  / __ \      | ||  ____|/ ____||__   __|          | |/ /|  __ \ 
 | |__) || |__) || |  | |     | || |__  | |        | |     ______  | ' / | |__) |
 |  ___/ |  _  / | |  | | _   | ||  __| | |        | |    |______| |  <  |  ___/ 
 | |     | | \ \ | |__| || |__| || |____| |____    | |             | . \ | |     
 |_|     |_|  \_\ \____/  \____/ |______|\_____|   |_|             |_|\_\|_|     
                                                                                 
--------------------------------------------------------------------------------              
""")
    print("1. Activate")
    print("2. Deactivate")
    print("3. Exit")
    print("")

# Main function 
def main():
    # Load configuration from config.json
    config = load_config()

    while True:
        # Display menu
        display_menu()

        # Prompt user for choice
        choice = input("Enter your choice: ")

        if choice == '1':
            # Activate feature
            ActivateKP(config['username'], config['password'], config['edge_path'])
        elif choice == '2':
            # Deactivate feature
            DeactivateKP(config['username'], config['password'], config['edge_path'])
        elif choice == '3':
            # Exit program
            print("Exiting the program.")
            break
        else:
            # Invalid choice
            print("Invalid choice. Please enter a valid option (1, 2, or 3).")

# Entry point of the script
if __name__ == "__main__":
    main()