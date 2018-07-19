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

from datetime import datetime
import locale
# from Link import Link


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