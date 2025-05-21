from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import time
import os
from dotenv import load_dotenv

# Ielādē .env failu
load_dotenv()

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"WebDriver kļūda: {e}")
        return None

def login_to_ortus():
    driver = setup_driver()
    if not driver:
        return None

    try:
        driver.get("https://id2.rtu.lv/openam/UI/Login?locale=lv&goto=https%3A%2F%2Festudijas.rtu.lv")
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "IDToken1"))
        ).send_keys(os.getenv("RTU_LOGIN"))
        
        driver.find_element(By.ID, "IDToken2").send_keys(os.getenv("RTU_PASSWORD"))
        driver.find_element(By.NAME, "Login.Submit").click()

        WebDriverWait(driver, 15).until(
            EC.url_contains("estudijas.rtu.lv")
        )
        return driver

    except Exception as e:
        print(f"Pieslēgšanās kļūda: {e}")
        return None

def parse_deadlines(driver):
    try:
        driver.get("https://estudijas.rtu.lv/my/")
        time.sleep(3)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "td.day.hasevent"))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        deadlines = []

        days = soup.select('td.day.hasevent')
        
        for day in days:
            try:
                day_number = int(day['data-day'])
                current_year = datetime.datetime.now().year
                current_month = datetime.datetime.now().month
                deadline_date = datetime.datetime(current_year, current_month, day_number)
                
                events = day.select('li[data-region="event-item"]')
                
                for event in events:
                    event_name = event.select_one('.eventname').get_text(strip=True)
                    deadlines.append({
                        'date': deadline_date,
                        'task': event_name
                    })
                    
            except (KeyError, ValueError, AttributeError) as e:
                continue

        return deadlines

    except Exception as e:
        print(f"Analīzes kļūda: {e}")
        return []

def check_upcoming_deadlines(deadlines):
    today = datetime.datetime.now()
    upcoming = []

    for deadline in deadlines:
        days_left = (deadline['date'] - today).days
        if 0 <= days_left <= 7:
            upcoming.append(deadline)

    return upcoming

def console_notification(deadline):
    days_left = (deadline['date'] - datetime.datetime.now()).days
    print(f"\n=== ATGĀDINĀJUMS ===")
    print(f"Uzdevums: {deadline['task']}")
    print(f"Termiņš: {deadline['date'].strftime('%d.%m.%Y')}")
    print(f"Atlikušas dienas: {days_left}")
    print("===================\n")

if __name__ == "__main__":
    print("Sāk darbu...")
    driver = login_to_ortus()
    
    if not driver:
        print("Nevarēja pieslēgties. Pārbaudiet:")
        print("1. Vai .env fails satur pareizos datus")
        print("2. Vai interneta savienojums darbojas")
        exit()

    print("Veiksmīgi pieslēgties, iegūstam datus...")
    deadlines = parse_deadlines(driver)
    driver.quit()

    upcoming = check_upcoming_deadlines(deadlines)

    if not upcoming:
        print("Tuvāko termiņu nav atrasts.")
    else:
        print(f"Atrasti {len(upcoming)} termiņi:")
        for task in upcoming:
            console_notification(task)

    print("Darbība pabeigta!")
