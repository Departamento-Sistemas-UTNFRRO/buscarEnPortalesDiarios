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


class ClarinPosteo(object):
    def __init__(self, link):
        '''Inicia un posteo de Clarin, el parametro link debe ser una instancia de la clase Link'''
        self.HtmlParseado = link.obtenerHtmlParseada()

    def getTitulo(self):
        resultado = "TITULO NO ENCONTRADO"
        if self.HtmlParseado is None:
            return resultado

        for etiqueta in self.HtmlParseado.find_all("meta"):
            if etiqueta.get("property", None) == "og:title":
                return etiqueta.get("content", None)
        try:
            if self.HtmlParseado.h1 is not None:
                resultado = self.HtmlParseado.h1.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
        return resultado

    def getTextoDiario(self):
        texto = "TEXTO DIARIO NO ENCONTRADO"
        if self.HtmlParseado is None:
            return texto

        try:
            cuerpo = self.HtmlParseado.find(class_='body-nota')
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

        for etiqueta in self.HtmlParseado.find_all("meta"):
            if etiqueta.get("itemprop", None) == "datePublished":
                return etiqueta.get("content", None)
            if etiqueta.get("name", None) == "cXenseParse:recs:publishtime":
                fechaCompleta = etiqueta.get("content", None)
                fechaCompleta = fechaCompleta.replace('T', ' ')[:19]
                return fechaCompleta
        return resultado

    def getTema(self):
        texto = "TEMA  NO ENCONTRADO"
        if self.HtmlParseado is None:
            return texto

        for etiqueta in self.HtmlParseado.find_all("meta"):
            if etiqueta.get("name", None) == "cXenseParse:gca-categories":
                return etiqueta.get("content", None)

        try:
            # Clarín
            tema = self.HtmlParseado.find(class_='header-section-name')
            texto = ""
            if tema is not None:
                texto = tema.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
        return texto

    def getVolanta(self):
        texto = "VOLANTA NO ENCONTRADA"
        if self.HtmlParseado is None:
            return texto

        for etiqueta in self.HtmlParseado.find_all("meta"):
            if etiqueta.get("name", None) == "cXenseParse:recs:volanta":
                return etiqueta.get("content", None)

        try:
            volanta = self.HtmlParseado.find(class_='volanta')
            texto = ""
            if volanta is not None:
                texto = volanta.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
        return texto

    def getBajada(self):
        texto = "BAJADA NO ENCONTRADA"
        if self.HtmlParseado is None:
            return texto

        for etiqueta in self.HtmlParseado.find_all("meta"):
            if etiqueta.get("property", None) == "og:description":
                return etiqueta.get("content", None)

        try:
            bajada = self.HtmlParseado.find(class_='bajada')
            if bajada is not None:
                parrafos = bajada.find_all('p')
                texto = ""
                for p in parrafos:
                    texto = texto + p.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
        return texto
