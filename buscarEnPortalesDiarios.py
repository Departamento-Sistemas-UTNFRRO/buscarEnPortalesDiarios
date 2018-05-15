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

def getHtml(req):
    try:
        resp = urllib.request.urlopen(req)
    except Exception as ex:
        print("ERROR" + str(ex))
        return None
    else:
        html = resp.read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        return soup


def getFechaNacion(soup):
    if (soup is not None):
        for tag in soup.find_all("meta"):
            if tag.get("itemprop", None) == "datePublished":
                return tag.get("content", None)
        contenedor = soup.find(class_='fecha')
        if(contenedor is not None):
            fechaCompleta = contenedor.getText()
            fechaCompleta = fechaCompleta.replace('\xa0•', '')
            fechaCompleta = fechaCompleta.replace('de', '')
            fechaCompleta = fechaCompleta.replace('  ', ' ')
            fechaCompleta = fechaCompleta.replace('  ', ' ')
            locale.setlocale(locale.LC_TIME, 'es_AR')
            fechaCompleta = datetime.strptime(fechaCompleta, '%d %B %Y %H:%M')
            return fechaCompleta.strftime('%d/%m/%Y %H:%M:%S')
    return "FECHA NO ENCONTRADA"


def getTemaNacion(soup):
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
        
    return "TEMA NO ENCONTRADO"


def getVolantaNacion(soup):
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
                if(elementosContenedor is not None):
                    return elementosContenedor[1].getText()
        if(contenedor is not None):
            elementosContenedor = contenedor.find_all("span")
            if(elementosContenedor is not None and len(elementosContenedor) > 2):
                tag = elementosContenedor[2]
                if tag.get("itemprop", None) == "name":
                    return tag.getText()
    return "VOLANTA NO ENCONTRADA"


def getTituloDiario(soup):
    if (soup is not None):
        if (soup.h1 is not None):
            return(soup.h1.getText())
        else:
            return "TITULO No Encontrado"
    else:
        return "SOUP No Encontrado 2"


def getBajadaNacion(soup):
    if (soup is not None):
        texto = "BAJADA NO ENCONTRADA"
        if (soup is not None):
            try:
                # Clarín
                bajada = soup.find(class_="bajada")
                # porque class es una palabra reservada
                if(bajada is not None):
                    texto = ""
                    texto = bajada.getText()
            except Exception as ex:
                print("ERROR" + str(ex))
                print(texto)
    return texto


def getTextoDiarioLaNacion(soup):
    texto = "TEXTO DIARIO NO ENCONTRADO"
    if (soup is not None):
        # La Nación
        try:
            cuerpo = soup.find(id='cuerpo')
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
        try:
            # Clarín
            cuerpo = soup.find(class_='body-nota')
            # porque class es una palabra reservada
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
    if (soup is not None):
        try:
            # Clarín
            tema = soup.find(class_='header-section-name')
            texto = ""
            texto = tema.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
    return texto


def getVolantaClarin(soup):
    texto = "VOLANTA NO ENCONTRADA"
    if (soup is not None):
        try:
            # Clarín
            volanta = soup.find(class_='volanta')
            texto = ""
            texto = volanta.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
    return texto


def getBajadaDiarioClarin(soup):
    texto = "BAJADA NO ENCONTRADA"
    if (soup is not None):
        try:
            # Clarín
            bajada = soup.find(class_='bajada')
            parrafos = bajada.find_all('p')
            texto = ""
            for p in parrafos:
                texto = texto + p.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
    return texto


def loadCsvIntoDataSet(nombreArchivoEntrada):
    csv = pd.read_csv(nombreArchivoEntrada, header=0, sep=',', quotechar='\"', encoding="utf-8")
    return csv.values


def alargar_url(req):
    try:
        resolvedURL = urllib.request.urlopen(req)
        return resolvedURL.url
    except Exception as ex:
        print("ERROR" + str(ex))
    
    return None

def addColumnaTitulo(nombreArchivoEntrada):
    posts = loadCsvIntoDataSet(nombreArchivoEntrada).tolist()
#    for i in range(0, len(posts) - 1):
    for i in range(22, 27):
        try:
            print(i)
            if (not(pd.isnull(posts[i][3]))):
                req = urllib.request.Request(posts[i][3])
                urlOriginal = alargar_url(req)
                if(not(pd.isnull(urlOriginal)) and not(urlOriginal is None)):
                    parsed_uri = urllib.parse.urlparse(urlOriginal)
                    domain = '{uri.netloc}'.format(uri=parsed_uri)
                    posts[i][4] = domain
                    posts[i].append(urlOriginal)
                    if (('lanacion.com' in urlOriginal) and not('blogs.lanacion' in urlOriginal)):
                        soup = getHtml(req)
                        posts[i].append(getFechaNacion(soup))
                        # tema o seccion Ej: política, deportes
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
            for _ in range(columnas, 13):
                posts[i].append("TIME OUT")
            print("TIME OUT")
            print(ex)

    return posts


def saveInCsv(postsFinal, nombreArchivoSalida):
    columns = ['tipo_post', 'post_id', 'post_link', 'link', 'link_domain', 'post_message', 'UrlCompleta', 'fecha_hora_diario', 'tema', 'volanta', 'titulo_diario', 'bajada', 'texto_diario']
    print(postsFinal)
    df = pd.DataFrame(data=postsFinal, columns=columns)
    df.to_csv(nombreArchivoSalida, index=False, columns=columns, sep=';', quotechar='"')


nombreArchivoEntrada = os.path.join(os.path.dirname(__file__), 'data', 'buscar_links_faltantes.csv')
nombreArchivoSalida = os.path.join(os.path.dirname(__file__), 'data', 'post_output.csv')
postsConTitulo = addColumnaTitulo(nombreArchivoEntrada)
saveInCsv(postsConTitulo, nombreArchivoSalida)
