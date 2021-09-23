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


class NacionPosteo(object):
    def __init__(self, link):
        '''Inicia un posteo de Clarin, el parametro link debe ser una instancia de la clase Link'''
        self.HtmlParseado = link.obtenerHtmlParseada()

    def getFecha(self):
        fechaNacion = "FECHA NO ENCONTRADA"
        if self.HtmlParseado is None:
            return fechaNacion

        try:
            for etiqueta in self.HtmlParseado.find_all("meta"):
                if etiqueta.get("property", None) == "article:published_time":
                    fechaCompleta = etiqueta.get("content", None)
                    fechaCompleta = fechaCompleta.replace('T', ' ')[:19]
                    return fechaCompleta
        except Exception as ex:
            print("ERROR" + str(ex))
        return fechaNacion

    def getTema(self):
        resultado = "TEMA NO ENCONTRADO"
        if self.HtmlParseado is None:
            return resultado

        for etiqueta in self.HtmlParseado.find_all("meta"):
            if etiqueta.get("name", None) == "parsely-section":
                return etiqueta.get("content", None)

        return resultado

    def getVolanta(self):
        resultado = ""
        if self.HtmlParseado is None:
            return resultado

        try:
            contenedor = self.HtmlParseado.find("div", class_='temas')
            if contenedor is not None:
                elementosContenedor = contenedor.find_all("a")
                if elementosContenedor is not None and len(elementosContenedor) > 1:
                    return elementosContenedor[1].getText().replace("\r\n", "").strip()

            contenedor = self.HtmlParseado.find(class_='path floatFix breadcrumb')
            if contenedor is None:
                contenedor = self.HtmlParseado.find(class_='path patrocinado floatFix breadcrumb')
            if contenedor is None:
                contenedor = self.HtmlParseado.find(class_='path tema-espacio-hsbc floatFix breadcrumb')
            if contenedor is not None:
                elementosContenedor = contenedor.find_all("span")
                if elementosContenedor is not None and len(elementosContenedor) > 2:
                    etiqueta = elementosContenedor[2]
                    if etiqueta.get("itemprop", None) == "name":
                        return etiqueta.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
        return resultado

    def getTitulo(self):
        resultado = "TITULO NO ENCONTRADO"
        if self.HtmlParseado is None:
            return resultado

        for etiqueta in self.HtmlParseado.find_all("meta"):
            if etiqueta.get("property", None) == "og:title":
                return etiqueta.get("content", None)
        return resultado

    def getBajada(self):
        texto = "BAJADA NO ENCONTRADA"
        if self.HtmlParseado is None:
            return texto

        for etiqueta in self.HtmlParseado.find_all("meta"):
            if etiqueta.get("property", None) == "og:description":
                return etiqueta.get("content", None)
        return texto

    def getTextoDiario(self):
        texto = "TEXTO DIARIO NO ENCONTRADO"
        if self.HtmlParseado is None:
            return texto

        try:
            parrafos = self.HtmlParseado.find_all("p", {"class": "com-paragraph"})
            texto = ""
            for p in parrafos:
                texto = texto + p.getText()
        except Exception as ex:
            print("ERROR" + str(ex))
            print(texto)
        return texto
