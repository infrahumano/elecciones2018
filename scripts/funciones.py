import os
import numpy as np
import json 
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument('--headless')

def lista_departamentos(base, first_page='DSE99999.htm'):
    portada = requests.get(base + first_page)
    portada.encoding = 'utf-8'
    portada = portada.text
    portada = BeautifulSoup(portada, 'html5lib')
    return [(li.find('a').contents[0], base + li.find('a')['href']) 
            for li in portada.find_all(class_='desplegable')[2].find_all('li')][1:]

def lista_municipios(departamento, base):
    nombre, url = departamento
    datos_departamento = requests.get(url)
    datos_departamento.encoding = 'utf-8'
    datos_departamento = datos_departamento.text
    datos_departamento = BeautifulSoup(datos_departamento, 'html5lib')
    return nombre, [(li.find('a').contents[0], base + li.find('a')['href']) 
                    for li in datos_departamento.find_all(class_='desplegable')[3].find_all('li')][1:]

def lista_municipios_consulta(departamento, base, base_consulta):
    nombre_dpto, municipios = lista_municipios(departamento, base)
    codigos_municipios = [(nombre, '{}{}.json'.format(base_consulta, url.split('/')[-1].split('.')[0][3:])) 
                          for nombre, url in municipios]
    return nombre_dpto, codigos_municipios

def extraer_cuentas_candidato(cand):
    cuentas = dict()
    
    cuentas['candidato_nombre'] = cand.find(class_='nombreCandidato').contents[0].strip().lower()
    cuentas['candidato_votos'] = int(cand.find(class_='abs').contents[0].replace('.', ''))
    cuentas['candidato_porcentaje'] = float(cand.find(class_='prc').contents[0].replace(',', '.')[2:-2])

    return cuentas

def extraer_cuentas_partido(partido, candidatos_partido):
    cuentas = dict()
    
    cuentas['partido'] = partido.find(class_='nomc').find_all('span')[1].contents[0].lower()
    cuentas['votos'] = int(partido.find(class_='abs').contents[0].replace('.', ''))
    cuentas['porcentaje'] = float(partido.find(class_='abs').contents[1].contents[0].replace(',', '.')[2:-2])
    cuentas['candidatos'] = [extraer_cuentas_candidato(cand) 
                             for cand in candidatos_partido.find_all('tr', class_='cndto')]

    return cuentas

def extraer_cuentas_municipio(municipio):
    circunscripciones = [item.find('a').contents[0].lower().replace(' ', '_') 
                         for item in municipio.find('ul', class_='solapasGroup').find_all('li')]
    suffixes = np.repeat([''] + ['_' + c for c in circunscripciones], 2, axis=0).tolist()
    
    cuentas = {(item.find_all(class_='infoTit')[0]
                .contents[0].lower()
                .replace(' ', '_')[:-1] + suffix): int(item.find_all(class_='infoInfo')[0].contents[0].replace('.', '')) 
               for item, suffix in zip(municipio.find_all(class_='votUp'), suffixes)}

    mesas_informadas = municipio.find_all(class_='piebola')[0].find_all('span')[1].contents[0].split(' ')
    cuentas['mesas_informadas'] = int(mesas_informadas[0].replace('.', ''))
    cuentas['total_mesas'] = int(mesas_informadas[2].replace('.', ''))
    
    votantes_habilitados = municipio.find_all(class_='piebola')[1].find_all('span')[1].contents[0].split(' ')
    cuentas['votantes'] = int(votantes_habilitados[0].replace('.', ''))
    cuentas['habilitados'] = int(votantes_habilitados[2].replace('.', ''))
    
    partidos = [zip(tabla.find_all(class_='datosTablaCandidatosH'), tabla.find_all(class_='datosTablaCandidatosB')) 
                for tabla in municipio.find_all(class_='tablaYFooter')]
                           
    for partido_circ, circunscripcion in zip(partidos, circunscripciones):
        cuentas[circunscripcion] = [extraer_cuentas_partido(partido, candidatos_partido) 
                                    for partido, candidatos_partido in partido_circ]

    return cuentas

def datos_municipio(municipio, nombre_departamento, prefix):
    nombre, url = municipio
    datos_municipio = requests.get(url)
    datos_municipio.encoding = 'utf-8'
    datos_municipio = datos_municipio.text
    datos_municipio = BeautifulSoup(datos_municipio, 'html5lib')
    cuentas = extraer_cuentas_municipio(datos_municipio)
    cuentas['municipio'] = nombre
    cuentas['departamento'] = nombre_departamento
    cuentas['url'] = url
    filename = '{}-{}-{}.json'.format(prefix, 
                                      nombre.replace(' ', '_').lower(), 
                                      nombre_departamento.replace(' ', '_').lower())
    with open('datos/' + filename, 'w') as f:
        json.dump(cuentas, f)
        
    print('Listo {}'.format(filename))

def extraer_cuentas_candidato(candidato):
    cuentas = dict()
    cuentas['candidato_nombre'] = candidato.find_element_by_class_name('nombCamdidato').text.title()
    cuentas['candidato_partido'] = candidato.find_element_by_class_name('nombPartido').text.title()
    votos = candidato.find_element_by_class_name('abs').text.replace('.', '').replace(',', '.').split(' ')
    cuentas['candidato_votos'] = int(votos[0])
    cuentas['candidato_porcentaje'] = float(votos[2][:-2])
    return cuentas

