import requests as requests
import urllib
import json
import time

url = 'https://api.covid19api.com/summary'

def consultaMundo():
    request = urllib.request.urlopen(url)
    data_Atualizacao_global = json.load(request)['Date']
    ano = data_Atualizacao_global[0:4]
    mes = data_Atualizacao_global[5:7]
    dia = data_Atualizacao_global[8:10]
    data_Formatada = dia + "/" + mes + "/" + ano
    time.sleep(2)
    request = urllib.request.urlopen(url)
    data_global = json.load(request)["Global"]
    return f"Global\nTotal de Casos Confirmados: {data_global['TotalConfirmed']}\nNumero Total de Mortos: {data_global['TotalDeaths']},Numero Total de Recuperados: {data_global['TotalRecovered']}\nData Atualizacao: {data_Formatada}"


def consultaBrasil():
    time.sleep(2)
    request = urllib.request.urlopen(url)
    data_paises = json.load(request)["Countries"]
    data_brasil = json
    for country in data_paises:
        if country["CountryCode"] == "BR":
            data_brasil = country
            break

    data_Atualizacao_brasil = data_brasil['Date']
    ano = data_Atualizacao_brasil[0:4]
    mes = data_Atualizacao_brasil[5:7]
    dia = data_Atualizacao_brasil[8:10]
    data_Formatada = dia+"/"+mes+"/"+ano
    return f"BRASIL\nNumero Total de Infectados: {data_brasil['TotalConfirmed']},Numeros Total de Mortos: {data_brasil['TotalDeaths']},Numero Total de Recuperados: {data_brasil['TotalRecovered']}\nData Atualização: {data_Formatada}"

