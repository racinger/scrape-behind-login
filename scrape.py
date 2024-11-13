import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
from openai import OpenAI

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Initialize OpenAI client
client = OpenAI(api_key="<sk-proj->") # replace with your own OPENAI API key


def save_cookies(driver):
    """Save cookies from the Selenium WebDriver into a dictionary."""
    cookies = driver.get_cookies()
    cookie_dict = {}
    for cookie in cookies:
        cookie_dict[cookie['name']] = cookie['value']
    return cookie_dict


def extract_api_key_using_ai(response_text):
    """Use OpenAI's GPT model to extract the API key."""
    prompt = f"""
    You are an expert scraper, and you will extract only the information asked from the context.
    I need the value of my api-key from the following context:

    {response_text}
    """

    try:
        # Use OpenAI client to create a chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",  # You can change to gpt-4 if needed
        )

        # Extract the response from the AI
        extracted_api_key = chat_completion.choices[0].message.content
        return extracted_api_key

    except Exception as e:
        print(f"An error occurred with OpenAI API: {e}")
        return None


def scrape_api_key(cookies):
    """Use cookies to scrape the /account/api_key page."""
    url = 'https://app.scrapewebapp.com/account/api_key'

    # Set up the session to persist cookies
    session = requests.Session()

    # Add cookies from Selenium to the requests session
    for name, value in cookies.items():
        session.cookies.set(name, value)

    # Make the request to the /account/api_key page
    response = session.get(url)

    # Check if the request is successful
    if response.status_code == 200:
        print("API Key page content retrieved.")
        response_text = response.text  # Capture the page content

        # Now, use AI to extract the API key
        api_key = extract_api_key_using_ai(response_text)

        # Print the extracted API key
        if api_key:
            print(f"Extracted API Key: {api_key}")
        else:
            print("Failed to extract API key.")
    else:
        print(f"Failed to retrieve API key page, status code: {response.status_code}")


try:
    # Open the login page
    driver.get("https://app.scrapewebapp.com/login")

    # Find the email input field by ID and input your email
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys("<email>") # replace with your own credentials

    # Find the password input field by ID and input your password
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("<password>") # replace with your own credentials

    # Find the login button and submit the form
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Wait for the login process to complete
    time.sleep(5)  # Adjust this depending on your site's response time

    # Save the cookies from the WebDriver
    cookies = save_cookies(driver)

    # Now use the cookies to scrape the API key page
    scrape_api_key(cookies)

finally:
    # Close the browser
    driver.quit()
