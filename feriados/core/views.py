from asyncore import dispatcher_with_send
from django.shortcuts import render
from datetime import datetime
from .models import FeriadoModel
from .forms import FeriadoForm

def verifica_feriado(request):
    hoje = datetime.today()
    resultado = FeriadoModel.objects.filter(dia = hoje.day).filter(mes = hoje.month)
    if len(resultado) > 0:
        contexto = {'feriado': True,
                    'nome': resultado[0].nome}
    else:
        contexto = {'feriado': False}
    return render(request, 'feriado.html', contexto)


def cadastrar(request):
    if request.method == 'POST':
        
        form = FeriadoForm(request.POST)
        if form.is_valid():
            FeriadoModel.objects.create(**form.cleaned_data)   
            contexto = {}
            return render(request, 'feriado.html', contexto) 
        else:
            contexto = {'form': form}
            return render(request, 'cadastrar.html', contexto)
    else:
        form = FeriadoForm()
        contexto = {'form': form}
        return render(request, 'cadastrar.html', contexto)