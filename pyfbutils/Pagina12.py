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


class Pagina12Posteo(object):
    def __init__(self, link):
        '''Inicia un posteo de Clarin, el parametro link debe ser una instancia de la clase Link'''
        self.HtmlParseado = link.obtenerHtmlParseada()

    def getTitulo(self):
        resultado = "TITULO NO ENCONTRADO"
        if self.HtmlParseado is None:
            return resultado

        for etiqueta in self.HtmlParseado.find_all("h2"):
            return etiqueta.getText()
        return resultado

    def getTextoDiario(self):
        texto = "TEXTO DIARIO NO ENCONTRADO"
        if self.HtmlParseado is None:
            return texto

        try:
            cuerpo = self.HtmlParseado.find(id='cuerpo')
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
        resultado = "FECHA NO ENCONTRADA"
        if self.HtmlParseado is None:
            return resultado

        contenedor = self.HtmlParseado.find(class_='fecha_edicion')
        if contenedor is not None:
            fechaCompleta = contenedor.getText()
            fechaCompleta = fechaCompleta.replace('\xa0', '')
            fechaCompleta = fechaCompleta.replace('de', '')
            fechaCompleta = fechaCompleta.replace('•', '')
            fechaCompleta = fechaCompleta.replace('  ', ' ')
            fechaCompleta = fechaCompleta.replace('  ', ' ')
            fechaCompleta = fechaCompleta.strip()
            locale.setlocale(locale.LC_TIME, 'es_AR')
            fechaCompleta = datetime.strptime(
            fechaCompleta, '%A, %d %B %Y')
            resultado = fechaCompleta.strftime('%d/%m/%Y %H:%M:%S')
        return resultado

    def getTema(self):
        texto = "TEMA  NO ENCONTRADO"
        if self.HtmlParseado is None:
            return texto

        volanta = self.HtmlParseado.find(class_='volanta')
        if volanta is not None:
            for etiqueta in volanta.find_all("a", {"class": "cprincipal"}):
                return etiqueta.getText()
            for etiqueta in volanta.find_all("span", {"class": "hora cultimas"}):
                return "Ultimas Noticias"
        
        for etiqueta in self.HtmlParseado.find_all("div", {"class": "logosuple top12"}):
            return "Las 12"

        return texto

    def getVolanta(self):
        texto = ""
        if self.HtmlParseado is None:
            return texto

        try:
            volanta = self.HtmlParseado.find(class_='volanta')
            texto = ""
            if volanta is not None:
                texto = volanta.getText()
                texto = texto.split("›", 1)
                if len(texto) == 2:
                    return texto[1]
                else:
                    texto = ""
            volanta = self.HtmlParseado.find(class_='volantasuple')
            if volanta:
                return volanta.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
        return texto

    def getBajada(self):
        texto = "BAJADA NO ENCONTRADA"
        if self.HtmlParseado is None:
            return texto

        try:
            volanta = self.HtmlParseado.find(class_='fgprincipal')
            texto = ""
            if volanta is not None:
                texto = volanta.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
        return texto
