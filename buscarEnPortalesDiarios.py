# -*- coding: utf-8 -*-
#    This file is part of buscarEnPortalesDiarios.
#
#    buscarEnPortalesDiarios is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    buscarEnPortalesDiarios is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with buscarEnPortalesDiarios; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import urllib.request
import bs4
import pandas as pd
import os
import urllib.parse
from datetime import datetime
import locale
import csv


linkAOmitir = ['https://www.facebook.com/lanacion/photos',
               'https://www.facebook.com/lanacion/videos',
               'https://www.facebook.com/lndeportes/photos',
               'https://www.facebook.com/clarincom/videos',
               'https://www.facebook.com/clarincom/photos',
               'http://www.youtube.com',
               'http://youtu.be/',
               'blogs.lanacion',
               '\\N'
               ]

linkMovidos = {'http://canchallena.lanacion': 'http://www.lanacion',
               'http://personajes.lanacion': 'http://www.lanacion',
               'https://www.ieco.clarin.com/ieco/economia': 'https://www.clarin.com/economia',
               }


def getHtml(req):
    try:
        resp = urllib.request.urlopen(req)
        html = resp.read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        return soup
    except Exception as ex:
        print("ERROR" + str(ex))
        return None


def getFechaNacion(soup):
    fechaNacion = "FECHA NO ENCONTRADA"
    if (soup is None):
        return fechaNacion

    try:
        for tag in soup.find_all("meta"):
            if tag.get("itemprop", None) == "datePublished":
                    return tag.get("content", None)
        contenedor = soup.find(class_='fecha')
        if(contenedor is not None):
            fechaCompleta = contenedor.getText()
            fechaCompleta = fechaCompleta.replace('\xa0', '')
            fechaCompleta = fechaCompleta.replace('de', '')
            fechaCompleta = fechaCompleta.replace('•', '')
            fechaCompleta = fechaCompleta.replace('  ', ' ')
            fechaCompleta = fechaCompleta.replace('  ', ' ')
            fechaCompleta = fechaCompleta.strip()
            locale.setlocale(locale.LC_TIME, 'es_AR')
            if('•' in contenedor.getText()):
                fechaCompleta = datetime.strptime(
                    fechaCompleta, '%d %B %Y %H:%M')
            else:
                fechaCompleta = datetime.strptime(
                    fechaCompleta, '%d %B %Y')
            fechaNacion = fechaCompleta.strftime('%d/%m/%Y %H:%M:%S')
    except Exception as ex:
        print("ERROR" + str(ex))
    return fechaNacion


def getTemaNacion(soup):
    try:
        if (soup is not None):
            contenedor = soup.find(class_='path floatFix breadcrumb')
            if(contenedor is None):
                contenedor = soup.find(class_='path patrocinado floatFix breadcrumb')
            if(contenedor is None):
                contenedor = soup.find(class_='temas')
                if (contenedor is not None):
                    elementosContenedor = contenedor.find_all("a")
                    if(elementosContenedor is not None):
                        return elementosContenedor[0].getText()
            if (contenedor is not None):
                elementosContenedor = contenedor.find_all("span")
                if(elementosContenedor is not None):
                    tag = elementosContenedor[1]
                    if tag.get("itemprop", None) == "name":
                        return tag.getText()
    except Exception as ex:
        print("ERROR" + str(ex))
       
    return "TEMA NO ENCONTRADO"


def getVolantaNacion(soup):
    try:
        if (soup is not None):
            contenedor = soup.find(class_='path floatFix breadcrumb')
            if(contenedor is None):
                contenedor = soup.find(class_='path patrocinado floatFix breadcrumb')
            if(contenedor is None):
                contenedor = soup.find(class_='path tema-espacio-hsbc floatFix breadcrumb')
            if(contenedor is None):
                contenedor = soup.find(class_='temas')
                if (contenedor is not None):
                    elementosContenedor = contenedor.find_all("a")
                    if(elementosContenedor is not None and len(elementosContenedor) > 1):
                        return elementosContenedor[1].getText()
            if(contenedor is not None):
                elementosContenedor = contenedor.find_all("span")
                if(elementosContenedor is not None and len(elementosContenedor) > 2):
                    tag = elementosContenedor[2]
                    if tag.get("itemprop", None) == "name":
                        return tag.getText()
    except Exception as ex:
        print("ERROR" + str(ex))

    return "VOLANTA NO ENCONTRADA"


