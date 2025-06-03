"""
python -m pip install requests
"""
import tkinter as tk
from tkinter import PhotoImage
import urllib.request
from io import BytesIO
from PIL import Image, ImageTk
import requests
import random 
import csv
import re
from archivos import * 

##################################################
# Ventanas Secundarias
##################################################
def ventanaRetroalimentacion(mensaje):
    root = tk.Toplevel()
    root.geometry("300x100")
    root.title("Retroalimentación")
    title = tk.Label(root, text=mensaje, padx=10, pady=10)
    title.pack()
    boton = tk.Button(root, text="Aceptar", command=root.destroy)
    boton.pack(pady=10)

def ventanaConfirmacion(mensaje):
    root = tk.Toplevel()
    root.geometry("300x100")
    root.title("Confirmación")
    title = tk.Label(root, text=mensaje, padx=10, pady=10)
    title.pack()
    boton = tk.Button(root, text="Aceptar", command=root.destroy)
    boton.pack(pady=10)
    
def ventanaAprobacion(comandoAceptar):
    root = tk.Toplevel()
    root.geometry("250x150")
    root.title("Aprobación")
    title = tk.Label(root, text="¿Deseas realizar esta acción?", padx=10, pady=10)
    title.pack()
    botonAceptar = tk.Button(root, text="Aceptar", command=lambda: [comandoAceptar(), root.destroy()])
    botonAceptar.pack(pady=5)
    botonRechazar = tk.Button(root, text="Rechazar", command=root.destroy)
    botonRechazar.pack(pady=5)

##################################################
# 14. Salir
##################################################

def close():
    diccGlobal["root"].quit()

##################################################
# 13. Créditos
##################################################

def ventanaCreditos():
    from tkinter import font
    creditos = tk.Toplevel()
    creditos.title("Créditos")
    creditos.geometry("250x100")
    fuenteSuave = font.Font(family="Segoe UI", size=10)
    texto = tk.Label(creditos,font=fuenteSuave, text = "Hecho por:\n\nDaniel Liao Huang\nEthan Hernández Cubillo")
    texto.pack(side= tk.TOP)

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
                txtPokemonsActualizado += nuevoPokemon + "\n"
            else:
                txtPokemonsActualizado += pokemon + "\n"
        print(txtPokemonsActualizado)
            
def atraparPokemonID(id, pokemonsA):
    urlID = f"https://pokeapi.co/api/v2/pokemon/{id}/"
    respuesta = requests.get(urlID) #200 si está ok, 400 si tiene un error, 500 si no se encuentra
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
        pokemonsA[int(id)] = [info['name'],
                                         (validarShiny(info), obtenerPeso(info['weight']), obtenerAltura(info['height'])), # (esShiny, peso, altura)
                                         [totalStats, (salud, ataque, defensa, ataqueEspecial, defensaEspecial, velocidad)], # [totalEstad, (PS, A, D, AE, DE, V)]
                                         (obtenerTipo(info, 0), obtenerTipo(info, 1)), # (listaDeTipos, listaDeTipos)
                                          obtenerImagen(info) # url
                                        ]
        graba(misPokemonsAtrapadosPkl, pokemonsA)
        diccionarioActualizado = lee(misPokemonsAtrapadosPkl)
        #print(diccionarioActualizado) # Borrar luego -----------------
        nombre = info['name']
        agregarPokemonIDTxt(id, nombre)
        mensaje = f"Se ha guardado el pokemon {id} en el diccionario."
        ventanaConfirmacion(mensaje)
    else:
        print(f"Error: {respuesta.status_code}")
    print(f"Se ha agregado el id: {id}.")

def obtenerIDBuscados(txtPokemons):
    listaID = []
    listaPokemons = txtPokemons.split("\n")[:-1]
    for pokemon in listaPokemons:
        infoPokemon = pokemon.split("^")
        listaID.append(infoPokemon[0])
    print(listaID)
    return listaID

def validarAtraparPokemon(id):
    limite = obtenerLimitePokemon()
    pokemonsA = lee(misPokemonsAtrapadosPkl)
    try:
        if int(id) <= 0:
            mensaje = "El valor tiene que ser un número mayor a 0."
            return ventanaRetroalimentacion(mensaje)
        elif int(id) in pokemonsA:
            mensaje = "El ID ya se encontraba en el diccionario."
            return ventanaRetroalimentacion(mensaje)
        elif int(id) > limite:
            mensaje = "Excediste el límite de pokémons dentro del API."
            return ventanaRetroalimentacion(mensaje)
        else:
            return atraparPokemonID(id, pokemonsA)
    except ValueError:
        mensaje = "El valor tiene que ser un número entero."
        return ventanaRetroalimentacion(mensaje)

