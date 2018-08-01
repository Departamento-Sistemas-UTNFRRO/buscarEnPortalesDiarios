# -*- coding: utf-8 -*-

#    This file is part of buscarTitulosFacebook.
#
#    buscarTitulosFacebook is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    buscarTitulosFacebook is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with buscarTitulosFacebook; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import pandas as pd
import os
import csv


class DataSetCSV(object):
    def __init__(self, nombreArchivoEntrada, nombreArchivoSalida, columnas, inicio=None, fin=None):
        self.nombreArchivoEntrada = self._armarRutaDatos(nombreArchivoEntrada)
        self.nombreArchivoSalida = self._armarRutaDatos(nombreArchivoSalida)
        self.columnas = columnas
        self.cantidadColumnas = len(columnas)
        self.dataset = self._obtenerDataSet()
        self.inicio = inicio
        if inicio is None:
            self.inicio = 0
        self.fin = fin
        if fin is None:
            self.fin = len(self.dataset)

    def _armarRutaDatos(self, nombreArchivo):
        rutaADatos = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', nombreArchivo)
        return rutaADatos

    def _obtenerDataSet(self):
        csv = pd.read_csv(self.nombreArchivoEntrada, header=0, sep=',', quotechar='\"', encoding="utf-8")
        return csv.values.tolist()

    def guardar(self):
        df = pd.DataFrame(data=self.dataset, columns=self.columnas)
        df.to_csv(self.nombreArchivoSalida, index=False, columns=self.columnas, sep=';', quoting=csv.QUOTE_ALL, doublequote=True, quotechar='"', encoding="utf-8")    