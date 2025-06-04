import requests
import pickle
import csv
import re

##################################################
# Funciones de lectura
##################################################

def grabaTxt(archivoTxt,datos):
    """
    Funcionamiento:
    Guarda los datos proporcionados en un archivo de texto, sobrescribiendo el contenido anterior.
    Entradas:
    - archivoTxt (str): Nombre del archivo de texto a escribir.
    - datos (str): El texto que se escribirá en el archivo.
    Salidas:
    - NA
    """
    try:
        f=open(archivoTxt,"w")
        f.write(datos)
        f.close()
    except:
        print(f"Error al leer el archivo: {archivoTxt}")
    return

def leeTxtLineas(txt):
    """
    Funcionamiento:
    Lee un archivo de texto y devuelve sus líneas como una lista.
    Entradas:
    - txt (str): Ruta o nombre del archivo a leer.
    Salidas:
    - list[str]: Lista con las líneas del archivo.
    """
    with open(txt, 'r', encoding='utf-8') as f:
        return f.readlines()

def agregarTxt(archivoTxt,datos):
    """
    Funcionamiento:
    Agrega texto al final de un archivo de texto existente.
    Entradas:
    - archivoTxt (str): Nombre del archivo al que se agregará información.
    - datos (str): Texto que se desea añadir.
    Salidas:
    - NA
    """
    try:
        f=open(archivoTxt,"a")
        f.write(datos)
        f.close()
    except:
        print(f"Error al leer el archivo: {archivoTxt}")
    return

def leeTxt(archivoTxt):
    """
    Funcionamiento:
    Lee todo el contenido de un archivo de texto y lo devuelve como una cadena.
    Entradas:
    - archivoTxt (str): Nombre del archivo a leer.
    Salidas:
    - str: Contenido del archivo si se puede leer.
    - False: Si ocurre un error durante la lectura.
    """
    datos = []
    try:
        f=open(archivoTxt,"r")
        datos = f.read()
        f.close()
        return datos
    except:
        return False

def graba(archivo,datos):
    """
    Funcionamiento:
    Guarda datos en un archivo usando serialización binaria con pickle.
    Entradas:
    - archivo (str): Nombre del archivo donde se guardarán los datos.
    - datos: Información que será guardado.
    Salidas:
    - NA
    """
    try:
        f=open(archivo,"wb")
        pickle.dump(datos,f)
        f.close()
    except:
        print(f"Error al leer el archivo: {archivo}")
    return

def lee(archivo):
    """
    Funcionamiento:
    Lee un archivo con formato binario serializado (pickle) y devuelve su contenido.
    Entradas:
    - archivo (str): Nombre del archivo a leer.
    Salidas:
    - datos: Información leído desde el archivo.
    - False: Si ocurre un error durante la lectura.
    """
    datos = []
    try:
        f=open(archivo,"rb")
        datos = pickle.load(f)
        f.close()
    except:
        return False
    return datos

def obtenerCsv(matrizPokemons):
    """
    Funcionamiento:
    Crea un archivo CSV y escribe una matriz de datos de Pokémon en él.
    Entradas:
    - matrizPokemons (matriz): Matriz con la información de los Pokémon.
    Salidas:
    - NA
    """
    try:
        f=open(excelPokemons,"w")
        escritor = csv.writer(f, delimiter=",") #; si el asistente lo quiere ver en diferentes casillas
        escritor.writerows(matrizPokemons)
        f.close()
    except Exception as e:
        print(f"Error al crear el archivo: {e}")

misPokemonsTxt = "Mis pokémons.txt"
misIdAtrapados = "Mis id pokemons atrapados"
misPokemonsAtrapadosPkl = "Mis pokémons atrapados"
matrizPokemonAD = "Matriz de pokémons"
diccPokemonAM = "Diccionario de pokémons"
excelPokemons = "Mis pokémons.csv"

##################################################
# 12. Agregar Pokémon
##################################################

def agregarPokemonIDTxt(id, nombre):
    """
    Funcionamiento:
    Agrega un nuevo Pokémon al archivo de texto si no está registrado. Si ya existe, actualiza su información.
    Entradas:
    - id (str): ID del Pokémon.
    - nombre (str): Nombre del Pokémon.
    Salidas:
    - NA
    """
    txtPokemons = leeTxt(misPokemonsTxt)
    listaID = obtenerIDBuscados(txtPokemons)
    nuevoPokemon = f"{id}^{nombre}^a"
    txtPokemonsActualizado = ""
    if id not in listaID:
        agregarTxt(misPokemonsTxt, nuevoPokemon)
    else:
        listaPokemons = txtPokemons.split("\n")[:-1]
        for pokemon in listaPokemons:
            if re.fullmatch(f"^{id}\\^[a-z\\-]+\\^[a-z]$", pokemon):
                txtPokemonsActualizado += f"{nuevoPokemon}\n"
            else:
                txtPokemonsActualizado += f"{pokemon}\n"
        print(txtPokemonsActualizado)

