from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item, List


class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_itens = List()
        list_itens.save()

        first_item = Item(text="item1", list=list_itens)
        first_item.save()
        second_item = Item(text="item2", list=list_itens)
        second_item.save()

        #check if saved object List
        self.assertEqual(list_itens,List.objects.first())

        #check if saved object Item
        saved_itens = Item.objects.all()
        self.assertEqual(len(saved_itens),2)

        copy_first_item = saved_itens[0]
        copy_second_item = saved_itens[1]

        #Check details of object saved
        self.assertEqual(copy_first_item.text, 'item1')
        self.assertEqual(copy_first_item.list, list_itens)

        self.assertEqual(copy_second_item.text, 'item2')
        self.assertEqual(copy_second_item.list, list_itens)