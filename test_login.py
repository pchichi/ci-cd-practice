import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import allure

# 1. 테스트 데이터 (함수보다 위에 있어야 합니다)
test_scenarios = [
    ("admin", "1234", "DASHBOARD", "정상_로그인"),
    ("wrong_user", "1234", "fail", "아이디_오류"),
    ("admin", "wrong_pw", "fail", "비밀번호_오류"),
    ("", "", "fail", "빈값_로그인"),
    ("admin'--", "1234", "fail", "SQL_인젝션_시도")
]

# 2. 공통 드라이버 설정
def setup_driver():
    options = Options()
    if os.environ.get('IS_CI') == 'true':
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

# 3. 파라미터화된 테스트 함수
@allure.feature("로그인 기능")
@allure.story("로그인 시나리오 검증")
@pytest.mark.parametrize("user_id, user_pw, expected_text, case_name", test_scenarios)
def test_login_logic(user_id, user_pw, expected_text, case_name):
    allure.dynamic.title(f"케이스: {case_name}")
    driver = setup_driver()
    
    try:
        with allure.step(f"{case_name} 실행: {user_id} / {user_pw}"):
            driver.get("http://127.0.0.1:5000")
            driver.find_element(By.NAME, "id").send_keys(user_id)
            driver.find_element(By.NAME, "pw").send_keys(user_pw)
            driver.find_element(By.TAG_NAME, "button").click()
            time.sleep(2)

        with allure.step(f"검증: {expected_text} 포함 여부 확인"):
            assert expected_text.lower() in driver.page_source.lower()

    except Exception as e:
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        screenshot_path = f"screenshots/fail_{case_name}.png"
        driver.save_screenshot(screenshot_path)
        # Allure 리포트에 스크린샷 직접 첨부
        allure.attach.file(screenshot_path, name=f"fail_{case_name}", attachment_type=allure.attachment_type.PNG)
        raise e
    finally:
        driver.quit()