def ventanaAgregarPokemon():
    agregar = tk.Toplevel()
    agregar.title("Agregar Pokémon")
    agregar.geometry("500x200")
    etiquetaBuscar = tk.Label(agregar, text = "Ingrese el ID que quieras buscar:")
    etiquetaBuscar.pack(pady=20)
    contenedorAtrapar = tk.Frame(agregar, pady=15, padx=5)
    contenedorAtrapar.pack(pady=10, padx=10)
    id = tk.Entry(contenedorAtrapar, width=20)
    id.grid(row=0,column=0)
    botonBuscar = tk.Button(contenedorAtrapar, text="Agregar", width=30, command=lambda: validarAtraparPokemon(id.get()))
    botonBuscar.grid(row=0,column=1)
    agregar.mainloop()

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

def actualizarStatsVirus(cambio, porcentaje):
    pokemonBD = lee(misPokemonsAtrapadosPkl)
    #print(cambio, porcentaje)
    diccPokemonVirus = {}
    for clave, info in pokemonBD.items():
        infoPokemon = []
        infoPokemon.append(info[0])
        infoPokemon.append(info[1])
        estadisticas = info[2]
        apartadoEstadistica = manipularEstadisticas(cambio, porcentaje, estadisticas)
        infoPokemon.append(apartadoEstadistica)
        infoPokemon.append(info[3])
        infoPokemon.append(info[4])
        diccPokemonVirus[clave] = infoPokemon
    def guardarDicc():
        graba(misPokemonsAtrapadosPkl, diccPokemonVirus)  # Guardar el diccionario
        mensaje = "Los cambios han sido guardados"
        ventanaConfirmacion(mensaje)
        print(diccPokemonVirus)
    ventanaAprobacion(guardarDicc)

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

def verificarPorcentajeVirus(cambio, porcentaje):
    porcentajeValido = validarPorcentajeVirus(cambio, porcentaje)
    if porcentajeValido[0] == True:
        return actualizarStatsVirus(cambio, porcentaje)
    else:
        mensaje = porcentajeValido[1] # Obtener el mensaje de error
        return ventanaRetroalimentacion(mensaje)

def ventanaVirus():
    virus = tk.Toplevel()
    virus.title("Virus")
    virus.geometry("250x180")
    opcion = tk.StringVar(value="disminuir")
    tk.Radiobutton(virus, text="Aumentar", variable=opcion, value=0).pack(anchor="w", padx=10, pady=5)
    tk.Radiobutton(virus, text="Disminuir", variable=opcion, value=1).pack(anchor="w", padx=10)
    contenedor = tk.Frame(virus)
    contenedor.pack(pady=10, padx=10, fill="x")
    etiquetaPorcentaje = tk.Label(contenedor, text="Porcentaje:")
    etiquetaPorcentaje.pack(side="left")
    entrada = tk.Entry(contenedor)
    entrada.pack(side="left", fill="x", expand=True)
    botonAccion = tk.Button(virus, text="Accionar virus", width=30, command=lambda: verificarPorcentajeVirus(opcion.get(), entrada.get()))
    botonAccion.pack(pady=10, padx=10, fill="x")

##################################################
# 10. Desconvertidor
##################################################

def matrizADicc():
    matrizPokemon = lee(matrizPokemonAD)
    diccPokemon = {}
    for pokemon in matrizPokemon:
        clave = pokemon[0]
        infoPokemon = []
        infoPokemon.append(pokemon[1])
        infoPokemon.append(tuple(pokemon[2]))
        estadisticas = pokemon[3]
        apartadoEstadistica = []
        apartadoEstadistica.append(estadisticas[0])
        apartadoEstadistica.append(tuple(estadisticas[1]))
        infoPokemon.append(apartadoEstadistica)
        infoPokemon.append(tuple(pokemon[4]))
        infoPokemon.append(pokemon[5])
        diccPokemon[clave] = infoPokemon
    
    def guardarDicc():
        graba(diccPokemonAM, diccPokemon)  # Guardar el diccionario
        mensaje = "Los cambios han sido guardados"
        ventanaConfirmacion(mensaje)
        print(diccPokemon)
        # Aquí puedes reactivar botones u otras acciones
    ventanaAprobacion(guardarDicc)
    #Volver a activar todos los botones que requerían de dicc

