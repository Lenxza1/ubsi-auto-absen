from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from user import user
import locale
from datetime import datetime
import re
import time

mapelDetail = []
isAbsenTime = bool
totalAbsenHariIni = 0

locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
current_date = datetime.now()
formatted_time = current_date.strftime('%A - %H:%M')
today = current_date.strftime("%A")

def absen():
    options = Options()
    # options.add_argument('--headless=new')

    driver = Chrome(options= options)
    driver.get("http://elearning.bsi.ac.id")
    wait = WebDriverWait(driver, 10)

    isAbsenTime = False

    sliced_value = []
    try:
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Masuk"))).click()
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(user[1].nim)
        wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(user[1].password)
        captcha_question = wait.until(EC.presence_of_element_located((By.ID, "captcha_question")))
        captcha_question = captcha_question.text
        match = re.search(r'(\d+)\s*(\+)\s*(\d+)', captcha_question)
        captcha_answer = int(match.group(1)) + int(match.group(3))
        wait.until(EC.presence_of_element_located((By.ID, "captcha_answer"))).send_keys(captcha_answer)
        
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

        wait.until(EC.element_to_be_clickable((By.ID, "pin-sidebar"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Jadwal']"))).click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Jadwal Kuliah"))).click()

        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pricing-plan")))
        for element in elements:
            try:
                child_element = element.find_element(By.CSS_SELECTOR, ".pricing-save")
                child_value = child_element.text

                sliced_value.append(child_value[:-6])

                if sliced_value == formatted_time:
                    element.find_element(By.CSS_SELECTOR, ".pricing-footer").find_element(By.LINK_TEXT, "Masuk Kelas").click()
                    isAbsenTime = True
            except StaleElementReferenceException:
                break     

        if isAbsenTime == True:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.btn-rounded.left"))).click()
            with open('logs.txt', 'a', newline='\n') as logs:
                logs.write(f"{sliced_value}\n Sukses Absen \n")
        else:
            print("Belum Saatnya untuk Absen")
            with open('logs.txt', 'a') as logs:
                logs.write(f'{sliced_value}\n Belum saatnya untuk absen \n')
        
        return sliced_value
    
    except Exception as e:
        print(f"Terjadi sebuah kesalahan: \n{e}")
        with open('logs.txt', 'a') as logs:
            logs.write(f'{sliced_value} \n {e} \n')
    finally:
        driver.quit()

def SleepUntil(targets):
    deltas = []
    for i in range(len(targets)):
        target = datetime.strptime((targets[i]).title(), '%A - %H:%M')
        deltas.append((target - datetime.strptime(formatted_time, '%A - %H:%M')).total_seconds())

    deltas.sort()
    for delta in deltas:
        print(delta)

mapelDetail = absen()

SleepUntil(mapelDetail)