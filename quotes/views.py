import requests
import json

from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockFrom
from django.contrib import messages

PUBLIC_KEY = 'pk_908d3547248549428866b03ba25e03e5'


def getStockData(ticker):
    api_request = requests.get('https://cloud.iexapis.com/stable/stock/{}/quote?token={}'.format(str(ticker), PUBLIC_KEY))
    try:
        api = json.loads(api_request.content)
    except Exception as e:
        api = 'Error...'
    
    return api


def home(request):

    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = getStockData(ticker)

        return render(request,'home.html',{'returnStuff': api_request })
    else:
        return render(request,'home.html',{'ticker': 'enter a ticker symbol...'})


def about(request):
    return render(request,'about.html',{})


def add_stock(request):

    if request.method == 'POST':
        form = StockFrom(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ('Stock has been added'))
            return redirect('add_stock')
    
    else:
        ticker = Stock.objects.all()
        myDict = {}
        
        for i in ticker:
            myDict[str(i.pk)] = getStockData(i)

        return render(request,'add_stock.html',{'myDict' : myDict})

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, 'Profile stock deleted')
    return redirect('add_stock')


def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request,'delete_stock.html',{'ticker' : ticker})
