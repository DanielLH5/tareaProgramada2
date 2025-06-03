import requests
import pickle
import csv
import re
from funciones import * 

##################################################
# Funciones de lectura
##################################################

def grabaTxt(archivoTxt,datos):
    try:
        f=open(archivoTxt,"w")
        f.write(datos)
        f.close()
    except:
        print(f"Error al leer el archivo: {archivoTxt}")
    return

def leeTxtLineas(txt):
    with open(txt, 'r', encoding='utf-8') as f:
        return f.readlines()

def agregarTxt(archivoTxt,datos):
    try:
        f=open(archivoTxt,"a")
        f.write(datos)
        f.close()
    except:
        print(f"Error al leer el archivo: {archivoTxt}")
    return

def leeTxt(archivoTxt):
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
    Funcionamiento: Escribe en el archivo en modo escritura binaria. 
    Entradas: El archivo y los nuevos datos.
    Salidas: Guarda los datos en memoria externa.
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
    Funcionamiento: Lee el archivo en modo lectura binaria. 
    Entradas: El archivo.
    Salidas: Devuelve el elchivo.
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
    txtPokemons = leeTxt(misPokemonsTxt)
    listaID = obtenerIDBuscados(txtPokemons)
    nuevoPokemon = f"{id}^{nombre}^a"
    #print(nuevoPokemon) # Borrar luego -----------------
    txtPokemonsActualizado = ""
    if id not in listaID:
        agregarTxt(misPokemonsTxt, nuevoPokemon)
        #txtActualizado = leeTxt(misPokemonsTxt) # Borrar luego -----------------
        #print(txtActualizado) # Borrar luego -----------------
    else:
        listaPokemons = txtPokemons.split("\n")[:-1]
        for pokemon in listaPokemons:
            if re.fullmatch(f"^{id}\\^[a-z\\-]+\\^[a-z]$", pokemon):
                txtPokemonsActualizado += f"{nuevoPokemon}\n"
            else:
                txtPokemonsActualizado += f"{pokemon}\n"
        print(txtPokemonsActualizado)

def obtenerIDBuscados(txtPokemons):
    listaID = []
    listaPokemons = txtPokemons.split("\n")[:-1]
    for pokemon in listaPokemons:
        infoPokemon = pokemon.split("^")
        listaID.append(infoPokemon[0])
    #print(listaID) # Borrar luego -----------------
    return listaID
    
##################################################
# 11. Virus
##################################################

def manipularEstadisticas(cambio, porcentaje, estadisticas):
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
    url = f"https://pokeapi.co/api/v2/pokemon/{nombreCorregido}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            total = 0
            for stat in data['stats']:
                total += stat['base_stat']
            return total
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
    shiny = info['sprites']['front_shiny']
    print(shiny) #Borrar luego, esto es para verificar link shiny ----------------
    if shiny is None:
        return False
    else:
        return True

def obtenerPeso(peso):
    try:
        return int(peso) * 10
    except ValueError:
        return 0
    
def obtenerAltura(altura):
    try:
        return int(altura) * 10
    except ValueError:
        return 0
    
def obtenerTotalEstadistica(info):
    salud = obtenerEstadisticaPuntoSalud(info)
    ataque = obtenerEstadisticaAtaque(info)
    defensa = obtenerEstadisticaDefensa(info)
    ataqueEspecial = obtenerEstadisticaAtaqueEspecial(info)
    defensaEspecial = obtenerEstadisticaDefensaEspecial(info)
    velocidad = obtenerEstadisticaVelocidad(info)
    return salud + ataque + defensa + ataqueEspecial + defensaEspecial + velocidad

def obtenerEstadistica(info, tipo):
    estadisticas = info['stats']
    for estadistica in estadisticas:
        if estadistica['stat']['name'] == tipo:
            return estadistica['base_stat']
    return 0

def obtenerEstadisticaPuntoSalud(info):
    return obtenerEstadistica(info, puntosSalud)

def obtenerEstadisticaAtaque(info):
    return obtenerEstadistica(info, ataque)

def obtenerEstadisticaDefensa(info):
    return obtenerEstadistica(info, defensa)

def obtenerEstadisticaAtaqueEspecial(info):
    return obtenerEstadistica(info, ataqueEspecial)

def obtenerEstadisticaDefensaEspecial(info):
    return obtenerEstadistica(info, defensaEspecial)

def obtenerEstadisticaVelocidad(info):
    return obtenerEstadistica(info, velocidad)

def obtenerTipo(info, indice):
    try:
        return info['types'][indice]['type']['name']
    except IndexError:
        return "" # Mostrar un String vacio cuando no encuentra el indice
    
def obtenerImagen(info):
    shiny = validarShiny(info)
    if shiny == True:
        return info['sprites']['front_shiny']
    else:
        return info['sprites']['front_default']

def obtenerPokemonsAtrapados(listaRandomAtrapados):
    # Crear el diccionario
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
            info = respuesta.json()
            # Asignar el valor al pokemon
            diccionarioPokemons[int(id)] = [info['name'], # nombre
                                             (validarShiny(info), obtenerPeso(info['weight']), obtenerAltura(info['height'])), # (esShiny, peso, altura)
                                             [totalStats, (salud, ataque, defensa, ataqueEspecial, defensaEspecial, velocidad)], # [totalEstad, (PS, A, D, AE, DE, V)]
                                             (obtenerTipo(info, 0), obtenerTipo(info, 1)), # (listaDeTipos, listaDeTipos)
                                              obtenerImagen(info) # url
                                            ]
        else:
            print("Error", respuesta.status_code)
    # Guardar el archivo
    graba(misPokemonsAtrapadosPkl, diccionarioPokemons) # Lo guardamos en memoria secundaria con el fin de hacerlo más eficiente.
    pokemonsAtrapados = lee(misPokemonsAtrapadosPkl) # Borrar luego -----------------
    print(pokemonsAtrapados) # Borrar luego -----------------

def obtenerIdAtrapados(listaRandomAtrapados):
    listaIdAtrapados = []
    for pokemon in listaRandomAtrapados:
        infoPokemon = pokemon.split("^")
        listaIdAtrapados.append(infoPokemon[0])
    print(listaIdAtrapados) # Borrar luego -----------------
    graba(misIdAtrapados, listaIdAtrapados)

def actualizarPokemonsTxt(listaPokemons, listaRandomAtrapados):
    misPokemons = ""
    for pokemon in listaPokemons:
        if pokemon in listaRandomAtrapados:
            misPokemons += f"{pokemon.strip("^a").strip("^h")}^a\n" # Usar strip para evitar valores viejos
        else:
            misPokemons += f"{pokemon.strip("^a").strip("^h")}^h\n" # Usar strip para evitar valores viejos
    # Guardar los cambios en el archivo "Mis Pokemons"
    grabaTxt(misPokemonsTxt, misPokemons)
    
def validarPorcentaje(porcentaje):
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
    url = "https://pokeapi.co/api/v2/pokemon"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return datos["count"]