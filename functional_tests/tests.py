from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time


MAX_WAIT = 10
DRIVER_PATH = '/usr/lib/chromium-browser/chromedriver'


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        # user visits webpage
        # self.browser.get('http://localhost:8000/')
        self.setup_browser()

    def tearDown(self):
        self.browser.quit()

    def setup_browser(self):
        self.browser = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.browser.get(self.live_server_url)

    def assert_for_row_in_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')

                self.assertIn(row_text, [row.text for row in rows])

                return

            except (AssertionError, WebDriverException) as e:
                if (time.time() - start_time) > MAX_WAIT:
                    raise e

                time.sleep(0.5)


    def test_can_start_list_for_one_user(self):
        # user notices webpage title and header mention "to-do" lists
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # user is invited to enter a to-item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'enter a to-do item')

        # user typer "buy new shoes" into a text box
        todo_1 = 'buy new shoes'
        inputbox.send_keys(todo_1)

        # when user hits enter, the webpage updates and now the webpages lists:
        # "1: buy new shoes" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)

        self.assert_for_row_in_table(f'1: {todo_1}')

        # there is still a text box inviting the user to add another item
        # user enters "check shoes"
        inputbox = self.browser.find_element_by_id('id_new_item')
        todo_2 = 'check shoes'
        inputbox.send_keys(todo_2)
        inputbox.send_keys(Keys.ENTER)

        # self.assert_for_row_in_table(f'1: {todo_1}')
        self.assert_for_row_in_table(f'2: {todo_2}')

        # user is satisfied and leaves

        # ---------------------------------------------------------------------

        # the webpage updates again and now shows both items on her list

        # user wonders if the webpage will remember his/hers list
        # then user sees that the webpage as generated a uqique URL for her

        # user visits that URL; user's to-do list is still there

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # first user starts a new to-do list
        inputbox = self.browser.find_element_by_id('id_new_item')
        usr_1_todo_1 = 'buy new shoes'
        inputbox.send_keys(usr_1_todo_1)
        inputbox.send_keys(Keys.ENTER)

        self.assert_for_row_in_table(f'1: {usr_1_todo_1}')

        # user notices that his list has a unique URL
        first_users_list = self.browser.current_url
        self.assertRegex(first_users_list, '/lists/.+')

        # new user visits site
        ## we use a new browser session to ensure that information of first
        ## user are gone
        self.browser.quit()
        self.setup_browser()

        # there is no sign of first user's list
        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn(usr_1_todo_1, page_text)
        # self.assertNotIn(todo_2_usr_1, page_text)

        # second user starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        usr_2_todo_1 = 'buy keyboard'
        inputbox.send_keys(usr_2_todo_1)
        inputbox.send_keys(Keys.ENTER)

        self.assert_for_row_in_table(f'1: {usr_2_todo_1}')

        # second user gets his own unique URL
        second_users_list = self.browser.current_url

        self.assertRegex(second_users_list, '/lists/.+')
        self.assertNotEqual(second_users_list, first_users_list)

        # still, there is no trace of first user's list
        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn(usr_1_todo_1, page_text)
        self.assertIn(usr_2_todo_1, page_text)
