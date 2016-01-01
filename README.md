# RiotMongoMatches

Script creado para extraer las partidas de un jugador o de la challenger tier de un servidor, cada partida sera almacenada segun los
parametros ingresados.


#Requisitos:
-Tener instalado PyMongo
-Tener Instalado riotwatcher (Si es posible clonarlo e instalarlo) https://github.com/pseudonym117/Riot-Watcher
-Tener un servidor MongoDB

#Importante:
Como algunas partidas se pueden repetir, la idea es no almacenar dos veces lo mismo en la base de datos, entonces para evitar eso recomiendo ejecutar el siguiente script para volver el match único en la DB

```python
db.matches_stored.createIndex( { matchId: 1 }, { unique: true } )
```


#Uso:
Una vez descargado debes crear un archivo api_key.txt o utilizar el que viene, ahi deberás ingresar tu API KEY proporcionada por
Riot Games.


#Ejemplos

Si deseo obtener las partidas de todos los Challenger del servidor LatinoAmérica Sur y almacenarlas utilizaria de esta manera:

```python
python RiotMongoMatches.py -t 0 -s las -q RANKED_SOLO_5x5 -a SEASON2015 -i localhost
```
Donde -t es el TARGET o el jugador que queremos extraer sus partidas, en este caso es 0 ya que deseo la Challenger Tier

Donde -s es el servidor, debe ser escrito en letra minuscula ej (las, lan, euw, na)

Donde -q es el tipo de cola de los matches que queremos extraer, en este caso todas las partidas clasificatorias de 2015

Donde -a indica la temporada en la cual queremos obtener las partidas, en este caso Temporada 2015 (SEASON2015)

Donde -i indica la IP del servidor MongoDB



#NOTA:

Al ejecutar el script, se crea una DB llamada "matchs" y una colección llamada "matches_stored" , si deseas cambiarle el nombre deberas modificar el script a tu gusto.


El script esta en una fase inicial, por lo que es probable que al alterar algun parametro este no responda de la forma esperada, el script se mejorara a medida del tiempo y de mi disponibilidad.