def obtenerIDBuscados(txtPokemons):
    """
    Funcionamiento:
    Extrae todos los IDs registrados en el archivo de texto de los Pokémon.
    Entradas:
    - txtPokemons (str): Contenido del archivo de texto con datos de Pokémon.
    Salidas:
    - list[str]: Lista de IDs extraídos.
    """
    listaID = []
    listaPokemons = txtPokemons.split("\n")[:-1]
    for pokemon in listaPokemons:
        infoPokemon = pokemon.split("^")
        listaID.append(infoPokemon[0])
    return listaID
    
##################################################
# 11. Virus
##################################################

def manipularEstadisticas(cambio, porcentaje, estadisticas):
    """
    Funcionamiento:
    Modifica las estadísticas de un Pokémon según un porcentaje de aumento o disminución.
    Entradas:
    - cambio (str): 0 para aumentar, 1 para disminuir.
    - porcentaje (str): Porcentaje de modificación.
    - estadisticas (list): Lista con estadísticas del Pokémon: [total, (PS, A, D, AE, DE, V)].
    Salidas:
    - list: Nueva lista con total modificado y estadísticas individuales modificadas.
    """
    listaEstadisticas = []
    porcentaje = int(porcentaje)
    cambio = int(cambio)
    if cambio == 1:
        porcentaje = -(porcentaje)
    totalEstad = 0
    totalEstad = estadisticas[0] + estadisticas[0] * (porcentaje/100)
    totalEstad = round(totalEstad, 2)
    listaEstadisticas.append(totalEstad)
    statsIndividuales = []
    for estad in estadisticas[1]:
        stat = estad + estad * (porcentaje/100)
        stat = round(stat, 2)
        statsIndividuales.append(stat)
    statsIndividuales = tuple(statsIndividuales)
    listaEstadisticas.append(statsIndividuales)
    return listaEstadisticas
    
def validarPorcentajeVirus(cambio, porcentaje):
    """
    Funcionamiento:
    Valida que el porcentaje de modificación para el virus sea adecuado.
    Entradas:
    - cambio (str): 0 para aumentar, 1 para disminuir.
    - porcentaje (str): Porcentaje de modificación.
    Salidas:
    - tuple: (bool, str) donde el booleano indica si es válido y el string contiene el mensaje de error si lo hay.
    """
    try:
        if int(porcentaje) < 0: #Si permite +100%
            return (False, "El porcentaje debe de ser mayor a 0.")
        elif int(cambio) == 1 and int(porcentaje) > 100:
            return (False, "Al disminuir, el porcentaje no puede ser mayor a 100.")
        else:
            return (True, "")
    except ValueError:
        return (False, "El valor tiene que ser un número entero.")
    
##################################################
# 8. esShiny
##################################################

def obtenerIdShiny(infoAtrapados):
    """
    Funcionamiento:
    Filtra los IDs de Pokémon shiny del diccionario y los agrupa en bloques de 100.
    Entradas:
    - infoAtrapados (dict): Diccionario con información de los Pokémon atrapados.
    Salidas:
    - matrizShiny (matriz): Lista que contiene sublistas con hasta 100 IDs shiny cada una.
    """
    listaIdShiny = []
    for id, datos in infoAtrapados.items():
        linkShiny = datos[4]
        if linkShiny != "":
            listaIdShiny.append(id)
    matrizShiny = []
    bloque = []
    for i in range(0, len(listaIdShiny), 100):
        bloque = listaIdShiny[i:i+100]
        matrizShiny.append(bloque)
    return matrizShiny

##################################################
# 6. Xml
##################################################

