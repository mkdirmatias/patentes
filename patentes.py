#!/usr/bin/python
#-*- coding:UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import httplib
import urllib
import json
from termcolor import colored

# 
# Funcion para obtener multas
# 
def multas_total(patente):
    link       = "http://consultamultas.srcei.cl/ConsultaMultas/buscarConsultaMultasExterna.do"
    host       = "consultamultas.srcei.cl"
    parametros = 'ppu=%s' % patente
    headers    = {'Content-Type':'application/x-www-form-urlencoded','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0','Cookie':'JSESSIONID=32F21D2C90883C05DEA350CBA98E1CDD'}
    conexion   = httplib.HTTPConnection(host)
    conexion.request("POST", link, parametros, headers)
    request    = conexion.getresponse()
    respuesta  = request.read()
    conexion.close()
    html       = BeautifulSoup(respuesta,"html5lib")
    entradas   = html.find_all('div', {'class':'textEncabezadoTablaVentas'})
    final      = []

    for item in entradas:
        item.encode('utf-8')
        resultado  = item.getText()
        final.append(resultado)

    if len(final) > 0:
        return final[0]
    else:
        return "Sin multas"

#
# Funcion para estado de robo
#
def robo(patente):
    link       = "http://consultawebvehiculos.carabineros.cl/index.php"
    host       = "consultawebvehiculos.carabineros.cl"
    letras     = patente[0] + patente[1]
    numero     = patente[2] + patente[3]
    numer2     = patente[4] + patente[5]
    parametros = 'accion=buscar&txtLetras=%s&txtNumeros1=%s&txtNumeros2=%s&vin=' %(letras,numero,numer2)
    headers    = {'Content-Type':'application/x-www-form-urlencoded','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0','Cookie':'JSESSIONID=32F21D2C90883C05DEA350CBA98E1CDD'}
    conexion   = httplib.HTTPConnection(host)
    conexion.request("POST", link, parametros, headers)
    request    = conexion.getresponse()
    respuesta  = request.read()
    conexion.close()
    html       = BeautifulSoup(respuesta,"html5lib")
    entradas   = html.find_all('span', {'class':'Estilo1'})
    final      = []

    for item in entradas:
        item.encode('utf-8')
        resultado  = item.getText()
        final.append(resultado)

    if len(final) > 0:
        return final[0]
    else:
        return 2


# 
# Funcion que devuelve el tipo vehiculo
# 
def tipoVehiculo(numero):
    if numero == "1":
        tipo = 'AUTOMOVIL'
    elif numero == "2":
        tipo = 'STATION WAGON'
    elif numero == "3":
        tipo = 'TODO TERRENO'
    elif numero == "4":
        tipo = 'CAMIONETA'
    elif numero == "5":
        tipo = 'FURGON'
    elif numero == "7":
        tipo = 'CARRO DE ARRASTRE'
    elif numero == "12":
        tipo = 'MOTOCICLETA'
    else:
        tipo = 'Otro'

    return tipo


