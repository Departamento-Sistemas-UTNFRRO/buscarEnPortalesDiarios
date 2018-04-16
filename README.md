# buscarEnPortalesDiarios
Script python compatible con la version 3 que permite a partir de un archivo csv con informacion de posteos de Facebook recuperada por Netvizz, navegar a los portales digitales de los diarios Clarin y LaNacion y recolectar automaticamente la Url original, fecha publicación, tema, volanta, titulo, bajada y texto de cada una de los posteos del archivo de entrada.
El archivo a ingresar post_input.csv, que se encuentra en la carpeta Data, es un archivo csv separado por punto y coma compuesto por 5 columnas:
1-tipo_post
2-post_id	
3-post_link	
4-link_fb
5-link_domain
6-link_domain
7-post_message
El script un archivo csv como salida en la carpeta data.