def extraer_cuentas_municipio_consulta(municipio):
    titulos = municipio.find_elements_by_class_name('infoTit')
    infos = municipio.find_elements_by_class_name('infoInfo')
    cuentas = dict([(t.text.lower().replace(' ', '_'), int(i.text.replace('.', ''))) 
                    for t, i in zip(titulos, infos)])
    bolas = [b.text.split('\n')[1].split(' ') for b 
             in municipio.find_elements_by_class_name('piebola')]
    cuentas['mesas_informadas'] = int(bolas[0][0].replace('.', '')) 
    cuentas['total_mesas'] = int(bolas[0][2].replace('.', ''))
    cuentas['votantes'] = int(bolas[1][0].replace('.', ''))
    cuentas['habilitados'] = int(bolas[1][2].replace('.', ''))
    cuentas['votos'] = [extraer_cuentas_candidato(candidato) for candidato 
                        in municipio.find_elements_by_class_name('fondofilacand')]
    return cuentas

def datos_municipio_consulta(municipio, nombre_departamento, prefix):
    nombre, url = municipio
    filename = '{}-{}-{}.json'.format(prefix, 
                                      nombre.replace(' ', '_').lower(), 
                                      nombre_departamento.replace(' ', '_').lower())   

    if os.path.isfile('datos/' + filename):
        print('Ya {} fue generada.'.format(filename))
        return 

    datos_municipio = webdriver.Firefox(firefox_options=options)
    datos_municipio.get(url)
    cuentas = extraer_cuentas_municipio_consulta(datos_municipio)
    datos_municipio.close()
    cuentas['municipio'] = nombre
    cuentas['departamento'] = nombre_departamento
    cuentas['url'] = url
    with open('datos/' + filename, 'w') as f:
        json.dump(cuentas, f)
        
    print('Listo {}'.format(filename))
    
def tabla_municipio_consulta(municipio):
    tabla = (pd.DataFrame(municipio['votos']).rename(columns={'candidato_partido':'partido'})
             .append([
                 {'candidato_nombre': 'votos no marcados', 
                  'partido': 'votos no marcados', 
                  'candidato_votos': municipio['votos_no_marcados:']},
                 {'candidato_nombre': 'votos nulos', 
                       'partido': 'votos nulos', 
                       'candidato_votos': municipio['votos_nulos:']}
             ]).assign(departamento=lambda x: municipio['departamento'], 
                       municipio=lambda x: municipio['municipio']))
    return tabla


# Funciones para leer los diccionarios que producen datos_municipio y datos_municipio_consulta
#
# Por ejemplo, para generar la tabla de datos de la cámara hago algo como: 
#
# import glob
# import pandas as pd
#
# municipios_camara = glob.glob('datos/cam*.json')  
# df = pd.concat([tabla(archivo, tabla_municipio, 'cámara_circ') for archivo in municipios_camara])
# 
# Y para generar la de la consulta de Petro contra Caicedo:
#
# municipios_consulta_inclusion = glob.glob('datos/cons*.json')
# df = pd.concat([tabla(archivo, tabla_municipio_consulta) for archivo in municipios_consulta_inclusion])

def tabla_partido(partido):
    candidatos = pd.DataFrame(partido['candidatos'])
    candidatos['partido'] = partido['partido']
    return candidatos

def tabla_circunscripcion(circunscripcion):
    tabla = pd.concat([tabla_partido(partido) for partido in circunscripcion[1]])
    tabla['circunscripcion'] = circunscripcion[0]
    return tabla

def tabla_municipio(municipio, prefijo):
    """
    Args:
        municipio (dict): el resultado de leer el json producido por datos_municipio.
        prefijo (str): para cámara es 'cámara_circ' y para senado es 'senado_circ'. Una chambonada.
    """
    circunscripciones = [key for key in municipio.keys() if key.startswith(prefijo)]
    tabla = (pd.concat([tabla_circunscripcion((key, municipio[key])) 
                       for key in circunscripciones])
             .append([{'candidato_nombre': 'votos nulos',
                       'partido': 'votos nulos',
                       'candidato_votos': municipio['votos_nulos'], 
                       'circunscripcion': 'sin circunscripción'},
                      {'candidato_nombre': 'votos no marcados',
                       'partido': 'votos no marcados',
                       'candidato_votos': municipio['votos_no_marcados'], 
                       'circunscripcion': 'sin circunscripción'}
                     ])
             .append([{'candidato_nombre': 'votos en blanco', 
                       'candidato_votos': municipio['votos_en_blanco_' + circunscripcion],
                       'partido': 'votos en blanco', 
                       'circunscripcion': circunscripcion} for circunscripcion in circunscripciones])
             .assign(departamento=lambda x: municipio['departamento'], 
                     municipio=lambda x: municipio['municipio']))
    return tabla

def tabla(archivo_municipio, funcion, *args):
    with open(archivo_municipio, 'r') as f:
        municipio = json.load(f)
    return funcion(municipio, *args)
