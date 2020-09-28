from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver')

        ## user visits webpage
        self.browser.get('http://localhost:8000/')

    def tearDown(self):
        self.browser.quit()

    def assert_row_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])


    def test_start_and_retrive_list(self):
        ## user notices webpage title and header mention "to-do" lists
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        ## user is invited to enter a to-item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertEqual(inputbox.get_attribute('placeholder'), 'enter a to-do item')

        ## user typer "buy new shoes" into a text box
        todo_1 = 'buy new shoes'
        inputbox.send_keys(todo_1)

        ## when user hits enter, the webpage updates and now the webpages lists:
        ## "1: buy new shoes" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.assert_row_in_table(f'1: {todo_1}')

        ## there is still a text box inviting the user to add another item
        ## user enters "check shoes"
        inputbox = self.browser.find_element_by_id('id_new_item')
        todo_2 = 'check_shoes'
        inputbox.send_keys(todo_2)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.assert_row_in_table(f'1: {todo_1}')
        self.assert_row_in_table(f'2: {todo_2}')

        ## the webpage updates again and now shows both items on her list

        ## user wonders if the webpage will remember his/hers list
        ## then user sees that the webpage ahs generated a uqique URL for him/her

        ## user visits that URL; user's to-do list is still there


        self.fail('finish the test!')


if __name__ == '__main__':
    unittest.main()