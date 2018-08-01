# buscarEnPortalesDiarios
Script python compatible con la version 3 que permite a partir de un archivo CSV con informacion de posteos de Facebook recuperada por Netvizz, navegar a los portales digitales de los diarios Clarin y LaNacion y recolectar automaticamente la Url original, fecha publicación, tema, volanta, titulo, bajada y texto de cada una de los posteos del archivo de entrada.
El archivo a ingresar post_input.csv, que se encuentra en la carpeta Data, es un archivo csv separado por punto y coma compuesto por 2 columnas:
1-post_id
2-link
El script genera un archivo csv como salida en la carpeta data.
Para usar posicionado sobre el directorio del proyecto ejecutar:
$ python3 buscarEnPortalesDiarios.py