# 
# Funcion que devuelve si pertenece al transporte publico
# 
def transportePublico(patente):
    urlPublico      = "http://apps.mtt.cl/consultaweb/default.aspx"
    peticionPublico = requests.get(urlPublico)
    htmlPublico     = BeautifulSoup(peticionPublico.content ,"html5lib")
    state           = htmlPublico.find('input',{'name':'__VIEWSTATE'}).get('value')
    validation      = htmlPublico.find('input',{'name':'__EVENTVALIDATION'}).get('value')
    parametros_publicos = urllib.urlencode({'__VIEWSTATE':state,'__EVENTVALIDATION':validation,'ctl00$MainContent$btn_buscar':'Buscar','ctl00$MainContent$ppu':patente})

    headers   = {'Content-Type':'application/x-www-form-urlencoded','User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0','Cookie':'PHPSESSID=5905d3b7cb7bf267d6430a8685b4f776','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    conexion   = httplib.HTTPConnection('apps.mtt.cl')
    conexion.request("POST", "http://apps.mtt.cl/consultaweb/default.aspx", parametros_publicos, headers)
    request   = conexion.getresponse()
    respuesta = request.read()
    conexion.close()
    return respuesta


# 
# Datos de inicio 
# 
print colored('''
    ╔═══╗╔═══╗╔════╗╔═══╗╔═╗ ╔╗╔════╗╔═══╗╔═══╗
    ║╔═╗║║╔═╗║║╔╗╔╗║║╔══╝║║╚╗║║║╔╗╔╗║║╔══╝║╔═╗║
    ║╚═╝║║║ ║║╚╝║║╚╝║╚══╗║╔╗╚╝║╚╝║║╚╝║╚══╗║╚══╗
    ║╔══╝║╚═╝║  ║║  ║╔══╝║║╚╗║║  ║║  ║╔══╝╚══╗║
    ║║   ║╔═╗║  ║║  ║╚══╗║║ ║║║  ║║  ║╚══╗║╚═╝║
    ╚╝   ╚╝ ╚╝  ╚╝  ╚═══╝╚╝ ╚═╝  ╚╝  ╚═══╝╚═══╝
                by @UnknDown
''',"blue",attrs=['bold'])
print colored(" Obten los datos de un vehiculo mediante la patente \n","magenta",attrs=['bold'])


#
# Variables y peticiones
#
patente = raw_input( " Ingresa la patente: ")
print colored("\n Realizando busqueda\n","yellow",attrs=['bold'])

try:
    url = "https://soap.uanbai.com/bci/soap/2018/ajax/loadPPU.jsp?PPU=%s&SES=DDB9674E703F9BB04C4F3BB2D96D8291.worker1" % patente
    peticion = requests.get(url)
    datos    = json.loads(peticion.content)
except:
    print "No se pudo obtener la información"
    exit()


#
# Datos del vehiculo
#
print colored("+--------- Datos del Vehiculo -------+", "green", attrs=["bold"])
print colored(" Tipo: ","blue", attrs=["bold"]) + tipoVehiculo(datos['id_tipo'])
print colored(" Marca: ","blue", attrs=["bold"]) + datos['marca']
print colored(" Modelo: ","blue", attrs=["bold"]) + datos['modelo']
print colored(" Año: ","blue", attrs=["bold"]) + str(datos['ano'])
print colored(" N° Motor: ","blue", attrs=["bold"]) + str(datos['vin'])
print colored(" DV patente: ","blue", attrs=["bold"]) + str(datos['dvpatente'])


# 
# Datos del dueño
# 
print colored("+--------- Datos del Dueño -------+", "green", attrs=["bold"])
print colored(" Nombre: ","blue", attrs=["bold"]) + datos['propietario']['nombre'] + " " + datos['propietario']['ap_paterno'] + " " + datos['propietario']['ap_materno']
print colored(" RUT: ","blue", attrs=["bold"]) + datos['propietario']['rut'] +"-" + datos['propietario']['dv']


# 
# Datos legales del vehiculo
# 
print colored("+--------- Datos Legales -------+", "green", attrs=["bold"])
print colored(" Total multas: ","blue", attrs=["bold"]) + str(multas_total(patente))
print colored(" Encargo por robo: ","blue", attrs=["bold"]) + str(robo(patente))

# 
# Verificamos si pertence al transporte publico
#
publico = transportePublico(patente)
print colored("+--------- Datos transporte publico -------+", "green", attrs=["bold"])

label    = []
content  = []
html     = BeautifulSoup(publico,"html5lib")
entradas = html.find_all('td', {'class':'label'})
cont     = html.find_all('span')

for item in entradas:
    item.encode('utf-8')
    resultado  = item.getText()
    label.append(resultado)

for contenido in cont:
    contenido.encode('utf-8')
    resultados  = contenido.getText()
    content.append(resultados)

content.pop(0)
total_label   = len(label)
total_content = len(content)

# verificamos si encuentra datos en transporte publico
if total_label > 0:
    for x in xrange(0,total_label):
        print colored(" "+label[x]+": ","blue", attrs=["bold"]) + content[x]

    if content[total_content-2] != "":
        print colored(" Conductores: ","blue", attrs=["bold"]) + content[total_content-2]
    else:
        print colored(" Conductores: -","blue", attrs=["bold"])
else:
    print " El vehiculo no pertenece al transporte publico"
