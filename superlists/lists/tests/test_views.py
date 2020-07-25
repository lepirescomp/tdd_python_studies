from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item, List

class TestHomePage(TestCase):

    def test_return_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home.html')   

class TestListView(TestCase):
    def test_displays_all_items(self):
        list_ = List.objects.create()
        first_item = Item.objects.create(text="item1", list = list_)
        second_item = Item.objects.create(text="item2", list = list_)

        response = self.client.get(f'/lists/{list_.id}/')

        self.assertContains(response, first_item.text)
        self.assertContains(response, second_item.text)
    
    def test_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response,'list.html')
    
class TestNewItem(TestCase):
    def test_post_save_success(self):
        response = self.client.post('/lists/new', data={'item_text': '1: buy food'})

        self.assertEqual(Item.objects.count(),1)
        item = Item.objects.first()
        self.assertEqual(item.text, '1: buy food')

    def test_post_redirect_correctly(self):
        response = self.client.post('/lists/new', data={'item_text': '1: buy food'})
        # self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/1/')
    
    def test_save_item_on_corret_list(self):
        wrong_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item',data={'item_text': 'item1'})

        self.assertEqual(Item.objects.count(),1)
        
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'item1')
        self.assertEqual(new_item.list, correct_list)

    def test_save_item_on_corret_list(self):
        wrong_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item',data={'item_text': 'item1'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
    
    def test_passes_correct_list_to_template(self):
        wrong_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)
