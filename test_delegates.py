from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import unittest


class PracticeTestFirst(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://the-internet.herokuapp.com')
        self.driver.set_window_size(1250, 850)
        self.driver.implicitly_wait(15)

    def tearDown(self):
        # if hasattr(self, 'driver') and self.driver:
        self.driver.quit()

    def test_runner(self):
        self.run_all_tests()

    def run_all_tests(self):
        try:
            # Loop over the list of test methods
            for test_method in [self.test_1, self.test_2, self.test_3, self.test_4]:
                self.setUp()  # Set up the browser (called once before the loop)
                test_method()  # Execute the test method
                self.tearDown()  # Tear down the browser (called once after the loop)
        finally:
            # if hasattr(self, 'driver') and self.driver:
            self.driver.quit()  # Make sure the browser is closed even if an exception occurs

    def test_1(self):
        # ## Add / Remove Elements ###
        self.driver.find_element(By.LINK_TEXT, "Add/Remove Elements").click()
        for _ in range(10):
            self.driver.find_element(By.XPATH, "//button[text()='Add Element']").click()
        for n in range(8):
            self.driver.find_element(By.CLASS_NAME, "added-manually").click()
        remaining_elements = len(self.driver.find_elements(By.CLASS_NAME, "added-manually"))
        self.assertEqual(remaining_elements, 2)

    def test_2(self):
        # ## Key Presses ###
        self.driver.find_element(By.LINK_TEXT, "Key Presses").click()
        ActionChains(self.driver).send_keys(Keys.SPACE).perform()
        action_status_message = self.driver.find_element(By.ID, 'result')
        self.assertEqual("You entered: SPACE", action_status_message.text)
        ActionChains(self.driver).send_keys("b").perform()
        self.assertEqual("You entered: B", action_status_message.text)

    def test_3(self):
        # ## Floating Menu ###
        floating_page = self.driver.find_element(By.LINK_TEXT, "Floating Menu")
        floating_page.click()
        body = self.driver.find_element(By.XPATH, '/html/body')
        body.send_keys(Keys.END)
        floating_element = self.driver.find_element(By.XPATH, '//*[@id="menu"]/ul/li[1]/a')
        try:
            assert floating_element.is_displayed()
        except NoSuchElementException:
            raise AssertionError(f"{floating_element} is not present on the page")

    def test_4(self):
        # ## Frames / iFrame ###
        self.driver.find_element(By.LINK_TEXT, "Frames").click()
        self.driver.find_element(By.LINK_TEXT, "iFrame").click()
        iframe = self.driver.find_element(By.TAG_NAME, "iframe")
        self.driver.switch_to.frame(iframe)
        edit_box = self.driver.find_element(By.XPATH, "//*[text()='Your content goes here.']")
        edit_box.send_keys(Keys.CONTROL, 'a')
        edit_box.send_keys(Keys.BACKSPACE)
        updated_edit_box = self.driver.find_element(By.XPATH, '//*[@id="tinymce"]')
        updated_edit_box.send_keys("This is an Automated Test !!")
        updated_edit_box.send_keys(Keys.CONTROL, 'a')
        updated_edit_box.send_keys(Keys.CONTROL, 'b')
        updated_edit_box.click()


if __name__ == "__main__":
    unittest.main()
