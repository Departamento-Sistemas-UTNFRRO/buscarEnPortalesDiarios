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


class Link(object):
    def __init__(self, linkURL):
        self.linksAOmitir = [
            'https://www.facebook.com/lanacion/photos',
            'https://www.facebook.com/lanacion/videos',
            'https://www.facebook.com/lndeportes/photos',
            'https://www.facebook.com/clarincom/videos',
            'https://www.facebook.com/clarincom/photos',
            'http://www.youtube.com',
            'http://youtu.be/',
            'blogs.lanacion',
            '\\N'
        ]

        self.linkMovidos = {
            'http://canchallena.lanacion': 'http://www.lanacion',
            'http://personajes.lanacion': 'http://www.lanacion',
            'https://www.ieco.clarin.com/ieco/economia': 'https://www.clarin.com/economia',
        }

        self.linkOriginal = linkURL

        for viejo in self.linkMovidos:
            if(viejo in self.linkOriginal):
                self.linkOriginal = self.linkOriginal.replace(viejo, self.linkMovidos[viejo])

        self.req = urllib.request.Request(self.linkOriginal)
        self.linkReal = self.alargar_url(self.req)
        self.linkDomain = self.getLinkDomain()

    def esLinkAOmitir(self):
        '''Determina si el link puede ser procesado o no'''
        if pd.isnull(self.linkOriginal):
            return False

        for linkAOmitir in self.linksAOmitir:
            if linkAOmitir in self.linkOriginal:
                return True

        if self.linkReal is None or pd.isnull(self.linkReal):
            return True

        return False

    def getLinkDomain(self):
        '''Devuelve el dominio del link'''
        parsed_uri = urllib.parse.urlparse(self.linkReal)
        return '{uri.netloc}'.format(uri=parsed_uri)

    def alargar_url(self, req):
        try:
            resolvedURL = urllib.request.urlopen(req)
            return resolvedURL.url
        except Exception as ex:
            print("ERROR" + str(ex))
        return None

    def getHtmlSoup(self):
        try:
            resp = urllib.request.urlopen(self.req)
            html = resp.read()
            soup = bs4.BeautifulSoup(html, 'html.parser')
            return soup
        except Exception as ex:
            print("ERROR" + str(ex))
            return None


class NacionPost(object):
    def __init__(self, link):
        self.soup = link.getHtmlSoup()

    def getFecha(self):
        fechaNacion = "FECHA NO ENCONTRADA"
        if self.soup is None:
            return fechaNacion

        try:
            for tag in self.soup.find_all("meta"):
                if tag.get("itemprop", None) == "datePublished":
                        return tag.get("content", None)
            contenedor = self.soup.find(class_='fecha')
            if contenedor is not None:
                fechaCompleta = contenedor.getText()
                fechaCompleta = fechaCompleta.replace('\xa0', '')
                fechaCompleta = fechaCompleta.replace('de', '')
                fechaCompleta = fechaCompleta.replace('•', '')
                fechaCompleta = fechaCompleta.replace('  ', ' ')
                fechaCompleta = fechaCompleta.replace('  ', ' ')
                fechaCompleta = fechaCompleta.strip()
                locale.setlocale(locale.LC_TIME, 'es_AR')
                if '•' in contenedor.getText():
                    fechaCompleta = datetime.strptime(
                        fechaCompleta, '%d %B %Y %H:%M')
                else:
                    fechaCompleta = datetime.strptime(
                        fechaCompleta, '%d %B %Y')
                fechaNacion = fechaCompleta.strftime('%d/%m/%Y %H:%M:%S')
        except Exception as ex:
            print("ERROR" + str(ex))
        return fechaNacion

    def getTema(self):
        result = "TEMA NO ENCONTRADO"
        if self.soup is None:
            return result

        try:
            contenedor = self.soup.find(class_='temas')
            if contenedor is not None:
                elementosContenedor = contenedor.find_all("a")
                if elementosContenedor is not None:
                    return elementosContenedor[0].getText()

            contenedor = self.soup.find(class_='path floatFix breadcrumb')
            if contenedor is None:
                contenedor = self.soup.find(class_='path patrocinado floatFix breadcrumb')
            if contenedor is not None:
                elementosContenedor = contenedor.find_all("span")
                if elementosContenedor is not None:
                    tag = elementosContenedor[1]
                    if tag.get("itemprop", None) == "name":
                        return tag.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
        return result

    def getVolanta(self):
        result = "VOLANTA NO ENCONTRADA"
        if self.soup is None:
            return result

        try:
            contenedor = self.soup.find(class_='temas')
            if contenedor is not None:
                elementosContenedor = contenedor.find_all("a")
                if elementosContenedor is not None and len(elementosContenedor) > 1:
                    return elementosContenedor[1].getText()

            contenedor = self.soup.find(class_='path floatFix breadcrumb')
            if contenedor is None:
                contenedor = self.soup.find(class_='path patrocinado floatFix breadcrumb')
            if contenedor is None:
                contenedor = self.soup.find(class_='path tema-espacio-hsbc floatFix breadcrumb')
            if contenedor is not None:
                elementosContenedor = contenedor.find_all("span")
                if elementosContenedor is not None and len(elementosContenedor) > 2:
                    tag = elementosContenedor[2]
                    if tag.get("itemprop", None) == "name":
                        return tag.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
        return result

    def getTitulo(self):
        result = "TITULO NO ENCONTRADO"
        if self.soup is None:
            return result

        try:
            if self.soup.h1 is not None:
                result = self.soup.h1.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
        return result

    def getBajada(self):
        texto = "BAJADA NO ENCONTRADA"
        if self.soup is None:
            return texto
        try:
            bajada = self.soup.find(class_="bajada")
            # porque class es una palabra reservada
            if bajada is not None:
                texto = bajada.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
        return texto

    def getTextoDiario(self):
        texto = "TEXTO DIARIO NO ENCONTRADO"
        if self.soup is None:
            return texto

        try:
            cuerpo = self.soup.find(id='cuerpo')
            if cuerpo is not None:
                parrafos = cuerpo.find_all('p')
                texto = ""
                for p in parrafos:
                    texto = texto + p.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
        return texto