def getTituloDiario(soup):
    result = "TITULO No Encontrado"
    if (soup is None):
        return result

    try:
        if (soup.h1 is not None):
            result = soup.h1.getText()
    except Exception as ex:
        print("ERROR" + str(ex))
    return result


def getBajadaNacion(soup):
    texto = "BAJADA NO ENCONTRADA"
    if (soup is None):
        return texto
    try:
        bajada = soup.find(class_="bajada")
        # porque class es una palabra reservada
        if(bajada is not None):
            texto = bajada.getText()
    except Exception as ex:
        print("ERROR" + str(ex))
        print(texto)
    return texto


def getTextoDiarioLaNacion(soup):
    texto = "TEXTO DIARIO NO ENCONTRADO"
    if (soup is not None):
        return texto

    try:
        cuerpo = soup.find(id='cuerpo')
        if(cuerpo is not None):
            parrafos = cuerpo.find_all('p')
            texto = ""
            for p in parrafos:
                texto = texto + p.getText()
    except Exception as ex:
        print("ERROR" + str(ex))
        print(texto)
    return texto


def getTextoDiarioClarin(soup):
    texto = "TEXTO DIARIO NO ENCONTRADO"
    if (soup is not None):
        return texto

    try:
        cuerpo = soup.find(class_='body-nota')
        # porque class es una palabra reservada
        if(cuerpo is not None):
            parrafos = cuerpo.find_all('p')
            texto = ""
            for p in parrafos:
                texto = texto + p.getText()
    except Exception as ex:
        print("ERROR" + str(ex))
        print(texto)
    return texto


def getFechaClarin(soup):

    for tag in soup.find_all("meta"):
        if tag.get("itemprop", None) == "datePublished":
            return tag.get("content", None)
    return "FECHA NO ENCONTRADA"


def getTemaClarin(soup):
    texto = "TEMA  NO ENCONTRADO"
    if (soup is None):
        return texto

    try:
        # Clarín
        tema = soup.find(class_='header-section-name')
        texto = ""
        if(tema is not None):
            texto = tema.getText()
    except Exception as ex:
        print("ERROR" + str(ex))
        print(texto)
    return texto


def getVolantaClarin(soup):
    texto = "VOLANTA NO ENCONTRADA"
    if (soup is None):
        return texto

    try:
        volanta = soup.find(class_='volanta')
        texto = ""
        if (volanta is not None):
            texto = volanta.getText()
    except Exception as ex:
        print("ERROR" + str(ex))
        print(texto)
    return texto


def getBajadaDiarioClarin(soup):
    texto = "BAJADA NO ENCONTRADA"
    if (soup is None):
        return texto

    try:
        bajada = soup.find(class_='bajada')
        if(bajada is not None):
            parrafos = bajada.find_all('p')
            texto = ""
            for p in parrafos:
                texto = texto + p.getText()
    except Exception as ex:
        print("ERROR" + str(ex))
        print(texto)
    return texto


def alargar_url(req):
    try:
        resolvedURL = urllib.request.urlopen(req)
        return resolvedURL.url
    except Exception as ex:
        print("ERROR" + str(ex))
    return None


def esLinkAOmitir(link_url):
    '''Determina si el link puede ser procesado o no'''
    for link in linkAOmitir:
        if link in link_url:
            return True
    return False


def getLinkDomain(link_url):
    '''Devuelve el dominio del link'''
    parsed_uri = urllib.parse.urlparse(link_url)
    return '{uri.netloc}'.format(uri=parsed_uri)


