import csv

from django.shortcuts import render
from django.views.generic import ListView


def get_csv_products():
    csv_list = []
    with open('/home/apple/code/project1/tune/cost_models/store.csv', 'r', encoding='utf-8') as f:
        data = csv.DictReader(f, delimiter=';')
        for row in data:
            if row['Editions']:
                # if row['Price'] != '0':
                csv_list.append({'Title': row['Title'], 'Price': row['Price'],})

    return csv_list


class CheckView(ListView):
    template_name = 'te.html'
    context_object_name = 'product'
    context = {'product_list', str(get_csv_products())}


def index(request):
    data = {'product_list': get_csv_products()}
    return render(request, "te.html", context=data)


def not_update(request):
    csv_list = []
    with open('/home/apple/code/project1/tune/cost_models/store.csv', 'r', encoding='utf-8') as f:
        data = csv.DictReader(f, delimiter=';')
        for row in data:
            if row['Editions']:
                if row['Price'] == '0':
                    csv_list.append({'Title': row['Title'], 'Price': row['Price'],})
    data = {'product_list': csv_list}
    return render(request, "te.html", context=data)


def ready(request):
    csv_list = []
    with open('/home/apple/code/project1/tune/cost_models/store.csv', 'r', encoding='utf-8') as f:
        data = csv.DictReader(f, delimiter=';')
        for row in data:
            if row['Editions']:
                if row['Price'] != '0':
                    csv_list.append({'Title': row['Title'], 'Price': row['Price'],})
    data = {'product_list': csv_list}
    return render(request, "te.html", context=data)


