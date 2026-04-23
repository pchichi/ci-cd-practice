import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

import allure

@allure.feature("로그인 기능")
@allure.story("비유효 계정 로그인 시도")
@pytest.mark.parametrize("user_id, user_pw, expected_text, case_name", test_scenarios)
def test_login_logic(user_id, user_pw, expected_text, case_name):
    allure.dynamic.title(f"테스트 케이스: {case_name}")
    # ... 기존 로직 ...


# 1. 공통 드라이버 설정 (고정)
def setup_driver():
    options = Options()
    if os.environ.get('IS_CI') == 'true':
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

# 2. [핵심] 테스트 데이터 관리
# 형식: (아이디, 패스워드, 기대하는 결과 키워드, 테스트 케이스 이름)
test_scenarios = [
    ("admin", "1234", "DASHBOARD", "정상_로그인"),
    ("wrong_user", "1234", "fail", "아이디_오류"),
    ("admin", "wrong_pw", "fail", "비밀번호_오류"),
    ("", "", "fail", "빈값_로그인"),
    ("admin'--", "1234", "fail", "SQL_인젝션_시도")
]

# 3. 파라미터화된 테스트 함수
@pytest.mark.parametrize("user_id, user_pw, expected_text, case_name", test_scenarios)
def test_login_logic(user_id, user_pw, expected_text, case_name):
    driver = setup_driver()
    print(f"\n실행 중인 케이스: {case_name}")
    
    try:
        driver.get("http://127.0.0.1:5000")
        
        # 데이터 세트의 값을 입력
        driver.find_element(By.NAME, "id").send_keys(user_id)
        driver.find_element(By.NAME, "pw").send_keys(user_pw)
        driver.find_element(By.TAG_NAME, "button").click()
        
        time.sleep(2)

        # 검증 (대소문자 구분 없이 확인)
        assert expected_text.lower() in driver.page_source.lower()

    except Exception as e:
        # 실패 시 케이스명을 파일명으로 해서 스크린샷 저장
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        driver.save_screenshot(f"screenshots/fail_{case_name}.png")
        raise e
    finally:
        driver.quit()