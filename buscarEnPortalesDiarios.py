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
from pyfbutils.ClarinPosteo import ClarinPosteo
from pyfbutils.NacionPosteo import NacionPosteo
from pyfbutils.DataSetCSV import DataSetCSV


def buscarInformacionPortales(datasetCSV):
    posteos = datasetCSV.dataset

    for i in range(datasetCSV.inicio, datasetCSV.fin):
        try:
            print(i)
            link_url = posteos[i][1]
            link = Link(link_url)
            if not link.esLinkAOmitir():
                posteos[i].append(link.linkReal)

                if ('lanacion.com' in link.linkReal):
                    postPortal = NacionPosteo(link)
                    posteos[i].append(postPortal.getFecha())
                    posteos[i].append(postPortal.getTema())
                    posteos[i].append(postPortal.getVolanta())
                    posteos[i].append(postPortal.getTitulo())
                    posteos[i].append(postPortal.getBajada())
                    posteos[i].append(postPortal.getTextoDiario())
                elif('clarin.com' in link.linkReal):
                    postPortal = ClarinPosteo(link)
                    posteos[i].append(postPortal.getFecha())
                    posteos[i].append(postPortal.getTema())
                    posteos[i].append(postPortal.getVolanta())
                    posteos[i].append(postPortal.getTitulo())
                    posteos[i].append(postPortal.getBajada())
                    posteos[i].append(postPortal.getTextoDiario())
                else:
                    posteos[i].append("OTRO MEDIO")
                    posteos[i].append("OTRO MEDIO")
                    posteos[i].append("OTRO MEDIO")
                    posteos[i].append("OTRO MEDIO")
                    posteos[i].append("OTRO MEDIO")
                    posteos[i].append("OTRO MEDIO")
            else:
                posteos[i].append("LINK NULL")
                posteos[i].append("LINK NULL")
                posteos[i].append("LINK NULL")
                posteos[i].append("LINK NULL")
                posteos[i].append("LINK NULL")
                posteos[i].append("LINK NULL")
                posteos[i].append("LINK NULL")
        except Exception as ex:
            columnas = len(posteos[i]) + 1
            for _ in range(columnas, datasetCSV.cantidadColumnas):
                posteos[i].append("TIME OUT")
            print("TIME OUT")
            print(ex)


# programaPrincipal
nombreArchivoEntrada = 'post_input.csv'
nombreArchivoSalida = 'post_output.csv'
columnas = ['post_id', 'link', 'UrlCompleta', 'fecha_hora_diario', 'tema', 'volanta', 'titulo_diario', 'bajada', 'texto_diario']

inicio = 0
fin = None

datasetCSV = DataSetCSV(nombreArchivoEntrada, nombreArchivoSalida, columnas, inicio, fin)
buscarInformacionPortales(datasetCSV)
datasetCSV.guardar()
