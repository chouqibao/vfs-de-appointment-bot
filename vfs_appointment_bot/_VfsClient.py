import time
import logging
import datetime

from _ConfigReader import _ConfigReader
from _TwilioClient import _TwilioClient
from _TelegramClient import _TelegramClient

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class _VfsClient:

    def __init__(self):
        self._twilio_client = _TwilioClient()
        self._telegram_client = _TelegramClient()
        self._config_reader = _ConfigReader()

        self._use_telegram = self._config_reader.read_prop('DEFAULT', 'use_telegram')
        self._use_twilio = self._config_reader.read_prop('DEFAULT', 'use_twilio')
        logging.debug('Will use Telegram : {}'.format(self._use_telegram))
        logging.debug('Will use Twilio : {}'.format(self._use_twilio))

    def _init_web_driver(self):
        chrome_options = Options()

        # open in headless mode to run in background
        chrome_options.headless = True

        # following options reduce the RAM usage
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-application-cache')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
        self._web_driver = webdriver.Chrome(options=chrome_options)

        # make sure that the browser is full screen,
        # else some buttons will not be visible to selenium
        self._web_driver.maximize_window()

    def _login(self):
        _section_header = 'VFS'
        _email = self._config_reader.read_prop(_section_header, 'vfs_email')
        _password = self._config_reader.read_prop(_section_header, 'vfs_password')

        logging.debug('Logging in with email: {}'.format(_email))

        # logging in
        time.sleep(10)

        # sleep provides sufficient time for all the elements to get visible
        _email_input = self._web_driver.find_element(By.XPATH, '//input[@id="mat-input-0"]')
        _email_input.send_keys(_email)
        _password_input = self._web_driver.find_element(By.XPATH, '//input[@id="mat-input-1"]')
        _password_input.send_keys(_password)
        _login_button = self._web_driver.find_element(By.XPATH, '//button/span')
        _login_button.click()
        time.sleep(10)

    def _validate_login(self):
        try:
            _new_booking_button = self._web_driver.find_element(By.CSS_SELECTOR,
                                                                '.mat-focus-indicator.btn.mat-btn-lg.btn-brand-orange.mat-raised-button.mat-button-base')
            if _new_booking_button is None:
                logging.debug('Unable to login. VFS website is not responding')
                raise Exception('Unable to login. VFS website is not responding')
            else:
                logging.debug('Logged in successfully')
        except:
            logging.debug('Unable to login. VFS website is not responding')
            raise Exception('Unable to login. VFS website is not responding')

    def _get_appointment_date(self, visa_centre, category, sub_category):
        logging.info(
            'Getting appointment date: Visa Centre: {}, Category: {}, Sub-Category: {}'.format(visa_centre, category,
                                                                                               sub_category))
        # select from drop down
        _new_booking_button = self._web_driver.find_element(By.CSS_SELECTOR,
                                                            '.mat-focus-indicator.btn.mat-btn-lg.btn-brand-orange.mat-raised-button.mat-button-base')

        _new_booking_button.click()
        time.sleep(5)
        _visa_centre_dropdown = self._web_driver.find_element(By.XPATH, '//mat-form-field/div/div/div[3]')
        _visa_centre_dropdown.click()
        time.sleep(2)

        try:
            _visa_centre = self._web_driver.find_element(
                By.XPATH,
                '//mat-option[starts-with(@id,"mat-option-")]/span[contains(text(), "{}")]'.format(visa_centre)
            )
        except NoSuchElementException:
            raise Exception('Visa centre not found: {}'.format(visa_centre))

        logging.debug('VFS Centre: ' + _visa_centre.text)
        self._web_driver.execute_script('arguments[0].click();', _visa_centre)
        time.sleep(15)

        # read contents of the text box
        return self._web_driver.find_element(By.XPATH, '//div[4]/div')

    def check_slot(self, visa_centre, category, sub_category):
        self._init_web_driver()

        # open the webpage
        self.vfs_login_url = self._config_reader.read_prop('VFS', 'vfs_login_url')
        self._web_driver.get(self.vfs_login_url)

        self._login()
        self._validate_login()

        _message = self._get_appointment_date(visa_centre, category, sub_category)
        logging.debug('Message: ' + _message.text)

        if _message.text and 'No appointment slots are currently available' not in _message.text:
            logging.info('Appointment slots available: {}'.format(_message.text))
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            message = '{} at {}'.format(_message.text, st)
            if eval(self._use_telegram):
                self._telegram_client.send_message(message)
            if eval(self._use_twilio):
                self._twilio_client.send_message(message)
                self._twilio_client.call()
        else:
            logging.info('No appointment slots are currently available')
        # Close the browser
        self._web_driver.close()
        self._web_driver.quit()
