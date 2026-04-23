from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options # 👈 추가
import time
import os # 👈 환경 변수 확인을 위해 추가

def test_login():
    # 1. 크롬 옵션 객체 생성
    options = Options()

    # 2. CI 환경(GitHub Actions)인지 체크해서 Headless 설정 주입
    # (아까 test.yml에 IS_CI: "true"를 넣기로 했으니 그걸 읽어옵니다)
    if os.environ.get('IS_CI') == 'true':
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

    # 3. 옵션을 적용해서 브라우저 실행
    driver = webdriver.Chrome(options=options)

    # --- 여기서부터는 윤지님의 기존 로직과 동일합니다 ---
    driver.get("http://127.0.0.1:5000")
    time.sleep(1)

    driver.find_element(By.NAME, "id").send_keys("admin")
    driver.find_element(By.NAME, "pw").send_keys("1234")

    driver.find_element(By.TAG_NAME, "button").click()

    time.sleep(2) # 👈 페이지 전환 대기 시간 살짝 추가

    assert "DASHBOARD" in driver.page_source

    driver.quit()

    ' 메ㅗㄹ올ㅇ 메롱ㄹ올 '