class ClarinPost(object):
    def __init__(self, link):
        self.soup = link.getHtmlSoup()

    def getTitulo(self):
        result = "TITULO NO ENCONTRADO"
        if self.soup is None:
            return result

        try:
            if self.soup.h1 is not None:
                result = self.soup.h1.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
        return result

    def getTextoDiario(self):
        texto = "TEXTO DIARIO NO ENCONTRADO"
        if self.soup is None:
            return texto

        try:
            cuerpo = self.soup.find(class_='body-nota')
            # porque class es una palabra reservada
            if cuerpo is not None:
                parrafos = cuerpo.find_all('p')
                texto = ""
                for p in parrafos:
                    texto = texto + p.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
        return texto

    def getFecha(self):
        for tag in self.soup.find_all("meta"):
            if tag.get("itemprop", None) == "datePublished":
                return tag.get("content", None)
        return "FECHA NO ENCONTRADA"

    def getTema(self):
        texto = "TEMA  NO ENCONTRADO"
        if self.soup is None:
            return texto

        try:
            # Clarín
            tema = self.soup.find(class_='header-section-name')
            texto = ""
            if tema is not None:
                texto = tema.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
        return texto

    def getVolanta(self):
        texto = "VOLANTA NO ENCONTRADA"
        if self.soup is None:
            return texto

        try:
            volanta = self.soup.find(class_='volanta')
            texto = ""
            if volanta is not None:
                texto = volanta.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
        return texto

    def getBajada(self):
        texto = "BAJADA NO ENCONTRADA"
        if self.soup is None:
            return texto

        try:
            bajada = self.soup.find(class_='bajada')
            if bajada is not None:
                parrafos = bajada.find_all('p')
                texto = ""
                for p in parrafos:
                    texto = texto + p.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
        return texto


def buscarInformacionPortales(posts, inicio, fin, tamañoLote):
    # calcular la cantidad de lotes
    cantidadAProcesar = fin - inicio
    cantidadLotes = cantidadAProcesar // tamañoLote

    for l in range(0, cantidadLotes):
        inicioLote = inicio + l * tamañoLote
        finLote = inicioLote + tamañoLote
        nombreArchivoSalidaLote = "post_ouput_lote_" + str(l) + "_" + str(inicioLote) + "_" + str(finLote) + ".csv"
        nombreArchivoSalidaLote = armarRutaDatos(nombreArchivoSalidaLote)

        for i in range(inicioLote, finLote):
            try:
                print(i)
                link_url = posts[i][3]
                link = Link(link_url)
                if not link.esLinkAOmitir():
                    posts[i][4] = link.linkDomain
                    posts[i].append(link.linkReal)

                    if ('lanacion.com' in link.linkReal):
                        postPortal = NacionPost(link)
                        posts[i].append(postPortal.getFecha())
                        posts[i].append(postPortal.getTema())
                        posts[i].append(postPortal.getVolanta())
                        posts[i].append(postPortal.getTitulo())
                        posts[i].append(postPortal.getBajada())
                        posts[i].append(postPortal.getTextoDiario())
                    elif('clarin.com' in link.linkReal):
                        postPortal = ClarinPost(link)
                        posts[i].append(postPortal.getFecha())
                        posts[i].append(postPortal.getTema())
                        posts[i].append(postPortal.getVolanta())
                        posts[i].append(postPortal.getTitulo())
                        posts[i].append(postPortal.getBajada())
                        posts[i].append(postPortal.getTextoDiario())
                    else:
                        posts[i].append("OTRO MEDIO")
                        posts[i].append("OTRO MEDIO")
                        posts[i].append("OTRO MEDIO")
                        posts[i].append("OTRO MEDIO")
                        posts[i].append("OTRO MEDIO")
                        posts[i].append("OTRO MEDIO")
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

        guardarEnCSV(posts, nombreArchivoSalidaLote)

    return posts


def loadCsvIntoDataSet(nombreArchivoEntrada):
    csv = pd.read_csv(nombreArchivoEntrada, header=0, sep=',', quotechar='\"', encoding="utf-8")
    return csv.values


def guardarEnCSV(postsFinal, nombreArchivoSalida):
    columns = ['tipo_post', 'post_id', 'post_link', 'link', 'link_domain', 'post_message', 'UrlCompleta', 'fecha_hora_diario', 'tema', 'volanta', 'titulo_diario', 'bajada', 'texto_diario']
    df = pd.DataFrame(data=postsFinal, columns=columns)
    df.to_csv(nombreArchivoSalida, index=False, columns=columns, sep=';', quoting=csv.QUOTE_ALL, doublequote=True, quotechar='"', encoding="utf-8")


def armarRutaDatos(nombreArchivo):
    rutaADatos = os.path.join(os.path.dirname(__file__), 'data', nombreArchivo)
    return rutaADatos


nombreArchivoEntrada = armarRutaDatos('post_input_1000_5000.csv')
posts = loadCsvIntoDataSet(nombreArchivoEntrada).tolist()

inicio = 100
fin = len(posts)
tamañoLote = 10
postsConTitulo = buscarInformacionPortales(posts, inicio, fin, tamañoLote)
