from django.test import TestCase

from lists.models import Item, List


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'lists/home.html')


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'the first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'second item'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        saved_items = Item.objects.all()
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(saved_list, list_)
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(first_saved_item.text, first_item.text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, second_item.text)
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):

    def test_display_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='item 1', list=list_)
        Item.objects.create(text='item 2', list=list_)

        response = self.client.get('/lists/the_only_list_in_the_world/')

        ## assertContains() handles bytes -> no need for decoding
        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/the_only_list_in_the_world/')

        self.assertTemplateUsed(response, 'lists/list.html')

class NewListTest(TestCase):

    def test_can_save_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'a new list item'})
        new_item = Item.objects.first()

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(new_item.text, 'a new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new',
                                    data={'item_text': 'a new list item'})

        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'],
        #                  '/lists/the_only_list_in_the_world/')
        self.assertRedirects(response, '/lists/the_only_list_in_the_world/')