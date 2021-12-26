from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

# Create your views here.
def home(request):
    import requests
    import json
    #esta logica aplica para el input del form
    if request.method == 'POST':
        ticker = request.POST['ticker']
        #pk_5b864e29575c4b7eb202900194a88dce
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_5b864e29575c4b7eb202900194a88dce")
        
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {'clave_api': api})
    else:
        return render(request, 'home.html', {'ticker':"Ingrese una Acción en el buscador"})


def about(request):
    return render(request, 'about.html', {})

def add_stock(request):
    import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock ha sido agregado"))
            return redirect('add_stock')        
    else:  
        ticker = Stock.objects.all()
        output = [] #lista, aqui se almacenara toda la data de la consulta, luego en el diccionario se crea la clave:valor, 'output':output y declaramos el output en add_stock.html e inyectamos la data en la tabla.
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_5b864e29575c4b7eb202900194a88dce")
        
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."

        return render(request, 'add_stock.html', {'stock':ticker, 'output':output})#para pasar la lista output al template, creamos la clave cuyo valor almacena los valores de ticker symbol, y despues declaramos interpolado la clave en el template



def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("El Activo ha sido borrado"))
    return redirect(delete_stock)

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})
    