# Scrape Behind Login

A Python script that demonstrates how to scrape content from behind a login wall using Selenium WebDriver and leverage OpenAI's GPT model to extract specific information from the scraped content.

Sponsored by [datafuel.dev](https://datafuel.dev) - Turn Websites into LLM-Ready Data.

## Features

- Automated login to web applications using Selenium
- Cookie management for maintaining session state
- Headless browser operation
- Integration with OpenAI's GPT model for intelligent content extraction

## Prerequisites

- Python 3.6+
- Chrome browser
- ChromeDriver
- Required Python packages:
  - selenium
  - requests
  - openai

## Installation

1. Install the required system packages:
```bash
apt-get update
apt install chromium-chromedriver
cp /usr/lib/chromium-browser/chromedriver /usr/bin
```

2. Install the required Python packages:
```bash
pip install selenium requests openai
```

3. Set up ChromeDriver in your system path:
```python
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
```

## Configuration

Before running the script, you need to configure the following:

1. OpenAI API Key:
   - Replace `<sk-proj->` with your OpenAI API key
   ```python
   client = OpenAI(api_key="your-api-key-here")
   ```

2. Login Credentials:
   - Replace `<email>` with your login email
   - Replace `<password>` with your login password
   ```python
   email_input.send_keys("your-email@example.com")
   password_input.send_keys("your-password")
   ```

## Usage

To run the script:
```bash
python scrape.py
```

## Key Components

### Cookie Management
```python
def save_cookies(driver):
    cookies = driver.get_cookies()
    cookie_dict = {}
    for cookie in cookies:
        cookie_dict[cookie['name']] = cookie['value']
    return cookie_dict
```

### AI-Powered Content Extraction
```python
def extract_api_key_using_ai(response_text):
    prompt = """
    You are an expert scraper, and you will extract only the information asked from the context.
    I need the value of my api-key from the following context:
    {response_text}
    """
    # ... AI processing logic
```

## Best Practices

1. Adjust sleep timers based on page load times:
```python
time.sleep(5)  # Adjust based on site response time
```

2. Implement proper error handling:
```python
try:
    # Your scraping logic
finally:
    driver.quit()  # Always close the browser
```

3. Use headless mode for production:
```python
chrome_options.add_argument('--headless')
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

Ensure you have permission to scrape target websites and comply with their terms of service. This tool is for educational purposes only.
