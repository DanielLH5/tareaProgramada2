"""
python -m pip install requests
"""
import tkinter as tk
import requests 
from archivos import * 

def openSearch():
    button1.config(state="active")
    print("Hola Daniel!")

def ventanaRetroalimentacion(mensaje):
    root = tk.Tk()
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
        grabaTxt("Mis pokémons.txt", strPokemones) #.txt solo admite str
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

    button2 = tk.Button(frame, text="2. Atrapar", width=20)
    button2.grid(row=2, column=0)
    
    button3 = tk.Button(frame, text="3. Pokédex", width=20)
    button3.grid(row=3, column=0)
    
    button4 = tk.Button(frame, text="4. Detalle", width=20)
    button4.grid(row=4, column=0)
    
    button5 = tk.Button(frame, text="5. Descarga", width=20)
    button5.grid(row=5, column=0)

    button6 = tk.Button(frame, text="6. XML", width=20)
    button6.grid(row=6, column=0)
    
    button7 = tk.Button(frame, text="7. HTML Desc", width=20)
    button7.grid(row=1, column=1)

    button8 = tk.Button(frame, text="8. esShiny", width=20)
    button8.grid(row=2, column=1)

    button9 = tk.Button(frame, text="9. Convertidor", width=20)
    button9.grid(row=3, column=1)

    button10 = tk.Button(frame, text="10. Desconveritdor", width=20)
    button10.grid(row=4, column=1)
    
    button11 = tk.Button(frame, text="11. Virus", width=20)
    button11.grid(row=5, column=1)
    
    button12 = tk.Button(frame, text="12. Agregar", width=20)
    button12.grid(row=5, column=1)
    
    button13 = tk.Button(frame, text="13. Créditos", width=20)
    button13.grid(row=5, column=1)
    
    button14 = tk.Button(frame, text="14. Salir", width=20, command=close)
    button14.grid(row=6, column=1)
    
    root.mainloop()

main()