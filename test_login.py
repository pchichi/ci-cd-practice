from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_login():
    driver = webdriver.Chrome()

    driver.get("http://127.0.0.1:5000")
    time.sleep(1)

    # 로그인 입력
    driver.find_element(By.NAME, "id").send_keys("admin")
    driver.find_element(By.NAME, "pw").send_keys("1234")

    # 로그인 버튼 클릭
    driver.find_element(By.TAG_NAME, "button").click()

    # 결과 확인
    assert "DASHBOARD" in driver.page_source

    driver.quit()