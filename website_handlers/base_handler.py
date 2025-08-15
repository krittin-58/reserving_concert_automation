"""Base class for website handlers"""

from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep
import json


class BaseTicketHandler(ABC):
    def __init__(self, driver, config, user_details):
        self.driver = driver
        self.config = config
        self.user_details = user_details
        self.wait = WebDriverWait(driver, 30)
        
    @abstractmethod
    def login(self):
        """Login to the website"""
        pass
    
    @abstractmethod
    def search_concert(self):
        """Search for the specified concert"""
        pass
    
    @abstractmethod
    def select_show(self):
        """Select the show/round"""
        pass
    
    @abstractmethod
    def select_zone(self):
        """Select the seating zone"""
        pass
    
    @abstractmethod
    def select_seats(self):
        """Select the seats"""
        pass
    
    @abstractmethod
    def confirm_booking(self):
        """Confirm the booking"""
        pass
    
    def setup(self):
        """Setup the browser and navigate to website"""
        self.driver.maximize_window()
        self.driver.get(self.config["base_url"])
        self.driver.implicitly_wait(30)
    
    def find_element_safe(self, by, value, timeout=10):
        """Safely find element with timeout"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"Element not found: {value}")
            return None
    
    def click_element_safe(self, by, value, timeout=10):
        """Safely click element with timeout"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return True
        except TimeoutException:
            print(f"Element not clickable: {value}")
            return False
    
    def wait_for_url_change(self, current_url, timeout=30):
        """Wait for URL to change from current URL"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.current_url != current_url
            )
            return True
        except TimeoutException:
            return False