##################################################
# 9. Convertidor
##################################################

def diccAMatriz():
    diccPokemon = lee(misPokemonsAtrapadosPkl)
    matrizPokemons = []
    for clave, valor in diccPokemon.items():
        matrizPokemon = []
        matrizPokemon.append(clave)
        matrizPokemon.append(valor[0])
        matrizPokemon.append(list(valor[1]))
        estadisticas = valor[2]
        apartadoEstadistica = []
        apartadoEstadistica.append(estadisticas[0])
        apartadoEstadistica.append(list(estadisticas[1]))
        matrizPokemon.append(apartadoEstadistica)
        matrizPokemon.append(list(valor[3]))
        matrizPokemon.append(valor[4])
        matrizPokemons.append(matrizPokemon)
        
    def guardarMatriz():
        graba(matrizPokemonAD, matrizPokemons)  # Guardar el diccionario
        mensaje = "Los cambios han sido guardados"
        ventanaConfirmacion(mensaje)
        print(matrizPokemons)
        # Aquí puedes reactivar botones u otras acciones
    ventanaAprobacion(guardarMatriz)
    #Deshabilitar los botones que requieran del diccionario

##################################################
# 8. esShiny
##################################################

def obtenerLimiteShiny(infoAtrapados):
    limite = 100
    if len(infoAtrapados) < 100:
        limite = len(infoAtrapados)
    return limite

def obtenerIdShiny(infoAtrapados):
    listaIdShiny = []
    contador = 0
    limite = obtenerLimiteShiny(infoAtrapados)
    for clave, valor in infoAtrapados.items():
        linkShiny = valor[4]
        if contador == limite:
            return listaIdShiny
        if linkShiny != "":
            listaIdShiny.append(clave)
        contador += 1
    return listaIdShiny

def crarArchivoShiny():
    infoAtrapados = lee(misPokemonsAtrapadosPkl)
    #print(infoAtrapados) # Borrar luego ---------------
    listaId = obtenerIdShiny(infoAtrapados)
    def crearHTMLShiny():
        with open("esShiny.html", "w", encoding="utf-8") as archivo:
            archivo.write("""<!DOCTYPE html>
<html lang="es">
<head>
    <title>esShiny</title>
    <meta charset="uft-8">
</head>
<body>
    <table>
        <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Peso</th>
            <th>Altura</th>
            <th>Total Estadísticas</th>
            <th>Estadísticas</th>
            <th>Tipos</th>
            <th>Imagen</th>
        </tr>""")
            for id in listaId:
                archivo.write(f"""
    <tr>
        <td>{id}</td>
        <td>{infoAtrapados.get(id)[0]}</td>
        <td>{infoAtrapados.get(id)[1][1]}</td>
        <td>{infoAtrapados.get(id)[1][2]}</td>
        <td>{infoAtrapados.get(id)[2][0]}</td>
        <td>{infoAtrapados.get(id)[2][1]}</td>
        <td>{infoAtrapados.get(id)[3]}</td>
        <td><img src={infoAtrapados.get(id)[4]}></td>
    </tr>""")
            archivo.write("""
    </table>
</body>
</html>
        """)
        mensaje = "Se ha creado el HTML de shinys exitosamente"
        ventanaConfirmacion(mensaje)
    ventanaAprobacion(crearHTMLShiny)

##################################################
# 7. HTML escapados.
##################################################leeTxtLineas