def addColumnaTitulo(nombreArchivoEntrada):
    posts = loadCsvIntoDataSet(nombreArchivoEntrada).tolist()
    for i in range(0, len(posts) - 1):
    #for i in range(1058, 1065):
        try:
            print(i)
            link_url = posts[i][3]
            if (not(pd.isnull(link_url))):
                if(esLinkAOmitir(link_url)):
                    continue

                for viejo in linkMovidos:
                    if(viejo in link_url):
                        link_url = link_url.replace(viejo, linkMovidos[viejo])

                req = urllib.request.Request(link_url)
                urlOriginal = alargar_url(req)
                if(not(pd.isnull(urlOriginal)) and not(urlOriginal is None)):
                    posts[i][4] = getLinkDomain(urlOriginal)
                    posts[i].append(urlOriginal)

                    if ('lanacion.com' in urlOriginal):
                        soup = getHtml(req)
                        posts[i].append(getFechaNacion(soup))
                        posts[i].append(getTemaNacion(soup))
                        posts[i].append(getVolantaNacion(soup))
                        posts[i].append(getTituloDiario(soup))
                        posts[i].append(getBajadaNacion(soup))
                        posts[i].append(getTextoDiarioLaNacion(soup))
                    elif('clarin.com' in urlOriginal):
                        soup = getHtml(req)
                        posts[i].append(getFechaClarin(soup))
                        posts[i].append(getTemaClarin(soup))
                        posts[i].append(getVolantaClarin(soup))
                        posts[i].append(getTituloDiario(soup))
                        posts[i].append(getBajadaDiarioClarin(soup))
                        posts[i].append(getTextoDiarioClarin(soup))
                    else:
                        posts[i].append("OTRO MEDIO")
                        posts[i].append("OTRO MEDIO")
                        posts[i].append("OTRO MEDIO")
                        posts[i].append("OTRO MEDIO")
                        posts[i].append("OTRO MEDIO")
                        posts[i].append("OTRO MEDIO")
                else:
                    posts[i].append("URL NULL")
                    posts[i].append("URL NULL")
                    posts[i].append("URL NULL")
                    posts[i].append("URL NULL")
                    posts[i].append("URL NULL")
                    posts[i].append("URL NULL")
                    posts[i].append("URL NULL")
            else:
                posts[i].append("LINK NULL")
                posts[i].append("LINK NULL")
                posts[i].append("LINK NULL")
                posts[i].append("LINK NULL")
                posts[i].append("LINK NULL")
                posts[i].append("LINK NULL")
                posts[i].append("LINK NULL")
        except Exception as ex:
            columnas = len(posts[i]) + 1
            for _ in range(columnas, 14):
                posts[i].append("TIME OUT")
            print("TIME OUT")
            print(ex)

    return posts


def loadCsvIntoDataSet(nombreArchivoEntrada):
    csv = pd.read_csv(nombreArchivoEntrada, header=0, sep=',', quotechar='\"', encoding="utf-8")
    return csv.values


def saveInCsv(postsFinal, nombreArchivoSalida):
    columns = ['tipo_post', 'post_id', 'post_link', 'link', 'link_domain', 'post_message', 'UrlCompleta', 'fecha_hora_diario', 'tema', 'volanta', 'titulo_diario', 'bajada', 'texto_diario']
    print(postsFinal)

#    for i in range(0, 30):
#        if(len(postsFinal[i]) > 12):
#            k=0

    df = pd.DataFrame(data=postsFinal, columns=columns)
    df.to_csv(nombreArchivoSalida, index=False, columns=columns, sep=';', quoting=csv.QUOTE_ALL, doublequote=True, quotechar='"', encoding="utf-8")


nombreArchivoEntrada = os.path.join(os.path.dirname(__file__), 'data', 'buscar_info_en_portales_1129.csv')
nombreArchivoSalida = os.path.join(os.path.dirname(__file__), 'data', 'post_output.csv')
postsConTitulo = addColumnaTitulo(nombreArchivoEntrada)
saveInCsv(postsConTitulo, nombreArchivoSalida)
