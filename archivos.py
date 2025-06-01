import pickle

def grabaTxt(archivoTxt,datos):
    try:
        f=open(archivoTxt,"w")
        f.write(datos)
        f.close()
    except:
        print("Error al leer el archivo: ", archivoTxt)
    return

def leeTxtLineas(txt):
    with open(txt, 'r', encoding='utf-8') as f:
        return f.readlines()

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
        print("Error al leer el archivo: ", archivo)
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

misPokemonsTxt = "Mis pokémons.txt"
misIdAtrapados = "Mis id pokemons atrapados"
misPokemonsAtrapadosPkl = "Mis pokémons atrapados"
matrizPokemonAD = "Matriz de pokémons"
diccPokemonAM = "Diccionario de pokémons"
excelPokemons = "Mis pokémons.csv"