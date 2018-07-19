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

from pyfbutils.Link import Link
from pyfbutils.ClarinPost import ClarinPost
from pyfbutils.NacionPost import NacionPost
from pyfbutils.DataSetCSV import DataSetCSV


def buscarInformacionPortales(datasetCSV):
    posts = datasetCSV.dataset

    for i in range(datasetCSV.inicio, datasetCSV.fin):
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
            for _ in range(columnas, datasetCSV.cantidadColumnas):
                posts[i].append("TIME OUT")
            print("TIME OUT")
            print(ex)


# programaPrincipal
nombreArchivoEntrada = 'post_input_1000_5000.csv'
nombreArchivoSalida = 'post_output.csv'
columnas = ['tipo_post', 'post_id', 'post_link', 'link', 'link_domain', 'post_message', 'UrlCompleta', 'fecha_hora_diario', 'tema', 'volanta', 'titulo_diario', 'bajada', 'texto_diario']

inicio = 0
fin = None

datasetCSV = DataSetCSV(nombreArchivoEntrada, nombreArchivoSalida, columnas, inicio, fin)
buscarInformacionPortales(datasetCSV)
datasetCSV.guardar()
