import time

from config import URL
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class SauceDemo:
    def __init__(
            self,
            login: str,
            password: str,
            item: str,
            first_name: str,
            last_name: str,
            zip_code: str,
    ) -> None:
            self.login = login
            self.password = password
            self.item = item
            self.first_name = first_name
            self.last_name = last_name
            self.zip_code = zip_code


    def __login(self):
        l_field = self.driver.find_element(
            by=By.XPATH, value='//*[@id="user-name"]'
        )
        l_field.send_keys(self.login)
        time.sleep(3)
        password_field = self.driver.find_element(
            by=By.XPATH, value='//*[@id="password"]'
        )
        password_field.send_keys(self.password)
        time.sleep(3)
        login_button = self.driver.find_element(
            by=By.XPATH, value='//*[@id="login-button"]'
        )
        login_button.click()
        logging.info('Successfully login!')
        time.sleep(3)


    def __add_to_cart(self):
        item = self.driver.find_element(By.XPATH, f"//div[@class='inventory_item_name ' and text()='{self.item}']")
        # item = self.driver.find_element(By.XPATH, "//div[@class='inventory_item_name ' and text()='Sauce Labs Backpack']")
        add_to_cart_button = item.find_element(By.XPATH,
                                                  ".//ancestor::div[@class='inventory_item_description']//button[contains(text(), 'Add to cart')]")
        add_to_cart_button.click()
        logging.info('Successfully add to cart!')
        time.sleep(3)
        cart_button = self.driver.find_element(
            by=By.XPATH, value='//*[@id="shopping_cart_container"]/a'
        )
        cart_button.click()
        time.sleep(3)


    def __checkout(self):
        check_item = self.driver.find_element(By.XPATH, f"//div[@class='inventory_item_name' and text()='{self.item}']")
        if check_item:
            logging.info('Check item in cart - ok!')
            checkout_button = self.driver.find_element(
                by=By.XPATH, value='//*[@id="checkout"]'
            )
            checkout_button.click()
            time.sleep(3)
            first_name_field = self.driver.find_element(
                by=By.XPATH, value='//*[@id="first-name"]'
            )
            first_name_field.send_keys(self.first_name)
            time.sleep(1)
            last_name_field = self.driver.find_element(
                by=By.XPATH, value='//*[@id="last-name"]'
            )
            last_name_field.send_keys(self.last_name)
            time.sleep(1)
            zip_code_field = self.driver.find_element(
                by=By.XPATH, value='//*[@id="postal-code"]'
            )
            zip_code_field.send_keys(self.zip_code)
            time.sleep(1)
            submit_button = self.driver.find_element(
                by=By.XPATH, value='//*[@id="continue"]'
            )
            submit_button.click()
            time.sleep(1)
            logging.info('Order submited')
            finish_button = self.driver.find_element(
                by=By.XPATH, value='//*[@id="finish"]'
            )
            finish_button.click()
            logging.info('Finish')
            time.sleep(1)
        else:
            logging.error('Check item in cart - error!')


    def __check_order(self):
        check_element = self.driver.find_element(By.XPATH, "//div[@id='checkout_complete_container']/h2[text()='Thank you for your order!']")

        if check_element:
            logging.info('Finish Check - ok!')
        else:
            logging.error('Finish Check - NOT ok!')


    def __run_script(self):
        self.driver = webdriver.Chrome()
        self.driver.get(URL)
        time.sleep(3)
        logging.info('Open web-site')
        list_of_functions = [self.__login, self.__add_to_cart, self.__checkout, self.__check_order]
        for func in list_of_functions:
            attempts = 0
            while attempts < 5:
                try:
                    func()
                    time.sleep(1)
                    break
                except Exception as _e:
                    attempts += 1
                    logging.error(_e)
                    pass
            else:
                break


    def start(self):
        logging.info('Script started')
        self.__run_script()
        logging.info('Script finished.')
        self.__quit()


    def __quit(self):
        self.driver.quit()