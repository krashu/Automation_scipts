from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


def cancel(domain, reservation_id, folder, email='L2ConsumerAppSupport@abg.com'):
    try:
        options = Options()
        # options.add_argument("--start-maximized")
        print()
        print('Cancelling reservation ....')
        options.add_argument("--window-size=1280x720")
        options.add_argument('log-level=3')
        options.add_argument('headless')

        # log-level: Sets the minimum log level.
        # Valid values are from 0 to 3:
        # 	INFO = 0,
        #     WARNING = 1,
        #     LOG_ERROR = 2,
        #     LOG_FATAL = 3.
        # default is 0.

        # Remove "DevTools listening log"
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        screenshot_name = domain.strip()
        screenshot_name = screenshot_name.split('www')[-1].replace('.', '_').replace('/', '')

        driver = webdriver.Chrome(options=options)
        driver.get(domain)

        # driver.maximize_window()
        # driver.set_window_size(1024, 768)
        wait = WebDriverWait(driver, 30)
        wait.until(EC.element_to_be_clickable((By.ID, 'consent_prompt_accept'))).click()

        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="supp_nav_booking"]'))).click()

        driver.find_element(By.XPATH, '//*[@id="InputBookingNumber"]').send_keys(reservation_id)

        driver.find_element(By.XPATH, '//*[@id="InputSurname"]').send_keys('Test')

        driver.find_element(By.XPATH, '//*[@id="InputEmailAddress"]').send_keys(email)

        driver.find_element(By.XPATH, '//*[@id="findbook_btn"]').click()

        # wait.until(EC.url_contains('yourBooking'))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="confirm-cancel-button"]'))).click()

        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cancelBookingLink"]'))).click()

        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="survey-close"]/i'))).click()
        except:
            # print('Cancellation survey not coming.')
            pass

        cancel_confirmed = wait.until(
            EC.visibility_of(driver.find_element(By.XPATH, '//*[@id="content"]//tbody/tr[1]/td')))
        if cancel_confirmed.text == reservation_id:
            print('Reservation cancelled successfully')
            driver.get_screenshot_as_file(f"{folder}\\cancellation{screenshot_name}.png")
            # time.sleep(3)

            return 'Cancelled'
        else:
            print("Not cancelled " + cancel_confirmed.text)
            driver.get_screenshot_as_file(f"{folder}\\cancellation{screenshot_name}.png")
            # time.sleep(3)

            return 'Active'
    except Exception as e:
        # print(e)
        print('~' * 50)
        print('Reservation Not created for ', domain)
        error_path = folder + '\\error'
        if not os.path.exists(error_path):
            os.mkdir(error_path)
        driver.get_screenshot_as_file(f"{error_path}\\error{screenshot_name}.png")
    finally:
        # time.sleep(10)
        driver.quit()


if __name__ == '__main__':
    print(cancel('https://www.avis.com.tn/', '2310-4422-FR-5'))