def generarHtmlDesdeXml():
    archivoXml = "pokemons.xml"
    with open(archivoXml, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    baseNombreHtml = "huyeron"
    porPagina = 100
    pokemons = []
    idP = None
    nombre = None
    total = None
    for linea in lineas:
        linea = linea.strip()
        if linea.startswith('<Pokemon') and 'id="' in linea:
            try:
                idP = int(linea.split('id="')[1].split('"')[0])
            except (IndexError, ValueError):
                continue
        elif linea.startswith('<nombre>'):
            nombre = linea.replace('<nombre>', '').replace('</nombre>', '').strip()
        elif linea.startswith('<totalEstad>'):
            try:
                total = int(linea.replace('<totalEstad>', '').replace('</totalEstad>', '').strip())
                if idP is not None and nombre is not None:
                    pokemons.append((idP, nombre, total))
            except ValueError:
                continue
    pokemons.sort(key=lambda x: x[2], reverse=True)
    totalPokemons = len(pokemons)
    paginas = (totalPokemons // porPagina) + (1 if totalPokemons % porPagina != 0 else 0)
    contador = 1
    for pagina in range(paginas):
        nombreArchivo = f"{baseNombreHtml}{pagina + 1}.html"
        with open(nombreArchivo, 'w', encoding='utf-8') as archivo:
            archivo.write("""<html lang="es">
<head><title>Pokémons Huyeron</title><meta charset="utf-8"></head>
<body>
<table border="1">
<tr><th>#</th><th>ID</th><th>Nombre</th><th>Total Estadísticas</th></tr>
""")
            inicio = pagina * porPagina
            fin = min(inicio + porPagina, totalPokemons)
            for i in range(inicio, fin):
                idP, nombre, total = pokemons[i]
                archivo.write(f"<tr><td>{contador}</td><td>{idP}</td><td>{nombre}</td><td>{total}</td></tr>\n")
                contador += 1
            archivo.write("</table>\n</body>\n</html>")
        print(f"Archivo HTML generado: {nombreArchivo}")

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

def generarXml():
    lineasPokemons = leeTxtLineas(misPokemonsTxt)
    pokemonsXml = "pokemons.xml"
    pokemonsHuyeron = []  #Lista nueva para guardar solo los que huyeron
    for linea in lineasPokemons:
        linea = linea.strip()
        if not linea:
            continue
        partes = linea.split('^')
        if len(partes) != 3:
            continue
        idStr, nombre, estado = partes
        if estado == 'h':  #Solo los que huyeron
            try:
                idPokemon = int(idStr)
                totalEstadisticas = obtenerEstadisticas(nombre)
                pokemonsHuyeron.append((idPokemon, nombre, totalEstadisticas))
            except ValueError:
                pass  #Ignorar si no es número
    lineasXml = ['<Pokemons>']
    for idP, nombre, total in pokemonsHuyeron:
        lineasXml.append(f'  <Pokemon id="{idP}">')
        lineasXml.append(f'    <nombre>{nombre}</nombre>')
        lineasXml.append(f'    <totalEstad>{total}</totalEstad>')
        lineasXml.append(f'  </Pokemon>')
    lineasXml.append('</Pokemons>')
    with open(pokemonsXml, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineasXml))
    print(f"Archivo XML generado: {pokemonsXml}")
    
##################################################
# 5. Descarga
##################################################

def obtenerCsv(matrizPokemons):
    try:
        f=open(excelPokemons,"w")
        escritor = csv.writer(f, delimiter=",") #; si el asistente lo quiere ver en diferentes casillas
        escritor.writerows(matrizPokemons)
        f.close()
    except Exception as e:
        print(f"Error al crear el archivo: {e}")

def crearMatrizPokemons():
    pokemons = leeTxt(misPokemonsTxt)
    listaPokemons = pokemons.split(f"\n")
    listaPokemons.pop() #Eliminamos el último "\n"
    matrizPokemons = [["ID","Nombre","Estado"]]
    for infoPokemon in listaPokemons:
        listaInfo = infoPokemon.split("^")
        if listaInfo[2] == "a":
            listaInfo[2] = "atrapado"
        else:
            listaInfo[2] = "huyó"
        matrizPokemons.append(listaInfo)
    
    def guardarCsv():
        obtenerCsv(matrizPokemons)
        mensaje = "Se ha creado el archivo .csv"
        ventanaConfirmacion(mensaje)
    ventanaAprobacion(guardarCsv)

##################################################
# 4. Detalle
##################################################

def mostrarDetalles(clave, nombre, shiny, peso, altura, tipos, stats):
    popup = tk.Toplevel()
    popup.geometry("300x380") 
    popup.title(f"{nombre.capitalize()} - Detalles")
    url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{clave}.png"
    if shiny:
        url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{clave}.png"
    try:
        with urllib.request.urlopen(url) as u:
            rawData = u.read()
        imagen = Image.open(BytesIO(rawData)).resize((96, 96))
        foto = ImageTk.PhotoImage(imagen)
        labelImg = tk.Label(popup, image=foto)
        labelImg.image = foto
        labelImg.pack()
    except:
        tk.Label(popup, text="(No se pudo cargar la imagen)").pack()
    tk.Label(popup, text=f"Nombre: {nombre}").pack()
    tk.Label(popup, text=f"Peso: {peso}").pack()
    tk.Label(popup, text=f"Altura: {altura}").pack()
    if tipos:
        tiposStr = ", ".join(tipos)
        tk.Label(popup, text=f"Tipos: {tiposStr}").pack()
    nombresStats = ["HP", "Ataque", "Defensa", "Ataque Esp", "Defensa Esp", "Velocidad"]
    for i in range(len(stats)):
        tk.Label(popup, text=f"{nombresStats[i]}: {stats[i]}").pack()
    tk.Button(popup, text="Cerrar", command=popup.destroy).pack(pady=10)

##################################################
# Pokédex Reto 3
##################################################
def mostrarPagina(ventana, frame, pokemons, pagina):
    for widget in frame.winfo_children():
        widget.destroy()
    claves = sorted(pokemons.keys())
    inicio = pagina * 25
    fin = inicio + 25
    subset = claves[inicio:fin]
    fila, columna = 0, 0
    for clave in subset:
        nombre = pokemons[clave][0]
        shiny = pokemons[clave][1][0]
        peso = pokemons[clave][1][1]
        altura = pokemons[clave][1][2]
        stats = pokemons[clave][2][1]  # lista de 6 stats
        tipos = pokemons[clave][3]     # tupla con tipos
        url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{clave}.png"
        if shiny:
            url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{clave}.png"
        try:
            with urllib.request.urlopen(url) as u:
                rawData = u.read()
            imagen = Image.open(BytesIO(rawData)).resize((64, 64))
            foto = ImageTk.PhotoImage(imagen)
        except:
            foto = None
        framePoke = tk.Frame(frame)
        framePoke.grid(row=fila, column=columna, padx=10, pady=10)
        if foto:
            labelImagen = tk.Label(framePoke, image=foto)
            labelImagen.image = foto  #Mantener referencia
            labelImagen.pack()
            labelImagen.bind(
                "<Button-1>",
                lambda e, c=clave, n=nombre, s=shiny, p=peso, a=altura, t=tipos, st=stats:
                mostrarDetalles(c, n, s, p, a, t, st)
            )
        tk.Label(framePoke, text=nombre).pack()
        columna += 1
        if columna == 5:
            columna = 0
            fila += 1          

def avanzar(ventana, frame, pokemons, paginaActualVar):
    totalPaginas = (len(pokemons) - 1) // 25
    if paginaActualVar.get() < totalPaginas:
        paginaActualVar.set(paginaActualVar.get() + 1)
        mostrarPagina(ventana, frame, pokemons, paginaActualVar.get())

def retroceder(ventana, frame, pokemons, paginaActualVar):
    if paginaActualVar.get() > 0:
        paginaActualVar.set(paginaActualVar.get() - 1)
        mostrarPagina(ventana, frame, pokemons, paginaActualVar.get())

def ventanaPokedex():
    pokemonsLista = lee(misPokemonsAtrapadosPkl)
    ventana = tk.Toplevel()
    ventana.title("Pokédex")
    frame = tk.Frame(ventana)
    frame.pack()
    paginaActualVar = tk.IntVar(value=0)
    controles = tk.Frame(ventana)
    controles.pack()
    tk.Button(controles, text="<<", command=lambda: retroceder(ventana, frame, pokemonsLista, paginaActualVar)).pack(side=tk.LEFT, padx=10)
    tk.Button(controles, text=">>", command=lambda: avanzar(ventana, frame, pokemonsLista, paginaActualVar)).pack(side=tk.RIGHT, padx=10)
    mostrarPagina(ventana, frame, pokemonsLista, paginaActualVar.get())

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

def atraparPokemons(porcentaje):
    archivoPokemons = leeTxt(misPokemonsTxt)
    listaPokemons = archivoPokemons.split("\n")[:-1] # Omitir el último salto de linea
    print(listaPokemons) # Luego borrarlo ----------------
    # Obtener la cantidad de Pokemons atrapados, según el porcentaje
    cantidadPokemonsAtrapados = int(len(listaPokemons) * (int(porcentaje) / 100))
    if cantidadPokemonsAtrapados == 0 and int(porcentaje) > 0: #Arreglado, antes no permitía si eran menos de 100
        cantidadPokemonsAtrapados = 1
    # Obtener las muestras de manera aleatoria, pasando la lista de Pokemons y la cantidad de Pokemons atrapados
    listaRandomAtrapados = random.sample(listaPokemons, cantidadPokemonsAtrapados)
    print(listaRandomAtrapados) # Borrar luego -----------------
    actualizarPokemonsTxt(listaPokemons, listaRandomAtrapados) # Actualizar el archivo "Mis Pokemons"
    obtenerIdAtrapados(listaRandomAtrapados)
    obtenerPokemonsAtrapados(listaRandomAtrapados) # Actualizar el archivo "Mis Pokemons"
    mensaje = "Pokemons atrapados exitosamente."
    ventanaConfirmacion(mensaje)
    
def validarPorcentaje(porcentaje):
    try:
        if int(porcentaje) < 0 or int(porcentaje) > 100:
            return (False, "El porcentaje debe de ser entre 0 y 100.")
        else:
            return (True, "")
    except ValueError:
        return (False, "El valor tiene que ser un número entero.")

def calcularPorcentaje(porcentaje):
    porcentajeValido = validarPorcentaje(porcentaje)
    if porcentajeValido[0] == True:
        return atraparPokemons(porcentaje)
    else:
        mensaje = porcentajeValido[1] # Obtener el mensaje de error
        return ventanaRetroalimentacion(mensaje)

def limpiarEntradaPorcentaje():
    diccGlobal["porcentaje"].set("")

def ventanaAtrapar():
    ventana = tk.Toplevel()
    ventana.title("Atrapar Pokémons")
    ventana.geometry("500x200")
    diccGlobal["porcentaje"] = tk.StringVar()
    contenedorPorcentaje = tk.Frame(ventana, pady=15, padx=5)
    contenedorPorcentaje.pack()
    etiquetaPorcentaje = tk.Label(contenedorPorcentaje, text = "Porcentaje: ")
    etiquetaPorcentaje.grid(row=0,column=0)
    entradaPorcentaje = tk.Entry(contenedorPorcentaje, width=30, textvariable=diccGlobal["porcentaje"])
    entradaPorcentaje.grid(row=0,column=1)
    contenedorBotones = tk.Frame(ventana, pady=15, padx=5)
    contenedorBotones.pack()
    botonAtrapar = tk.Button(contenedorBotones, text="Atrapar", width=30, command=lambda: calcularPorcentaje(diccGlobal["porcentaje"].get()))
    botonAtrapar.grid(row=0, column=0, pady=5)
    botonLimpiar = tk.Button(contenedorBotones, text="Limpiar", width=30, command=limpiarEntradaPorcentaje)
    botonLimpiar.grid(row=0, column=1, pady=5)
    ventana.mainloop()

##################################################
# 1. Buscar
##################################################

def obtenerLimitePokemon():
    url = "https://pokeapi.co/api/v2/pokemon"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return datos["count"]

def buscarPokemon(cantidad):
    urlPokemon = "https://pokeapi.co/api/v2/pokemon"
    diccGlobal["numero"].set("")
    url = "https://pokeapi.co/api/v2/pokemon"
    params = {
        "limit": cantidad,
        "offset": 0
    }
    response = requests.get(url, params) #200 si está ok, 400 si tiene un error, 500 si no se encuentra
    strPokemones = ""
    if response.ok:
        data = response.json()
        for pokemon in data['results']: #results es el key del json del API pokemon que contiene nome y url de cada pokemon.
            name = pokemon['name']
            url = pokemon['url']
            id = url.replace(urlPokemon,"").replace("/", "") #De esta forma no se tiene que acceder al link, más eficiente.
            print(f"nombre: {name}")
            print(f"url: {url}")
            strPokemones += f"{id}^{name}\n"
        grabaTxt(misPokemonsTxt, strPokemones) #.txt solo admite str
        mensaje = "Se ha creado la Base de Datos de pokémons"
        ventanaConfirmacion(mensaje)
        validarBotones() #verifico si está el .txt para habilitar los otros botones
        #print(listaPokemones) #Para verificar la información a u guardar.
    else:
        print(f"Error: {response.status_code}")
    print(f"Se ha creado los {cantidad} pokémons")

def validarEntradaBuscar(numero):
    try:
        if int(numero) < 1:
            mensaje = "El número tiene que ser mayor a 0."
            return ventanaRetroalimentacion(mensaje)
        elif int(numero) > obtenerLimitePokemon():
            mensaje = "Excediste el límite de pokémons dentro del API."
            return ventanaRetroalimentacion(mensaje)
        else:
            return buscarPokemon(numero)
    except ValueError:
        mensaje = "El valor tiene que ser un número entero."
        return ventanaRetroalimentacion(mensaje)

def ventanaBuscar():
    search = tk.Toplevel()
    search.title("Búsqueda de Pokémons")
    search.geometry("500x200")
    diccGlobal["numero"] = tk.StringVar()
    cantidad = tk.Entry(search, width=30, textvariable=diccGlobal["numero"])
    cantidad.pack()
    searchButton = tk.Button(search, text="Buscar", width=30, command=lambda: validarEntradaBuscar(diccGlobal["numero"].get()))
    searchButton.pack()
    search.mainloop()

##################################################
# Ventana Principal
##################################################

def validarBotones():
    if not leeTxt(misPokemonsTxt):
        for i in range(2, 13):  #Botones del 2 al 12
            diccGlobal["botones"][f"boton{i}"].config(state="disabled")
    else:
        for i in range(2, 13):
            if i != 4:
                diccGlobal["botones"][f"boton{i}"].config(state="active")

def main():
    #global root
    root = tk.Tk()
    root.geometry("500x300")
    root.title("Ventana Principal")
    diccGlobal["root"] = root
    title = tk.Label(root, text="Poképad")
    title.pack()
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()

    diccGlobal["botones"]["boton1"] = tk.Button(frame, width=20, text="1. Búsqueda", command=ventanaBuscar)
    diccGlobal["botones"]["boton1"].grid(row=1, column=0)    
    diccGlobal["botones"]["boton2"] = tk.Button(frame, text="2. Atrapar", width=20, command=ventanaAtrapar)
    diccGlobal["botones"]["boton2"].grid(row=2, column=0)
    diccGlobal["botones"]["boton3"] = tk.Button(frame, text="3. Pokédex", width=20, command=ventanaPokedex)
    diccGlobal["botones"]["boton3"].grid(row=3, column=0) 
    diccGlobal["botones"]["boton4"] = tk.Button(frame, text="4. Detalle", width=20, state="disabled") #nunca se va a usar
    diccGlobal["botones"]["boton4"].grid(row=4, column=0)
    diccGlobal["botones"]["boton5"] = tk.Button(frame, text="5. Descarga", width=20, command=crearMatrizPokemons)
    diccGlobal["botones"]["boton5"].grid(row=5, column=0)
    diccGlobal["botones"]["boton6"] = tk.Button(frame, text="6. XML", width=20, command=generarXml)
    diccGlobal["botones"]["boton6"].grid(row=6, column=0)
    diccGlobal["botones"]["boton7"] = tk.Button(frame, text="7. HTML Desc", width=20, command=generarHtmlDesdeXml)
    diccGlobal["botones"]["boton7"].grid(row=7, column=0)
    diccGlobal["botones"]["boton8"] = tk.Button(frame, text="8. esShiny", width=20, command=crarArchivoShiny)
    diccGlobal["botones"]["boton8"].grid(row=1, column=1)
    diccGlobal["botones"]["boton9"] = tk.Button(frame, text="9. Convertidor", width=20, command=diccAMatriz)
    diccGlobal["botones"]["boton9"].grid(row=2, column=1)
    diccGlobal["botones"]["boton10"] = tk.Button(frame, text="10. Desconvertidor", width=20, command=matrizADicc)
    diccGlobal["botones"]["boton10"].grid(row=3, column=1)
    diccGlobal["botones"]["boton11"] = tk.Button(frame, text="11. Virus", width=20, command=ventanaVirus)
    diccGlobal["botones"]["boton11"].grid(row=4, column=1)
    diccGlobal["botones"]["boton12"] = tk.Button(frame, text="12. Agregar", width=20, command=ventanaAgregarPokemon)
    diccGlobal["botones"]["boton12"].grid(row=5, column=1)
    diccGlobal["botones"]["boton13"] = tk.Button(frame, text="13. Créditos", width=20, command=ventanaCreditos)
    diccGlobal["botones"]["boton13"].grid(row=6, column=1)
    diccGlobal["botones"]["boton14"] = tk.Button(frame, text="14. Salir", width=20, command=close)
    diccGlobal["botones"]["boton14"].grid(row=7, column=1) 
    validarBotones()
    root.mainloop()

diccGlobal = {
    "root": None,
    "botones": {}
}
main()