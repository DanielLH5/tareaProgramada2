###########################################################
#Elaborado por: Daniel Liao Huang y Ethan Hernández Cubillo
#Fecha de Realización: 16/05/2025
#Última actualización: 04/06/2025
#Versión: 3.13.3
###########################################################

"""
python -m pip install requests
"""
import tkinter as tk
import requests
import random 
from tkinter import PhotoImage
import urllib.request
from io import BytesIO
from PIL import Image, ImageTk
from funciones import * 

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
        print(diccionarioActualizado) 
        nombre = info['name']
        agregarPokemonIDTxt(id, nombre)
        mensaje = f"Se ha guardado el pokemon {id} en el diccionario."
        ventanaConfirmacion(mensaje)
    else:
        print(f"Error: {respuesta.status_code}")
    print(f"Se ha agregado el id: {id}.")

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

def crarArchivoShiny():
    infoAtrapados = lee(misPokemonsAtrapadosPkl)
    matrizId = obtenerIdShiny(infoAtrapados)
    def crearHTMLShiny():
        for i, lista in enumerate(matrizId, start=1):
            with open(f"esShiny{i}.html", "w", encoding="utf-8") as archivo:
                archivo.write("""<!DOCTYPE html>
<html lang="es">
<head>
    <title>esShiny</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: sans-serif;
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            padding: 6px;
            text-align: center;
        }
        th {
            background-color: lightgray;
        }
        img {
            width: 80px;
            height: auto;
        }
    </style>
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
                for id in lista: #Cada bloque
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
##################################################
def generarHtmlDesdeXml():
    archivoXml = "pokemons.xml"
    with open(archivoXml, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    def aprobarGeneracionHtml():
        baseNombreHtml = "huyeron"
        porPagina = 100
        pokemons = []
        idPokemon = total = int
        nombre = str
        for linea in lineas:
            linea = linea.strip()
            if linea.startswith('<Pokemon'):
                if 'id="' in linea:
                    try:
                        idPokemon = int(linea.split('id="')[1].split('"')[0])
                    except (IndexError, ValueError):
                        continue
            elif linea.startswith('<nombre>'):
                nombre = linea.replace('<nombre>', '').replace('</nombre>', '').strip()
            elif linea.startswith('<totalEstad>'):
                try:
                    total = int(linea.replace('<totalEstad>', '').replace('</totalEstad>', '').strip())
                    if idPokemon != int:
                        if nombre != str:
                            pokemons.append((idPokemon, nombre, total))
                except ValueError:
                    continue
        pokemons.sort(key=lambda x: x[2], reverse=True)
        totalPokemons = len(pokemons)
        if totalPokemons % porPagina != 0: #Cuenta la cantidad de paginas que se deben crear según cantidad de pokémons.
            paginas = (totalPokemons // porPagina) + 1
        else:
            paginas = (totalPokemons // porPagina) + 0
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
                    idPokemon, nombre, total = pokemons[i]
                    archivo.write(f"<tr><td>{contador}</td><td>{idPokemon}</td><td>{nombre}</td><td>{total}</td></tr>\n")
                    contador += 1
                archivo.write("</table>\n</body>\n</html>")
        print(f"Archivo HTML generado: {nombreArchivo}")
        mensaje = "Se ha creado el HTML de pokemons huidos."
        ventanaConfirmacion(mensaje)
    ventanaAprobacion(aprobarGeneracionHtml)

##################################################
# 6. Xml
##################################################

def generarXml():
    lineasPokemons = leeTxtLineas(misPokemonsTxt)
    pokemonsXml = "pokemons.xml"
    pokemonsHuyeron = [] #Lista nueva para guardar solo los que huyeron
    def aprobacionXml():
        for linea in lineasPokemons:
            linea = linea.strip()
            if not linea: #En caso de haber línea vacía
                continue
            partes = linea.split('^') #Divide la información de los separadores
            if len(partes) != 3: #En caso de ser una linea con valores distintos
                continue
            idStr, nombre, estado = partes
            if estado == 'h':  #Solo los que huyeron
                try:
                    idPokemon = int(idStr)
                    totalEstadisticas = obtenerEstadisticas(nombre)
                    pokemonsHuyeron.append((idPokemon, nombre, totalEstadisticas))
                except ValueError:
                    pass #Ignora si no es número
        lineasXml = ['<Pokemons>'] #Escritura del XML
        for idPokemon, nombre, total in pokemonsHuyeron:
            lineasXml.append(f'  <Pokemon id="{idPokemon}">')
            lineasXml.append(f'    <nombre>{nombre}</nombre>')
            lineasXml.append(f'    <totalEstad>{total}</totalEstad>')
            lineasXml.append(f'  </Pokemon>')
        lineasXml.append('</Pokemons>')
        with open(pokemonsXml, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lineasXml))
        print(f"Archivo XML generado: {pokemonsXml}")
        mensaje = "Se ha creado el XML de pokemons huidos."
        ventanaConfirmacion(mensaje)
    ventanaAprobacion(aprobacionXml)
    
##################################################
# 5. Descarga
##################################################

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
    ventana = tk.Toplevel()
    ventana.geometry("300x380") 
    ventana.title(f"{nombre.capitalize()} - Detalles")
    url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{clave}.png"
    if shiny:
        url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{clave}.png"
    try:
        with urllib.request.urlopen(url) as u:
            imagenPokemon = u.read()
        imagen = Image.open(BytesIO(imagenPokemon)).resize((96, 96))
        foto = ImageTk.PhotoImage(imagen)
        labelImagen = tk.Label(ventana, image=foto)
        labelImagen.image = foto
        labelImagen.pack()
    except:
        tk.Label(ventana, text="(No se pudo cargar la imagen)").pack()
    tk.Label(ventana, text=f"Nombre: {nombre}").pack()
    tk.Label(ventana, text=f"Peso: {peso}").pack()
    tk.Label(ventana, text=f"Altura: {altura}").pack()
    if tipos:
        tiposStr = ", ".join(tipos)
        tk.Label(ventana, text=f"Tipos: {tiposStr}").pack()
    nombresStats = ["HP", "Ataque", "Defensa", "Ataque Esp", "Defensa Esp", "Velocidad"]
    for i in range(len(stats)):
        tk.Label(ventana, text=f"{nombresStats[i]}: {stats[i]}").pack()
    tk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

##################################################
# 3. Pokédex
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
        estadisticas = pokemons[clave][2][1] #Lista de 6 estadisticas
        tipos = pokemons[clave][3] #Tupla con tipos
        url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{clave}.png"
        if shiny:
            url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{clave}.png"
        try:
            with urllib.request.urlopen(url) as u:
                imagenPokemon = u.read()
            imagen = Image.open(BytesIO(imagenPokemon)).resize((64, 64))
            foto = ImageTk.PhotoImage(imagen)
        except:
            foto = None
        framePoke = tk.Frame(frame)
        framePoke.grid(row=fila, column=columna, padx=10, pady=10)
        if foto:
            labelImagen = tk.Label(framePoke, image=foto)
            labelImagen.image = foto #Mantener referencia
            labelImagen.pack()
            labelImagen.bind(
                "<Button-1>",
                lambda e, c=clave, n=nombre, s=shiny, p=peso, a=altura, t=tipos, est=estadisticas: 
                mostrarDetalles(c, n, s, p, a, t, est)) #Se actualizan los valores y se envían para mostrar
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

def atraparPokemons(porcentaje): #Se queda
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

def calcularPorcentaje(porcentaje): #Se queda
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