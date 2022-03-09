# Documentación

En el archivo report.md se explican los detalles de la implementación del proyecto. A continuación se pueden encontrar indicaciones para su uso.

## Readme

Para ejecutar el compilador de Cool que aquí se presenta existen ciertos requerimientos a tener en cuenta. En el archivo *requirements.py* que se encuentra en el directorio raiz del proyecto se encuentran listados los mismos. 

Para una rápida instalación de todas estas dependencias se debe ejecutar el siguiente comando:

```bash
$ pip install -r requirements.txt
```

Una vez añadidas las mismas se puede proceder a compilador un código dado en Cool a ensamblador. Con este fin, ejecute:

```bash
$ ./coolc.sh <path_to_file/file_name.cl>
```

en una consola centrada en el directorio *src* que se encuentra en la raiz del proyecto. Aquí <file_name.cl> sería un archivo escrito en cool. 

El *output* esperado es un archivo con el mismo nombre pero en .mips, el cual debe correrse con el correspondiente intérprete:

```bash
$ spim -file <path_to_file/file_name.mips>
```

que finalmente nos mostrará el resultado correspondiente al programa de entrada.