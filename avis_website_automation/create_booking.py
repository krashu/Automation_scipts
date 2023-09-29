from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.relative_locator import locate_with
import time
from datetime import datetime


def create_reservation(domain, folder, email='appdev681@gmail.com'):
    options = Options()
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
    try:
        print('Creating reservation for ' + domain)
        driver = webdriver.Chrome(options=options)
        driver.get(domain)

        # driver.maximize_window()
        wait = WebDriverWait(driver, 30)

        wait.until(EC.element_to_be_clickable((By.ID, 'consent_prompt_accept'))).click()

        # extra pop up on avis.ee

        # if domain.strip() == 'https://www.avis.ee/':

        search_box = driver.find_element(By.XPATH, '//*[@id="hire-search"]')
        wait.until(EC.element_to_be_clickable(search_box)).send_keys('LHR')

        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="getAQuote"]//ul/li/button'))).click()

        wait.until(EC.element_to_be_clickable((By.ID, "date-from-display"))).click()

        from_date = driver.find_elements(By.XPATH, '//*[@id="getAQuote"]//table/tbody/tr[3]/td[1]/button[last()]')
        wait.until(EC.element_to_be_clickable(from_date[1])).click()

        submit_btns = driver.find_elements(By.XPATH, '//*[@class="standard-form__submit"][last()]')
        find_cars = submit_btns[3]
        wait.until(EC.element_to_be_clickable(find_cars)).click()

        ## Car result page
        wait.until(EC.invisibility_of_element((By.XPATH, '//*[@class="nysLoading"]')))
        links = driver.find_elements(By.XPATH, '//*[@id="gridview"]//a')
        first_car = links[0]
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable(first_car)).click()

        payreview_btns = driver.find_elements(By.XPATH, '//*[@id="payreviewModal"]//a')

        if len(payreview_btns):
            wait.until(EC.element_to_be_clickable(payreview_btns[0])).click()

        ## Coverage Page
        # wait.until(EC.url_contains('coverage'))
        wait.until(EC.invisibility_of_element((By.XPATH, '//*[@class="nysLoading"]')))
        coverage_footer = driver.find_elements(By.XPATH, '//*[@id="content"]/footer')
        submit_coverage = driver.find_elements(By.XPATH, '//*[@id="submitCoverageLink"]')
        if len(submit_coverage):
            coverage_footer = wait.until(EC.element_to_be_clickable(coverage_footer[0]))
            ActionChains(driver) \
                .scroll_to_element(coverage_footer) \
                .perform()

            wait.until(EC.element_to_be_clickable(submit_coverage[0])).click()

        ## Extras Page
        # wait.until(EC.url_contains('car-extras'))
        extras_footer = driver.find_element(By.XPATH, '//*[@id="content"]/footer')
        ActionChains(driver) \
            .scroll_to_element(extras_footer) \
            .perform()

        submit_review_pay = driver.find_elements(By.XPATH, '//*[@id="submitReviewPay"]')

        wait.until(EC.element_to_be_clickable(submit_review_pay[0])).click()
        # driver.execute_script('document.querySelector("#submitReviewPay").click();')

        ## Pay and review page
        extras_paypage_btns = driver.find_elements(By.XPATH, '//*[@id="extras-form"]//button')
        if len(extras_paypage_btns):
            wait.until(EC.element_to_be_clickable(extras_paypage_btns[-1])).click()

        title = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="title"]')))
        Select(title).select_by_index(1)

        driver.find_element(By.ID, "firstname").send_keys("Test")
        driver.find_element(By.ID, "lastname").send_keys("Test")
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "confirm-email").send_keys(email)
        select_phone_code = Select(driver.find_element(By.XPATH, '//*[@id="phone-prefix"]'))
        select_phone_code.select_by_value('GB')
        driver.find_element(By.ID, "phone").send_keys("7000000000")
        driver.find_element(By.ID, "addr1").send_keys("test")
        driver.find_element(By.ID, "city").send_keys("test")
        driver.find_element(By.ID, "postcode").send_keys("test")

        driver.find_element(By.XPATH, '//*[@alt="Avis Charge Card"]').click()
        # driver.find_element(By.XPATH, '//*[@id="review-and-pay"]/div/div/div/fieldset[4]/div[5]/div[1]/ul/li/label').click()

        driver.execute_script('document.querySelector("#terms-and-conditions").click();')

        pay_footer = driver.find_element(By.XPATH, '/html/body//footer')
        ActionChains(driver) \
            .scroll_to_element(pay_footer) \
            .perform()

        confirm_booking = driver.find_elements(By.CSS_SELECTOR, '.pNrSubmit > .standard-form__submit')[0]
        ActionChains(driver) \
            .move_to_element(confirm_booking) \
            .click(confirm_booking) \
            .perform()
        # wait.until(EC.element_to_be_clickable(confirm_booking)).click()

        ## Confirmation Page
        # wait.until(EC.url_contains('car-confirmation'))
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="survey-close"]'))).click()
        except:
            # print('Survey not coming')
            pass

        reservation_id = None
        reservation_id = wait.until(
            EC.visibility_of(driver.find_element(By.XPATH, '//*[@id="content"]//section/header/p'))).text
        hr_tag = driver.find_element(By.XPATH, '//*[@id="content"]//hr')
        ActionChains(driver) \
            .scroll_to_element(hr_tag) \
            .perform()

        driver.get_screenshot_as_file(f"{folder}\\reservation{screenshot_name}.png")
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
        print('Reservation id - ', reservation_id)
    return reservation_id


if __name__ == "__main__":
    print(create_reservation('http://www.avis.co.uk/'))
