# buscarEnPortalesDiarios
Script que permite a partir de un archivo CSV con informacion de posteos de Facebook recuperada por Netvizz, navegar a los portales digitales de los diarios Clarin y LaNacion y recolectar automaticamente la Url original, fecha publicación, tema, volanta, titulo, bajada y texto de cada una de los posteos del archivo de entrada.

El archivo a ingresar post_input.csv, que se encuentra en la carpeta Data, es un archivo csv separado por punto y coma compuesto por 2 columnas:
1-post_id
2-link

Se genera un archivo csv (post_output) en la carpeta data con las siguientes columnas:
1-post_id
2-link
3-UrlCompleta
4-fecha_hora_diario
5-tema
6-volanta
7-titulo_diario
8-bajada
9-texto_diario

## Dependencias
Para utilizar el script es necesario instalar las siguientes librerias python:
- BeautifulSoup4
- Pandas

La instalacion puede hacerse utilizando pip de la siguiente manera:
- \$ su
- \# pip3 install pandas
- \# pip3 install bs4
- \# pip3 install lxml
- \# pip3 install tldextract


Para ejecutar el script una vez posicionado sobre el directorio del proyecto ejecutar:
$ python3 buscarEnPortalesDiarios.py