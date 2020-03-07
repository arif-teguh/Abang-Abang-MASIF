from django.test import TestCase
from selenium import webdriver
# Create your tests here.
from selenium.common.exceptions import WebDriverException


class fun_test(TestCase):
    def setUp(self):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='./chromedriver')

    def tearDown(self):
        self.driver.quit()
        super(fun_test, self).tearDown()

# This function is just to make sure that chromedriver is properly installed on gitlab pipeline
    def test_input_status_selenium(self):
        self.driver.get(url='http://localhost:8000/')