def obtenerEstadisticas(nombrePokemon):
    nombresCorregidos = {'kakun': 'kakuna','nidorin': 'nidorina','sandslas': 'sandslash','oddis': 'oddish','venomot': 'venomoth',
    'meowt': 'meowth','abr': 'abra','kadabr': 'kadabra','ponyt': 'ponyta','rapidas': 'rapidash','rattat': 'rattata',
    'poliwrat': 'poliwrath','tangel': 'tangela','horse': 'horsea','seadr': 'seadra','chikorit': 'chikorita','quilav': 'quilava',
    'ledyb': 'ledyba','cleff': 'cleffa','sunflor': 'sunflora',"yanm": "yanma","qwilfis": "qwilfish","teddiurs": "teddiursa","slugm": "slugma",
    "kingdr": "kingdra","lugi": "lugia","ho-o": "ho-oh","poochyen": "poochyena","mightyen": "mightyena","kirli": "kirlia",
    "shroomis": "shroomish","slakot": "slakoth","vigorot": "vigoroth","nincad": "nincada","shedinj": "shedinja","makuhit": "makuhita",
    "hariyam": "hariyama","roseli": "roselia","carvan": "carvanha","spind": "spinda","trapinc": "trapinch","vibrav": "vibrava",
    "cacne": "cacnea","altari": "altaria","barboac": "barboach","whiscas": "whiscash","corphis": "corphish","anorit": "anorith",
    "relicant": "relicanth","rayquaz": "rayquaza","torterr": "torterra","corsol": "corsola",
    "staravi": "staravia","tangrowt": "tangrowth","yanmeg": "yanmega","dialg": "dialga","palki": "palkia","cresseli": "cresselia",
    "munn": "munna","musharn": "musharna","zebstrik": "zebstrika","roggenrol": "roggenrola","gigalit": "gigalith","thro": "throh",
    "darumak": "darumaka","sigilyp": "sigilyph","tirtoug": "tirtouga","carracost": "carracosta","trubbis": "trubbish","zoru": "zorua",
    "gothit": "gothita","gothorit": "gothorita","swann": "swanna","vanillis": "vanillish","emolg": "emolga","frillis": "frillish",
    "alomomol": "alomomola","galvantul": "galvantula","larvest": "larvesta","volcaron": "volcarona","meloetta-ari": "meloetta",
    "greninj": "greninja","spewp": "spewpa","amaur": "amaura"} #Diccionario con nombres corregidos, para que se encuentren en el API.
    nombreCorregido = nombresCorregidos.get(nombrePokemon.lower(), nombrePokemon.lower())
    url = f"https://pokeapi.co/api/v2/pokemon/{nombreCorregido}" #Busca en la API el pokémon con el nombre correcto
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200: #Saca los datos de ese pokémon
            datos = respuesta.json()
            total = 0
            for estadistica in datos['stats']:
                total += estadistica['base_stat']
            return total #Retorna el total de estadisticas del pokémon específico
        else:
            print(f"No se encontró el Pokémon: {nombrePokemon}")
            return 0
    except Exception as e:
        print(f"Error al obtener stats de {nombrePokemon}: {e}")
        return 0
    
##################################################
# 2. Atrapar
##################################################

puntosSalud = "hp"
ataque = "attack"
ataqueEspecial = "special-attack"
defensa = "defense"
defensaEspecial = "special-defense"
velocidad = "speed"
    
def validarShiny(info):
    """
    Funcionamiento:
    Verifica si un Pokémon tiene una imagen shiny disponible.
    Entradas:
    - info (dict): Diccionario .json con información del Pokémon obtenido desde la API.
    Salidas:
    - True si la imagen shiny está disponible (no es None).
    - False si no tiene imagen shiny.
    """
    shiny = info['sprites']['front_shiny']
    print(shiny) #Borrar luego, esto es para verificar link shiny ----------------
    if shiny is None:
        return False
    else:
        return True

def obtenerPeso(peso):
    """
    Funcionamiento:
    Convierte el peso recibido (según la API) a gramos.
    Entradas:
    - peso (str): peso del Pokémon.
    Salidas:
    - Peso convertido en gramos (int).
    - Si ocurre un error, devuelve 0.
    """
    try:
        return int(peso) * 10
    except ValueError:
        return 0
    
def obtenerAltura(altura):
    """
    Funcionamiento:
    Convierte la altura recibida (según la API) a centímetros.
    Entradas:
    - altura (int o str): altura del Pokémon.
    Salidas:
    - Altura convertida en centímetros (int).
    - Si ocurre un error, devuelve 0.
    """
    try:
        return int(altura) * 10
    except ValueError:
        return 0
    
