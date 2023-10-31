from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with

from config import QIWI_LOGIN, QIWI_PASS


async def selenium_work(number: str):
    driver = webdriver.Firefox()
    try:
        driver.get('https://qiwi.com/payment/form/870')
        
        #Try Log in
        sign_in_wait = WebDriverWait(driver, timeout=20)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                            '//span[contains(text(), "Войти")]')))
        
        sign_in_wait.click()

        form_wait = WebDriverWait(driver, timeout=20)\
            .until(lambda el: el.find_element(By.XPATH,
                                            '//form[starts-with(@class, "auth-form")]'))

        phone, password = form_wait.find_elements(By.TAG_NAME, 'input')

        phone.send_keys(QIWI_LOGIN)
        password.send_keys(QIWI_PASS)

        form_wait.find_element(By.TAG_NAME, 'button').click()

        #After Log in

        invise_el = WebDriverWait(driver, timeout=10)\
        .until(EC.invisibility_of_element_located((By.XPATH, '//div[starts-with(@class, "center-loader-progress")]')))
        radio_wait = WebDriverWait(driver, timeout=20)\
        .until(EC.visibility_of_element_located((By.XPATH,
                                            '//div[contains(text(), "Номер телефона")]'))).click()

        driver.find_element(By.XPATH,
                            '//input[starts-with(@class, "mask-text-input-form")]').send_keys(number)

        try: 
            before_receiver_wait = WebDriverWait(driver, timeout=5)\
                .until(lambda el: el.find_element(By.XPATH,
                                                '//div[contains(text(), "Получатель")]'))
        except TimeoutException:
            try:
                driver.find_element(By.XPATH, '//div[starts-with(@class, "ref-message")]')
            except NoSuchElementException:
                return 'Отсутствует'
            else:
                return 'Ошибка\nНа сайте что то пошло не так.'

        receiver = driver.find_element(locate_with(By.TAG_NAME, "div").near(before_receiver_wait))

        _, name = receiver.text.split('\n')

        return name
    
    finally:
        driver.quit()