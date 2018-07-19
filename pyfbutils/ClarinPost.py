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

# from Link import Link


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
