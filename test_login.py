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
    try:
        driver.get("http://127.0.0.1:5000")
        time.sleep(1)

        driver.find_element(By.NAME, "id").send_keys("admin")
        driver.find_element(By.NAME, "pw").send_keys("1234")
        driver.find_element(By.TAG_NAME, "button").click()

        time.sleep(2)

        # 검증 (일부러 틀리게 바꿔서 스크린샷이 찍히는지 테스트해보세요!)
        # assert "WRONG_TEXT" in driver.page_source 
        assert "DASHBOARD_failed" in driver.page_source

    except Exception as e:
        # 에러가 나면 screenshots 폴더를 만들고 스크린샷 저장
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        driver.save_screenshot("screenshots/failure_log.png")
        
        # 스크린샷을 찍은 후, 원래 발생했던 에러를 다시 던져서 테스트가 실패하게 만듭니다.
        raise e
        
    finally:
        # 성공하든 실패하든 브라우저는 꼭 닫아줍니다.
        driver.quit()
