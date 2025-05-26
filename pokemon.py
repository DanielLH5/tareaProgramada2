"""
python -m pip install requests
"""
import tkinter as tk
import requests
import random 
from archivos import * 

"""
def openSearch():
    button1.config(state="active")
    print("Hola Daniel!")
"""
"""
def obtenerPokemons(inicio):
    pokemons = leeTxt(misPokemonsTxt) #suponemos que es un str
    listaPokemons = pokemons.split("\n")
    matriz = []
    for i in range(inicio, inicio + 25, 5):
        print(f"i = {i}")
        fila = listaPokemons[i: i+5]
        matriz.append(fila)
    print(matriz)
    #print(listaPokemons[inicio:limite]) 
    return (matriz)


def botonesFlecha(ventana, contador, framePokemons):
    #cursor = contador
    #print(contador)
    print(f"Este es el cont: {contador}")
    for componente in framePokemons.winfo_children():
        componente.destroy()
    listaActual = obtenerPokemons(contador)
    for pokemon in listaActual:
        label = tk.Label(framePokemons, text=pokemon, padx=10, pady=10)
        label.pack()

def siguiente(ventana, framePokemons):
    print(f"S.Este es el cursor inicial: {contador}")
    global contador
    contador += 25
    print(f"S.Este es el cursor nuevo: {contador}")
    botonesFlecha(ventana, contador, framePokemons)
        
def anteriror(ventana, framePokemons):
    print(f"A.Este es el cursor inicial: {contador}")
    global contador
    contador -= 25
    print(f"A.Este es el cursor nuevo: {contador}")
    botonesFlecha(ventana, contador, framePokemons)

def ventanaPokedex():
    root = tk.Toplevel()
    root.geometry("250x400")
    root.title("Pokédex")
    title = tk.Label(root, text="Pokédex", padx=10, pady=10)
    # Contenedor para los labels de los pokemons
    framePokemons = tk.Frame(root)
    framePokemons.pack()

    # Inicializa el cursor como variable local de ventanaPokedex
    #contador = 0
    print(f"esta es ventana {contador}")
    botonesFlecha(root, contador, framePokemons)
    botonSiguiente = tk.Button(root, text="->", command=lambda:siguiente(root, framePokemons))
    botonSiguiente.pack(pady=10)
    botonAnterior = tk.Button(root, text="<-", command=lambda:anteriror(root, framePokemons))
    botonAnterior.pack(pady=10)
"""

def buscarExistenciaPokemon(listaPokemones, pokemon):
    if pokemon in listaPokemones:
        return True
    return False

def obtenerIdAtrapados(listaAtrapados):
    idAtrapados = []
    for pokemon in listaAtrapados:
        infoPokemonSeparado = pokemon.split("^")
        idAtrapados.append(infoPokemonSeparado[0])
    print(idAtrapados)

def atraparPokemons(porcentaje):
    pokemones = leeTxt(misPokemonsTxt)
    listaPokemones = pokemones.split("\n")[:-1]
    atrapados = int(len(listaPokemones) / 100) * int(porcentaje)
    listaAtrapados = random.sample(listaPokemones, atrapados)
    print(listaAtrapados)
    print(len(listaAtrapados))
    misPokemones = ""
    for i in range(len(listaPokemones)):
        pokemon = listaPokemones[i]
        encontrado = buscarExistenciaPokemon(listaAtrapados, pokemon)
        if encontrado:
            misPokemones += f"{pokemon}^a\n"
        else:
            misPokemones += f"{pokemon}^h\n"
    grabaTxt(misPokemonsTxt, misPokemones)
    idAtrapados = obtenerIdAtrapados(listaAtrapados)
    
def validarPorcentaje(porcentaje):
    try:
        if int(porcentaje) < 0 or int(porcentaje) > 100:
            mensaje = "El porcentaje debe de ser entre 0 y 100." #Manejar solo enteros.
            return ventanaRetroalimentacion(mensaje)
        else:
            return atraparPokemons(porcentaje)
    except ValueError:
        mensaje = "El valor tiene que ser un número entero."
        return ventanaRetroalimentacion(mensaje)

def ventanaAtrapar():
    ventana = tk.Toplevel()
    ventana.title("Atrapar Pokémons")
    ventana.geometry("500x200")

    global porcentaje #Hace que todas las demás funciones también la pueda usar
    porcentaje = tk.StringVar()
    
    contenedorPorcentaje = tk.Frame(ventana, pady=15, padx=5)
    contenedorPorcentaje.pack()
    etiquetaPorcentaje = tk.Label(contenedorPorcentaje, text = "Porcentaje: ")
    etiquetaPorcentaje.grid(row=0,column=0)
    entradaPorcentaje = tk.Entry(contenedorPorcentaje, width=30, textvariable=porcentaje)
    entradaPorcentaje.grid(row=0,column=1)

    contenedorBotones = tk.Frame(ventana, pady=15, padx=5)
    contenedorBotones.pack()

    botonAtrapar = tk.Button(contenedorBotones, text="Atrapar", width=30, command=lambda: validarPorcentaje(porcentaje.get()))
    botonAtrapar.grid(row=0, column=0, pady=5)
    botonLimpiar = tk.Button(contenedorBotones, text="Limpiar", width=30, command=lambda: validarEntradaBuscar(porcentaje.get()))
    botonLimpiar.grid(row=0, column=1, pady=5)

    ventana.mainloop()

