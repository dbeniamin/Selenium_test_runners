from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import unittest


class PracticeTestRun1(unittest.TestCase):
    def __init__(self, method_name: str = "runTest"):
        super().__init__(method_name)
        self.test_list = None

    def setUp(self):
        # ## Headless set-up
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        # pass the headless options in the -> webdriver.Chrome(options=options)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://the-internet.herokuapp.com')
        # self.driver.set_window_size(1250, 850)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        # if hasattr(self, 'driver') and self.driver:
        self.driver.quit()

    def run_all_tests(self):
        try:
            # loop the list of test
            for test_method in self.test_list:
                self.setUp()
                test_method()
                self.tearDown()
        finally:
            # check if the browsers closed
            # if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

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
        # ## Check boxes
        self.driver.find_element(By.LINK_TEXT, "Checkboxes").click()
        check_box_1 = self.driver.find_element(By.XPATH, '//*[@id="checkboxes"]/input[1]')
        check_box_1.click()
        box1_attribute = check_box_1.get_attribute("checked")
        self.assertIsNotNone(box1_attribute, "The first box did not changed its status !!")
        # the 2nd box is checked by default
        check_box_2 = self.driver.find_element(By.XPATH, '//*[@id="checkboxes"]/input[2]')
        check_box_2.click()
        box2_attribute = check_box_2.text
        self.assertEqual(box2_attribute, "", "The 2nd box did not change its status !!")


if __name__ == "__main__":
    test_runner = PracticeTestRun1()
    test_runner.test_list = [test_runner.test_1, test_runner.test_2, test_runner.test_3, test_runner.test_4]
    test_runner.run_all_tests()
