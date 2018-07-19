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
import urllib.parse


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
            'tapas.clarin.com',
            '\\N'
        ]

        self.linkMovidos = {
            'http://canchallena.lanacion': 'http://www.lanacion',
            'http://personajes.lanacion': 'http://www.lanacion',
            'https://www.ieco.clarin.com/ieco/economia': 'https://www.clarin.com/economia',
            'a.ln.com.ar': 'www.lanacion.com.ar',
            'clar.in': 'www.clarin.com',
            'mundial-brasil-2014.clarin.com': 'www.clarin.com',
            'arq.clarin.com': 'www.clarin.com',
            'deporteshd.clarin.com': 'www.clarin.com'
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
