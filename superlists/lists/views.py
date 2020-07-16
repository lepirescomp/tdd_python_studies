from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

def home_page(request):
    return render(request,'home.html')

def view_list(request,list_id):
    list_ = List.objects.get(id=list_id)
    item = Item.objects.filter(list=list_)
    return render(request,'list.html',{'list': list_})

def new_list(request):
    list_of_items = List.objects.create()
    Item.objects.create(text=request.POST.get("item_text",""), list=list_of_items)
    return redirect(f'/lists/{list_of_items.id}/')

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST.get("item_text",""), list=list_)
    return redirect(f"/lists/{list_.id}/")