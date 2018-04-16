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


def getHtml(url):
    req = urllib.request.Request(url)
    try:
        resp = urllib.request.urlopen(req)
    except Exception as ex:
        print("ERROR" + str(ex))
        return None
    else:
        html = resp.read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        return soup


def getFechaNacion(url):
    soup = getHtml(url)
    for tag in soup.find_all("meta"):
        if tag.get("itemprop", None) == "datePublished":
            return tag.get("content", None)
    return "FECHA NO ENCONTRADA"


def getTemaNacion(url):
    soup = getHtml(url)
    contenedor = soup.find(class_='path floatFix breadcrumb')
    if(contenedor is None):
        contenedor = soup.find(class_='path patrocinado floatFix breadcrumb')
    elementosContenedor = contenedor.find_all("span")
    tag = elementosContenedor[1]
    if tag.get("itemprop", None) == "name":
        return tag.getText()
    return "TEMA NO ENCONTRADO"


def getVolantaNacion(url):
    soup = getHtml(url)
    contenedor = soup.find(class_='path floatFix breadcrumb')
    if(contenedor is None):
        contenedor = soup.find(class_='path patrocinado floatFix breadcrumb')
    if(contenedor is None):
        contenedor = soup.find(class_='path tema-espacio-hsbc floatFix breadcrumb')
    elementosContenedor = contenedor.find_all("span")
    if(len(elementosContenedor) > 2):
        tag = elementosContenedor[2]
        if tag.get("itemprop", None) == "name":
            return tag.getText()
    return "VOLANTA NO ENCONTRADA"


def getTituloDiario(url, soup):
    if (soup is not None):
        if (soup.h1 is not None):
            return(soup.h1.getText())
        else:
            return "TITULO No Encontrado"
    else:
        return "SOUP No Encontrado 2"


def getBajadaNacion(url):
    soup = getHtml(url)
    texto = "BAJADA NO ENCONTRADA"
    if (soup is not None):
        try:
            # Clarín
            bajada = soup.find(class_="bajada")
            # porque class es una palabra reservada
            texto = ""
            texto = bajada.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
    return texto


def getTextoDiarioLaNacion(url):
    soup = getHtml(url)
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


def getTextoDiarioClarin(url, soup):
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


def getFechaClarin(url, soup):
    for tag in soup.find_all("meta"):
        if tag.get("itemprop", None) == "datePublished":
            return tag.get("content", None)
    return "FECHA NO ENCONTRADA"


def getTemaClarin(url, soup):
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


def getVolantaClarin(url, soup):
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


def getBajadaDiarioClarin(url, soup):
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
    csv = pd.read_csv(nombreArchivoEntrada, header=0, sep=';', quotechar='\'', encoding="utf-8")
    return csv.values


def alargar_url(url):
    req = urllib.request.Request(url)
    try:
        urllib.request.urlopen(req)
    except Exception:
        return None
    else:
        resolvedURL = urllib.request.urlopen(url)
        return resolvedURL.url


def addColumnaTitulo(nombreArchivoEntrada):
    posts = loadCsvIntoDataSet(nombreArchivoEntrada).tolist()
    for i in range(0, len(posts) - 1):
        try:
            print(i)
            if (not(pd.isnull(posts[i][3]))):
                urlOriginal = alargar_url(posts[i][3])
                parsed_uri = urllib.parse.urlparse(urlOriginal)
                domain = '{uri.netloc}'.format(uri=parsed_uri)
                posts[i][4] = domain
                if(not(pd.isnull(urlOriginal)) and not(urlOriginal is None)):
                    if (('lanacion.com' in urlOriginal) and not('blogs.lanacion' in urlOriginal)):
                        posts[i].append(urlOriginal)
                        soup = getHtml(urlOriginal)
                        posts[i].append(getFechaNacion(urlOriginal))
                        # tema o seccion Ej: política, deportes
                        posts[i].append(getTemaNacion(urlOriginal))
                        posts[i].append(getVolantaNacion(urlOriginal))
                        posts[i].append(getTituloDiario(urlOriginal, soup))
                        posts[i].append(getBajadaNacion(urlOriginal))
                        posts[i].append(getTextoDiarioLaNacion(urlOriginal))
                    elif('clarin.com' in urlOriginal):
                        posts[i].append(urlOriginal)
                        soup = getHtml(urlOriginal)

                        posts[i].append(getFechaClarin(urlOriginal, soup))
                        posts[i].append(getTemaClarin(urlOriginal, soup))
                        posts[i].append(getVolantaClarin(urlOriginal, soup))
                        posts[i].append(getTituloDiario(urlOriginal, soup))
                        posts[i].append(getBajadaDiarioClarin(urlOriginal, soup))
                        posts[i].append(getTextoDiarioClarin(urlOriginal, soup))
                    else:
                        posts[i].append("OTRO MEDIO")
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
            for j in range(columnas, 13):
                posts[i].append("TIME OUT")
            print("TIME OUT")
            print(ex)

    return posts


def saveInCsv(postsFinal, nombreArchivoSalida):
    columns = ['tipo_post', 'post_id', 'post_link', 'link', 'link_domain', 'UrlCompleta', 'fecha_hora_diario', 'tema', 'volanta', 'titulo_diario', 'bajada', 'texto_diario']
    print(postsFinal)
    df = pd.DataFrame(data=postsFinal, columns=columns)
    df.to_csv(nombreArchivoSalida, index=False, columns=columns, sep=';', quotechar='"')


nombreArchivoEntrada = os.path.join(os.path.dirname(__file__), 'data', 'nacion_buscar_links.csv')
nombreArchivoSalida = os.path.join(os.path.dirname(__file__), 'data', 'post_output.csv')
postsConTitulo = addColumnaTitulo(nombreArchivoEntrada)
saveInCsv(postsConTitulo, nombreArchivoSalida)
