import os
from selenium import webdriver

BASE_URL = 'https://www.traveloka.com/en-id/'

class Scraper(webdriver.Chrome):
    def __init__(self, driver_path=None, teardown=False, implicitly_time_to_wait=10):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        driver_dir = os.path.join(base_path, 'driver')

        self.driver_path = driver_path if driver_path is not None else os.path.join(driver_dir, 'chromedriver.exe') 
        self.teardown = teardown
        self.implicitly_time_to_wait = implicitly_time_to_wait

        super().__init__(executable_path=self.driver_path)

        self.implicitly_wait(self.implicitly_time_to_wait)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def go_to_first_page(self):
        self.get(BASE_URL)

    def fill_in_hotel_destination_input(self, destination):
        input_element = self.find_element_by_css_selector(
            f'input[placeholder="City, hotel, place to go"]'
        )
        input_element.send_keys(destination)

    def click_nth_element_of_search_results(self, nth_index=0):
        try:
            search_result_elements = self.find_elements_by_css_selector(
                f'div[data-testid="dropdown-menu-item"]'
            )
            selected_element = search_result_elements[nth_index]
            selected_element.click()
        except IndexError:
            print('Index error')

if __name__ == '__main__':
    with Scraper() as scraper:
        scraper.go_to_first_page()
        scraper.fill_in_hotel_destination_input('Jakarta')
        scraper.click_nth_element_of_search_results(0)