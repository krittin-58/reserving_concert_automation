"""Handler for Thai Ticket Major website"""

from selenium.webdriver.common.by import By
from .base_handler import BaseTicketHandler
from time import sleep


class ThaiTicketMajorHandler(BaseTicketHandler):
    def __init__(self, driver, config, user_details):
        super().__init__(driver, config, user_details)
        self.seat_count = 0
        
    def login(self):
        """Login to Thai Ticket Major"""
        login_selectors = self.config["login_selectors"]
        
        # Click login button
        self.click_element_safe(By.XPATH, login_selectors["login_button"])
        sleep(1)
        
        # Enter credentials
        username = self.find_element_safe(By.ID, login_selectors["username_field"])
        if username:
            username.send_keys(self.user_details["email"])
            
        password = self.find_element_safe(By.ID, login_selectors["password_field"])
        if password:
            password.send_keys(self.user_details["pwd"])
            
        # Submit login
        self.click_element_safe(By.XPATH, login_selectors["submit_button"])
        sleep(2)
        
    def search_concert(self):
        """Search for concert"""
        current_url = self.driver.current_url
        concert_name = self.user_details["concert"]
        
        while self.driver.current_url == current_url:
            try:
                concert_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, concert_name)
                concert_link.click()
                self.driver.implicitly_wait(30)
            except:
                print(f"Concert '{concert_name}' not found")
                break
                
    def select_show(self):
        """Select show round"""
        show_num = int(self.user_details["show"])
        booking_selectors = self.config["booking_selectors"]
        
        # Get number of available shows
        shows = self.driver.find_elements(By.XPATH, "//div[@class='box-event-list']/div[2]/div")
        
        if show_num <= len(shows):
            show_selector = booking_selectors["show_selector"].format(show=show_num)
            self.click_element_safe(By.XPATH, show_selector)
            self.driver.implicitly_wait(30)
            
            # Check if show is selected
            selected = self.find_element_safe(By.XPATH, "//*[@id='rdId']/option[1]")
            if selected and "เลือกรอบการแสดง" in selected.text:
                self.click_element_safe(By.ID, "rdId")
                self.driver.implicitly_wait(30)
                self.click_element_safe(By.XPATH, f"//*[@div='select-date fix-me']/option[{show_num+1}]")
                self.driver.implicitly_wait(30)
                
    def select_zone(self, zone=None):
        """Select seating zone"""
        if zone is None:
            zone = self.user_details["zone"]
            
        booking_selectors = self.config["booking_selectors"]
        zone_areas = self.driver.find_elements(By.XPATH, booking_selectors["zone_map"])
        
        current_url = self.driver.current_url
        
        for i, area in enumerate(zone_areas, 1):
            href = area.get_attribute("href")
            if href and zone in href.split('#'):
                while self.driver.current_url == current_url:
                    area.click()
                    self.driver.implicitly_wait(30)
                break
                
    def select_seats(self):
        """Select available seats"""
        seats_needed = int(self.user_details["seats"])
        self.seat_count = 0
        
        # Find seat table
        rows = self.driver.find_elements(By.XPATH, "//*[@id='tableseats']/tbody[1]/tr")
        
        for i in range(1, len(rows) + 1):
            columns = self.driver.find_elements(By.XPATH, f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td")
            
            for j in range(2, len(columns) + 1):
                seat_element = self.driver.find_element(By.XPATH, f"//*[@id='tableseats']/tbody[1]/tr[{i}]/td[{j}]")
                seat_text = seat_element.text
                seat_title = seat_element.get_attribute("title")
                
                if seat_text == " ":
                    print(f"Seat {seat_title} not available")
                elif seat_text != " " and seat_text != "" and self.seat_count < seats_needed:
                    seat_element.click()
                    self.seat_count += 1
                    print(f"Selected seat: {seat_title}")
                    
                if self.seat_count == seats_needed:
                    break
                    
            if self.seat_count == seats_needed:
                break
                
        return self.seat_count > 0
        
    def confirm_booking(self):
        """Confirm the booking"""
        if self.seat_count > 0:
            booking_selectors = self.config["booking_selectors"]
            
            # Confirm seats
            self.driver.find_element(By.PARTIAL_LINK_TEXT, booking_selectors["confirm_button"]).click()
            self.driver.implicitly_wait(50)
            
            # Continue to payment
            self.driver.find_element(By.PARTIAL_LINK_TEXT, "Continue").click()
            self.driver.implicitly_wait(40)
            
            print("Booking confirmed successfully!")
            return True
        return False
        
    def find_alternative_zones(self):
        """Find alternative zones if preferred zone is not available"""
        # Go back to zone selection
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "ย้อนกลับ / Back").click()
        self.driver.implicitly_wait(40)
        
        # Check available zones
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "ที่นั่งว่าง / Seats Available").click()
        self.driver.implicitly_wait(30)
        
        # Get zone availability
        zone_rows = self.driver.find_elements(By.XPATH, "//*[@class='container-popup']/table[1]/tbody[1]/tr")
        
        for i in range(2, len(zone_rows) + 1):
            zone_name = self.driver.find_element(By.XPATH, f"//*[@class='container-popup']/table[1]/tbody[1]/tr[{i}]/td[1]").text
            availability = self.driver.find_element(By.XPATH, f"//*[@class='container-popup']/table[1]/tbody[1]/tr[{i}]/td[2]").text
            
            if availability != "0" and availability != "":
                print(f"Trying alternative zone: {zone_name}")
                self.select_zone(zone_name)
                if self.select_seats():
                    return True
                    
        return False