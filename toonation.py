from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import asyncio

options = Options()
options.add_argument("--headless=new")
browser = webdriver.Firefox(options=options)
toonation_url = "https://toon.at/widget/alertbox/{주소}" # 투네이션 후원창 주소입력

browser.get(toonation_url)

async def find():
    global running
    global bef_name
    global bef_content
    try:
        element = browser.find_elements(By.XPATH,"//span[@class='template-animated-text animated infinite pulse ']")
        content = browser.find_element(By.XPATH,"//div[@class='template-content']")
    except NoSuchElementException:
        print("후원이 감지되지 않았습니다.")
        running = True
    else:
        if running:
            try:
                print(f"후원내역 / 후원자 닉네임 - {element[0].text} 후원 금액 - {element[1].text} 후원 내용 - {content.text}")
            except StaleElementReferenceException:
                return 0
            running = False
            bef_name = element[0].text
            bef_content = content.text
        elif bef_name != element[0].text or bef_content != content.text: # 후원이 연속되는경우 먹히는걸 방지
            try:
                print(f"후원내역 / 후원자 닉네임 - {element[0].text} 후원 금액 - {element[1].text} 후원 내용 - {content.text}")
            except StaleElementReferenceException:
                return 0
            running = False
            bef_name = element[0].text
            bef_content = content.text
    await asyncio.sleep(1) # 감지 빈도
    await find()

asyncio.run(find())
