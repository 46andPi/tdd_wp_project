from django.test import TestCase
from django.urls import resolve

from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')

        self.assertEqual(found.func, home_page)

    def test_uses_home_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_POST_request(self):
        self.client.post('/', data={'item_text': 'a new list item'})
        new_item = Item.objects.first()

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(new_item.text, 'a new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'a new list item'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the_only_list_in_the_world/')

    def test_only_save_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'the first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'second item'
        second_item.save()

        saved_items = Item.objects.all()

        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_items[0].text, first_item.text)
        self.assertEqual(saved_items[1].text, second_item.text)

class ListViewTest(TestCase):

    def test_display_all_items(self):
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get('/lists/the_only_list_in_the_world/')

        ## assertContains() handles bytes -> no need for decoding
        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/the_only_list_in_the_world/')

        self.assertTemplateUsed(response, 'lists/list.html')