def obtenerTotalEstadistica(info):
    """
    Funcionamiento:
    Calcula la suma total de las estadísticas base de un Pokémon.
    Entradas:
    - info (dict): Diccionario .json con información del Pokémon.
    Salidas:
    - Suma de las seis estadísticas base (int).
    """
    salud = obtenerEstadisticaPuntoSalud(info)
    ataque = obtenerEstadisticaAtaque(info)
    defensa = obtenerEstadisticaDefensa(info)
    ataqueEspecial = obtenerEstadisticaAtaqueEspecial(info)
    defensaEspecial = obtenerEstadisticaDefensaEspecial(info)
    velocidad = obtenerEstadisticaVelocidad(info)
    return salud + ataque + defensa + ataqueEspecial + defensaEspecial + velocidad

def obtenerEstadistica(info, tipo):
    """
    Funcionamiento:
    Obtiene el valor base de una estadística específica de un Pokémon.
    Entradas:
    - info (dict): Diccionario .json con información del Pokémon.
    - tipo (str): Nombre de la estadística.
    Salidas:
    - Valor entero de la estadística base solicitada.
    - Si no se encuentra la estadística, devuelve 0.
    """
    estadisticas = info['stats']
    for estadistica in estadisticas:
        if estadistica['stat']['name'] == tipo:
            return estadistica['base_stat']
    return 0

def obtenerEstadisticaPuntoSalud(info):
    """
    Funcionamiento:
    Obtiene la estadística base de Puntos de Salud (HP) del Pokémon.
    Entradas:
    - info (dict): Diccionario .json con la información del Pokémon.
    Salidas:
    - Valor entero de HP.
    """
    return obtenerEstadistica(info, puntosSalud)

def obtenerEstadisticaAtaque(info):
    """
    Funcionamiento:
    Obtiene la estadística base de ataque del Pokémon.
    Entradas:
    - info (dict): Diccionario .json con la información del Pokémon.
    Salidas:
    - Valor entero de ataque.
    """
    return obtenerEstadistica(info, ataque)

def obtenerEstadisticaDefensa(info):
    """
    Funcionamiento:
    Obtiene la estadística base de defensa del Pokémon.
    Entradas:
    - info (dict): Diccionario .json con la información del Pokémon.
    Salidas:
    - Valor entero de defensa.
    """
    return obtenerEstadistica(info, defensa)

def obtenerEstadisticaAtaqueEspecial(info):
    """
    Funcionamiento:
    Obtiene la estadística base de ataque especial del Pokémon.
    Entradas:
    - info (dict): Diccionario .json con la información del Pokémon.
    Salidas:
    - Valor entero de Ataque Especial.
    """
    return obtenerEstadistica(info, ataqueEspecial)

def obtenerEstadisticaDefensaEspecial(info):
    """
    Funcionamiento:
    Obtiene la estadística base de Defensa Especial del Pokémon.
    Entradas:
    - info (dict): Diccionario .json con la información del Pokémon.
    Salidas:
    - Valor entero de Defensa Especial.
    """
    return obtenerEstadistica(info, defensaEspecial)

def obtenerEstadisticaVelocidad(info):
    """
    Funcionamiento:
    Obtiene la estadística base de Velocidad del Pokémon.
    Entradas:
    - info (dict): Diccionario .josn con la información del Pokémon.
    Salidas:
    - Valor entero de Velocidad.
    """
    return obtenerEstadistica(info, velocidad)

def obtenerTipo(info, indice):
    """
    Funcionamiento:
    Obtiene el nombre del tipo del Pokémon según el índice.
    Entradas:
    - info (dict): Diccionario .json con la información del Pokémon.
    - indice (int): índice para acceder al tipo (0 para primer tipo, 1 para segundo tipo, etc.)
    Salidas:
    - String con el nombre del tipo si existe; si no, string vacío.
    """
    try:
        return info['types'][indice]['type']['name']
    except IndexError:
        return "" # Mostrar un String vacio cuando no encuentra el indice
    
def obtenerImagen(info):
    """
    Funcionamiento:
    Obtiene la URL de la imagen del Pokémon.
    Prefiere la imagen shiny si está disponible; si no, devuelve la imagen normal.
    Entradas:
    - info (dict): Diccionario .json con la información del Pokémon.
    Salidas:
    - URL (string) de la imagen shiny si existe, o imagen normal en caso contrario.
    """
    shiny = validarShiny(info)
    if shiny == True:
        return info['sprites']['front_shiny']
    else:
        return info['sprites']['front_default']

