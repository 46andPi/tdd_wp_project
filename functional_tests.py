from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver')

        # user visits webpage
        self.browser.get('http://localhost:8000/')

    def tearDown(self):
        self.browser.quit()

    def test_start_and_retrive_list(self):
        # user notices webpage title and header mention "to-do" lists
        self.assertIn('To-Do', self.browser.title, f'browser title was "{self.browser.title}"')

        self.fail('finish the test')

        # user is invited to enter a to-item straight away

        # user typer "buy new shoes" into a text box

        # when user hits enter, the webpage updates and now the webpages lists:
        # "1: buy new shoes" as an item in a to-do list

        # there is still a text box inviting the user to add another item
        # user enters "check shoes"

        # the webpage updates again and now shows both items on her list

        # user wonders if the webpage will remember his/hers list
        # then user sees that the webpage ahs generated a uqique URL for him/her

        # user visits that URL; user's to-do list is still there


if __name__ == '__main__':
    unittest.main()