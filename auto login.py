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

mapelDetail = {} 
isAbsenTime = bool
totalAbsenHariIni = 0

locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
current_date = datetime.datetime.now()
formatted_time = current_date.strftime('%A - %H:%M')
today = current_date.strftime("%A")

def absen():
    options = Options()
    options.page_load_strategy = "eager"
    # options.add_argument('--headless=new')

    driver = Chrome(options= options)
    driver.get("http://elearning.bsi.ac.id")
    wait = WebDriverWait(driver, 10)

    isAbsenTime = False

    mapelDetail = {}
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
                
                if mapelDetail.get(child_value[:-14]) == None:
                    mapelDetail[child_value[:-14]] = child_value[-11:]
                else:
                    temp = mapelDetail[child_value[:-14]]
                    mapelDetail[child_value[:-14]] = [temp, child_value[-11:]]

                if sliced_value == 'Kamis - 07:30':
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
        
        return isAbsenTime, mapelDetail
    
    except Exception as e:
        print(f"Terjadi sebuah kesalahan: \n{e}")
        with open('logs.txt', 'a') as logs:
            logs.write(f'{sliced_value} \n {e} \n')
    finally:
        driver.quit()

if __name__ == '__main__':
    isAbsenTime, mapelDetail = absen()

if today in mapelDetail:
    for mapel, timeList in mapelDetail.items():
        if today == mapel:
            if isinstance(timeList, list):
                mapelLenght = len(timeList)
            else: 
                timeDetails = []
                timeDetails.append(timeList)
                mapelLenght = len(timeDetails)
    while totalAbsenHariIni < mapelLenght:
        totalAbsenHariIni += 1
else:
    time.sleep(86400)

def SleepUntil(target: list):
    pass