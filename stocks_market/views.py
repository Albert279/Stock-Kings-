from django.shortcuts import render, redirect
from .models import Stock 
from .forms import StockForm
from django.contrib import messages

# Create your views here.
def home(request):
    import requests
    import json
    
    if request.method == "POST":
        ticker = request.POST["ticker"]
        #pk_0c1ca59c09ec4d1399348db5c9728f68
        
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker + "/quote?token=pk_c1a926c9fc58422a9abfcea92d16393d")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error 404 ...."
    
        return render(request, 'home.html', {"api": api})

    else:
        return render(request, 'home.html', {"ticker":  "Enter ticker symbol above!!!"})

def about(request):
    return render(request, 'about.html', {})


def add_stock(request):
    import requests
    import json

    if request.method == "POST":
        form = StockForm(request.POST or None)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Stock has been added!!! ")
            return redirect("add_stock")
        
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(ticker_item) + "/quote?token=pk_c1a926c9fc58422a9abfcea92d16393d")

            try:
                api = json.loads(api_request .content)
                output.append(api)
            except Exception as e:
                api = "Error 404 ...."
        return render(request, 'add_stock.html', {"ticker": ticker, "output": output})


def delete(request, Stock_id):
    item = Stock.objects.get(pk=Stock_id)
    item.delete()
    messages.success(request, "Stock has been deleted successfully")
    return redirect(add_stock)

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {"ticker" : ticker})