from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from user import user
import locale
import datetime
import time

def login():
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
    current_date = datetime.datetime.now()
    formatted_time = current_date.strftime('%A - %H:%M')

    options = Options()
    options.page_load_strategy = "eager"
    options.add_argument("--headless")

    driver = Chrome()
    driver.get("http://elearning.bsi.ac.id")
    wait = WebDriverWait(driver, 5)

    isLoginTime = False

    print(formatted_time)

    try:
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Masuk"))).click()
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(user[1].nim)
        wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(user[1].password)
        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div[2]/div/div[2]/form/div[3]/button"))).click()

        wait.until(EC.element_to_be_clickable((By.ID, "pin-sidebar"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"sidebar\"]/div/div[1]/div/ul/li[4]"))).click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Jadwal Kuliah"))).click()

        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pricing-plan")))
        for element in elements:
            try:
                child_element = element.find_element(By.CSS_SELECTOR, ".pricing-save")

                child_value = child_element.text
                sliced_value = child_value[:-6]
                print(sliced_value)
                if sliced_value == formatted_time:
                    element.find_element(By.CSS_SELECTOR, ".pricing-footer").find_element(By.LINK_TEXT, "Masuk Kelas").click()
                    isLoginTime = True
            except StaleElementReferenceException:
                break
    
        if isLoginTime == True:
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[5]/div/center/button"))).click()
        else:
            print("Belum Saatnya untuk login")

    except Exception as e:
        print(f"Terjadi sebuah kesalahan: \n{e}")
    finally:
        driver.quit()

while True:
    login()
    time.sleep(1800)