def obtenerPokemonsAtrapados(listaRandomAtrapados):
    """
    Funcionamiento:
    Obtiene información detallada de los Pokémon atrapados consultando la API.
    Construye un diccionario con datos relevantes y lo guarda.
    Entradas:
    - listaRandomAtrapados (list): Lista de cadenas con formato "id^nombre^estado" de Pokémon atrapados.
    Salidas:
    - Guarda el diccionario de Pokémon en un archivo binario.
    """
    diccionarioPokemons = {}
    for pokemon in listaRandomAtrapados:
        id = pokemon.split("^")[0] # Obtener el id del Pokemon
        respuesta = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
        if respuesta.ok:
            info = respuesta.json()
            salud = obtenerEstadisticaPuntoSalud(info)
            ataque = obtenerEstadisticaAtaque(info)
            defensa = obtenerEstadisticaDefensa(info)
            ataqueEspecial = obtenerEstadisticaAtaqueEspecial(info)
            defensaEspecial = obtenerEstadisticaDefensaEspecial(info)
            velocidad = obtenerEstadisticaVelocidad(info)
            totalStats = obtenerTotalEstadistica(info)
            # Asignar el valor al pokemon
            diccionarioPokemons[int(id)] = [info['name'], # nombre
                                             (validarShiny(info), obtenerPeso(info['weight']), obtenerAltura(info['height'])), # (esShiny, peso, altura)
                                             [totalStats, (salud, ataque, defensa, ataqueEspecial, defensaEspecial, velocidad)], # [totalEstad, (PS, A, D, AE, DE, V)]
                                             (obtenerTipo(info, 0), obtenerTipo(info, 1)), # (listaDeTipos, listaDeTipos)
                                              obtenerImagen(info) # url
                                            ]
        else:
            print("Error", respuesta.status_code)
    graba(misPokemonsAtrapadosPkl, diccionarioPokemons) # Lo guardamos en memoria secundaria con el fin de hacerlo más eficiente.
    pokemonsAtrapados = lee(misPokemonsAtrapadosPkl) # Borrar luego -----------------
    print(pokemonsAtrapados) # Borrar luego -----------------

def obtenerIdAtrapados(listaRandomAtrapados):
    """
    Funcionamiento:
    Extrae los IDs de los Pokémon atrapados de la lista dada y los guarda en un archivo.
    Entradas:
    - listaRandomAtrapados (list): Lista de cadenas con formato "id^nombre^estado".
    Salidas:
    - Guarda la lista de IDs en un archivo binario.
    """
    listaIdAtrapados = []
    for pokemon in listaRandomAtrapados:
        infoPokemon = pokemon.split("^")
        listaIdAtrapados.append(infoPokemon[0])
    print(listaIdAtrapados) # Borrar luego -----------------
    graba(misIdAtrapados, listaIdAtrapados)

def actualizarPokemonsTxt(listaPokemons, listaRandomAtrapados):
    """
    Funcionamiento:
    Actualiza el archivo de texto que almacena el estado de cada Pokémon, 
    Entradas:
    - listaPokemons (list): Lista de cadenas "id^nombre^estado" con estado anterior.
    - listaRandomAtrapados (list): Lista de cadenas "id^nombre^estado" que representa los atrapados actuales.
    Salidas:
    - Guarda el archivo de texto actualizado con los nuevos estados.
    """
    misPokemons = ""
    for pokemon in listaPokemons:
        if pokemon in listaRandomAtrapados:
            misPokemons += f"{pokemon.strip("^a").strip("^h")}^a\n" # Usar strip para evitar valores viejos
        else:
            misPokemons += f"{pokemon.strip("^a").strip("^h")}^h\n" # Usar strip para evitar valores viejos
    # Guardar los cambios en el archivo "Mis Pokemons"
    grabaTxt(misPokemonsTxt, misPokemons)
    
def validarPorcentaje(porcentaje):
    """
    Funcionamiento:
    Valida que el porcentaje ingresado sea un número entero entre 0 y 100.
    Entradas:
    - porcentaje (str): Valor a validar.
    Salidas:
    - tuple(bool, str): (True, "") si válido; (False, mensaje de error) si inválido.
    """
    try:
        if int(porcentaje) < 0 or int(porcentaje) > 100:
            return (False, "El porcentaje debe de ser entre 0 y 100.")
        else:
            return (True, "")
    except ValueError:
        return (False, "El valor tiene que ser un número entero.")
    
##################################################
# 1. Buscar
##################################################

def obtenerLimitePokemon():
    """
    Funcionamiento:
    Consulta la API de Pokémon para obtener el número total de Pokémon disponibles.
    Entradas:
    - NA
    Salidas:
    - int: Cantidad total de Pokémon disponibles en la API.
    """
    url = "https://pokeapi.co/api/v2/pokemon"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return datos["count"]
    return False