def validarBotones():
    if leeTxt(misPokemonsTxt) == False: 
        button2.config(state="disabled")
        button3.config(state="disabled")
        button4.config(state="disabled")
        button5.config(state="disabled")
        button6.config(state="disabled")
        button7.config(state="disabled")
        button8.config(state="disabled")
        button9.config(state="disabled")
        button10.config(state="disabled")
        button11.config(state="disabled")
        button12.config(state="disabled")
    else:
        button2.config(state="active")
        button3.config(state="active")
        button4.config(state="active")
        button5.config(state="active")
        button6.config(state="active")
        button7.config(state="active")
        button8.config(state="active")
        button9.config(state="active")
        button10.config(state="active")
        button11.config(state="active")
        button12.config(state="active")

def ventanaRetroalimentacion(mensaje):
    root = tk.Toplevel()
    root.geometry("250x100")
    root.title("Retroalimentación")

    title = tk.Label(root, text=mensaje, padx=10, pady=10)
    title.pack()
    
    boton = tk.Button(root, text="Aceptar", command=root.destroy)
    boton.pack(pady=10)

def validarEntradaBuscar(numero):
    try:
        if int(numero) >= 1:
            return buscarPokemon(numero)
        else:
            mensaje = "El número tiene que ser mayor a 0."
            return ventanaRetroalimentacion(mensaje)
    except ValueError:
        mensaje = "El valor tiene que ser un número entero."
        return ventanaRetroalimentacion(mensaje)

def buscarPokemon(cantidad):
    urlPokemon = "https://pokeapi.co/api/v2/pokemon"
    number.set("")
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
        validarBotones() #verifico si está el .txt para habilitar los otros botones
        #print(listaPokemones) #Para verificar la información a u guardar.
    else:
        print(f"Error: {response.status_code}")
    print(f"Se ha creado los {cantidad} pokémons")

def ventanaBuscar():
    search = tk.Toplevel()
    search.title("Búsqueda de Pokémons")
    search.geometry("500x200")

    global number #Hace que todas las demás funciones también la pueda usar
    number = tk.StringVar()
    cantidad = tk.Entry(search, width=30, textvariable=number)
    cantidad.pack()

    searchButton = tk.Button(search, text="Buscar", width=30, command=lambda: validarEntradaBuscar(number.get()))
    searchButton.pack()

    search.mainloop()

def close():
    root.quit()

def main():
    global root
    root = tk.Tk()
    root.geometry("500x300")
    root.title("Ventana Principal")

    title = tk.Label(root, text="Poképad")
    title.pack()

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()

    global button1
    button1 = tk.Button(frame, width=20, text="1. Búsqueda", command=ventanaBuscar)
    button1.grid(row=1, column=0)
    
    global button2
    button2 = tk.Button(frame, text="2. Atrapar", width=20, command=ventanaAtrapar)
    button2.grid(row=2, column=0)

    global button3
    button3 = tk.Button(frame, text="3. Pokédex", width=20) #command=#ventanaPokedex
    button3.grid(row=3, column=0)
    
    global button4
    button4 = tk.Button(frame, text="4. Detalle", width=20)
    button4.grid(row=4, column=0)
    
    global button5
    button5 = tk.Button(frame, text="5. Descarga", width=20)
    button5.grid(row=5, column=0)
    
    global button6
    button6 = tk.Button(frame, text="6. XML", width=20)
    button6.grid(row=6, column=0)
    
    global button7
    button7 = tk.Button(frame, text="7. HTML Desc", width=20)
    button7.grid(row=1, column=1)

    global button8
    button8 = tk.Button(frame, text="8. esShiny", width=20)
    button8.grid(row=2, column=1)

    global button9
    button9 = tk.Button(frame, text="9. Convertidor", width=20)
    button9.grid(row=3, column=1)

    global button10
    button10 = tk.Button(frame, text="10. Desconveritdor", width=20)
    button10.grid(row=4, column=1)
    
    global button11
    button11 = tk.Button(frame, text="11. Virus", width=20)
    button11.grid(row=5, column=1)
    
    global button12
    button12 = tk.Button(frame, text="12. Agregar", width=20)
    button12.grid(row=5, column=1)
    
    global button13
    button13 = tk.Button(frame, text="13. Créditos", width=20)
    button13.grid(row=5, column=1)
    
    global button14
    button14 = tk.Button(frame, text="14. Salir", width=20, command=close)
    button14.grid(row=6, column=1)
    
    validarBotones()
    root.mainloop()

main()