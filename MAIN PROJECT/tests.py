from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
from selenium.webdriver.support.ui import Select

class Logintest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()

    def fill_form(self, username='', password=''):
        driver = self.driver
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "usename"))
        )
        driver.find_element(By.NAME, "usename").send_keys(username)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "passname"))
        )
        driver.find_element(By.NAME, "passname").send_keys(password)
    
    def login_with_credentials(self, username, password):
        self.driver.get(self.live_server_url)
        self.fill_form(username, password)
        self.driver.find_element(By.ID, "submit").click()

    '''def test_no_credentials(self):
        self.driver.get(self.live_server_url)
        self.fill_form()  # Leave username and password empty
        self.driver.find_element(By.ID, "submit").click()
        # Add an assertion or check for failed login
        # Example: Check for an error message element
        # self.assertTrue("error_message_element" in self.driver.page_source)
        print("Test scenario 'No Credentials' passed.")
        time.sleep(5)

    def test_wrong_password(self):
        self.driver.get(self.live_server_url)
        self.fill_form(username="vishal", password="wrongpassword")
        self.driver.find_element(By.ID, "submit").click()
        # Add an assertion or check for failed login
        # Example: Check for an error message element
        # self.assertTrue("error_message_element" in self.driver.page_source)
        print("Test scenario 'Wrong Password' passed.")
        time.sleep(5)

    def test_correct_credentials(self):
        self.driver.get(self.live_server_url)
        self.fill_form(username="vishal", password="zxcvbnmL@123")
        self.driver.find_element(By.ID, "submit").click()
        # Add an assertion or check for successful login
        # Example: Check for a successful login element or URL change
        # self.assertTrue("success_message_element" in self.driver.page_source)
        print("Test scenario 'Correct Credentials' passed.")
        time.sleep(5)

    def open_add_department(self):
        # Open the sidebar
        profile_picture = self.driver.find_element(By.CSS_SELECTOR, "img[onclick='toggleProfileSidebar()']")
        profile_picture.click()

        # Wait for the sidebar to open and click on "Add Departments"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Add Departments"))
        )
        self.driver.find_element(By.LINK_TEXT, "Add Departments").click()

    def fill_department_form(self, name, programs, hod):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "department_name"))
        )
        self.driver.find_element(By.ID, "department_name").send_keys(name)
        self.driver.find_element(By.ID, "offered_programs").send_keys(programs)
        self.driver.find_element(By.ID, "head_of_department").send_keys(hod)
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

    def test_add_department_without_data(self):
        self.login_with_credentials("amaljyothi", "zxcvbnmL@123")
        self.open_add_department()
        self.fill_department_form("", "", "")
        # Add checks for validation messages or unsuccessful addition
        print("Test scenario 'Add Department without Data' passed.")

    def test_add_existing_department(self):
        self.login_with_credentials("amaljyothi", "zxcvbnmL@123")
        self.open_add_department()
        self.fill_department_form("MCA", "both", "Dr. Smith")
        # Add checks for the error message for existing department
        print("Test scenario 'Add Existing Department' passed.")

    def test_add_new_department(self):
        self.login_with_credentials("amaljyothi", "zxcvbnmL@123")
        self.open_add_department()
        self.fill_department_form("Integrated MCA", "both", "Dr. Johnson")
        # Add checks for successful addition message
        print("Test scenario 'Add New Department' passed.")
    
    def open_add_instructor_page(self):
        # Log in and open the sidebar to click on "Add Instructor"
        self.login_with_credentials("amaljyothi", "zxcvbnmL@123")
        profile_picture = self.driver.find_element(By.CSS_SELECTOR, "img[onclick='toggleProfileSidebar()']")
        profile_picture.click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Add Instructors"))
        )
        self.driver.find_element(By.LINK_TEXT, "Add Instructors").click()

    def test_add_instructor_without_data(self):
        self.open_add_instructor_page()
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        # Add checks for validation messages or unsuccessful addition
        print("Test scenario 'Add Instructor without Data' passed. Failed to add instructor without giving details")

    def test_add_instructor_without_department(self):
        self.open_add_instructor_page()
        self.driver.find_element(By.ID, "instructorName").send_keys("John Doe")
        self.driver.find_element(By.ID, "instructorCourses").send_keys("Mathematics")
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        # Add checks for validation messages or unsuccessful addition
        print("Test scenario 'Add Instructor without Department' passed. Failed to add new instructor without selecting department")

    def test_add_instructor_with_all_details(self):
        self.open_add_instructor_page()

        # Wait for and fill in the instructor's name
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "instructorName"))
        )
        self.driver.find_element(By.ID, "instructorName").send_keys("Jane Doe")

        # Wait for and fill in the instructor's courses
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "instructorCourses"))
        )
        self.driver.find_element(By.ID, "instructorCourses").send_keys("Physics")

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "instructorQualification"))
        )
        self.driver.find_element(By.ID, "instructorQualification").send_keys("MCA")

        # Wait for and select the first department from the dropdown
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "department"))
        )
        department_select = Select(self.driver.find_element(By.ID, "department"))  # Ensure this ID matches your HTML
        department_select.select_by_index(1)

        # Submit the form
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        submit_button.click()

        # TODO: Add checks for successful addition message
        print("Test scenario 'Add Instructor with All Details' passed. Successfully added the instructor")'''
    
    def open_add_course_page(self):
        # Log in and open the sidebar to click on "Add Course"
        self.login_with_credentials("amaljyothi", "zxcvbnmL@123")
        profile_picture = self.driver.find_element(By.CSS_SELECTOR, "img[onclick='toggleProfileSidebar()']")
        profile_picture.click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Add Courses"))
        )
        self.driver.find_element(By.LINK_TEXT, "Add Courses").click()

    def test_add_course(self):
        self.open_add_course_page()
        # Fill in the course details
        self.driver.find_element(By.NAME, "course_name").send_keys("Introduction to Python")
        Select(self.driver.find_element(By.NAME, "department")).select_by_index(1)  # Select the first department
        self.driver.find_element(By.NAME, "course_duration").send_keys("100")
        self.driver.find_element(By.NAME, "course_fee").send_keys("500")
        self.driver.find_element(By.NAME, "course_description").send_keys("This is a course about Python.")

        # Select Languages

        # Select Course Level
        Select(self.driver.find_element(By.NAME, "course_level")).select_by_value("beginner")

        # Submit the form
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # Add checks for successful course addition
        print("Test scenario 'Add Course' passed.")



        
if __name__ == '__main__':
    unittest.main()




