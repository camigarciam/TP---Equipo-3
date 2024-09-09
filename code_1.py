
import random


##login 
def validarusuario(usuario):
        while len(usuario)<6:
            print("El nombre de usuario debe contener al menos 6 caracteres")
            usuario=input("Ingrese su nombre de usuario: ")
        print("El nombre de usuario es válido")
        return usuario

def validarcontraseña(nuevacontra):
    while len(nuevacontra) <8:
        nuevacontra=input("Contraseña invalida, ingrese la contraseña nuevamente: ")
    print("Contraseña válida")
    contraseña=input("Confirme su contraseña: ")
    while contraseña != nuevacontra:
        contraseña=input("Las contraseñas no coinciden, ingrese la contraseña nuevamente: ")
    else:
        print("Contraseña confirmada")
    return contraseña


#2. mostrar los titulos de las peliculas 
def Mostrarpelis():
   global catalogo
   print("Nuestro catálogo es el siguiente")
   catalogo = [
        {"numero": 1, "titulo": "Laguna Azul", "generos": "Romance, Drama", "lanzamiento": 1980, "reparto": "Brooke Shields, Christopher Atkins"},
        {"numero": 2, "titulo": "Her", "generos": "Romance, Ciencia Ficción", "lanzamiento": 2013, "reparto": "Joaquin Phoenix"},
        {"numero": 3, "titulo": "Drive", "generos": "Acción", "lanzamiento": 2011, "reparto": "Ryan Gosling"},
        {"numero": 4, "titulo": "Whiplash", "generos": "Suspenso, Drama", "lanzamiento": 2014, "reparto": "Miles Teller, J.K Simmons"},
        {"numero": 5, "titulo": "Historia de un Matrimonio", "generos": "Romance, Drama", "lanzamiento": 2014, "reparto": "Adam Driver, Scarlett Johanson"},
        {"numero": 6, "titulo": "Mente Indomable", "generos": "Romance, Drama", "lanzamiento": 1997, "reparto": "Matt Damon, Ben Affleck"},
        {"numero": 7, "titulo": "Como Entrenar a tu Dragón", "generos": "Animación, Aventura", "lanzamiento": 2010},
        {"numero":8, "titulo":"El viaje de Chihiro", "generos": "Animación", "lanzamiento": 2001},
        {"numero":9, "titulo":"La Langosta", "generos": "Drama", "reparto": "Collin Farrell", "lanzamiento": 2015},
        {"numero":10, "titulo": "The Basketball Diaries", "generos": "Drama", "reparto": "Leonardo Di Caprio"},
        {"numero": 11, "titulo": "Titanic", "generos": "Drama", "reparto": "Leonardo Di Caprio", "lanzamiento":1991},
        {"numero": 12, "titulo": "The Talented Mr Ripley", "generos": "Drama", "reparto": "Jude Law, Matt Damon", "lanzamiento":"1999"} ,
        {"numero": 13, "titulo": "Ghost Rider", "generos": "Aventura", "reparto": "Nicolas Cage", "lanzamiento": 2007}
   ]
   for peli in catalogo:
        print(f"{peli['numero']}. {peli['titulo']}")
       
   
#3. elegir una peli y mostrar detalles 
def Infopeli(numpeli):
    while numpeli<1 or numpeli>len(catalogo):
        numpeli = int(input("Número de película inválido. Ingrese un número válido"))
    for peli in catalogo:
        if peli["numero"]==numpeli:
            print(f"Título: {peli['titulo']}")
            print(f"Géneros: {peli['generos']}")
            print(f"Año: {peli['lanzamiento']}")
            reparto = peli.get("reparto", "No disponible")
            print(f"Reparto: {reparto}")
    return numpeli
   
    

    
#4. mostrar disponibilidad y seleccionar 
def Alquilarpeli(numero,disponibilidad):

    if disponibilidad[numero - 1] > 0:
        print(f"Hay {disponibilidad[numero - 1]} unidades disponibles de '{catalogo[numero - 1]["titulo"]}'")
        confirmacion = input("¿Deseas alquilar esta película? (s/n): ")
        if confirmacion == 's':
            disponibilidad[numero - 1] -= 1
            print(f"Has alquilado '{catalogo[numero - 1]["titulo"]}'. Quedan {disponibilidad[numero - 1]} unidades disponibles.")
        else:
            print("No se ha realizado el alquiler.")
            return False
    else:
        print(f"Lo siento, '{catalogo[numero - 1]["titulo"]}' no está disponible en este momento.")
    return True
#5. sacar la seleccion 
def Sacar(numpeli):
    pass

#6. recomendacion de una pelicula por si no sabes qué elegir! 
def Recomendacion():
    peliculas_disponibles = [i + 1 for i in range(len(disponibilidad)) if disponibilidad[i]]
    if peliculas_disponibles:
        indice_aleatorio = random.randint(0, len(peliculas_disponibles) - 1)
        pelicula_recomendada = peliculas_disponibles[indice_aleatorio]
        print(f"Te recomendamos: {catalogo[pelicula_recomendada - 1]["titulo"]}")
        return pelicula_recomendada
    else: 
        print("Lo siento, no hay peliculas disponibles para recomendar")
        return None

#7. finalizar
def Finalizar():
    pass


#programa principal

usuario=input("Cree su nombre de usuario: ")
usuario=validarusuario(usuario)
nuevacontra=input("Cree su contraseña, debe contener al menos 8 caracteres: ")
contraseña=validarcontraseña(nuevacontra)

Mostrarpelis()

disponibilidad = [5, 3, 4, 2, 6, 1, 5,0,2,3,11,2,1]
numero=int(input("Ingrese el número de película sobre la que desea obtener más información"))
# Comprobar disponibilidad y alquilar
while True:
    Infopeli(numero)
    if Alquilarpeli(numero, disponibilidad):
        break
    else:
        Mostrarpelis()
        numero=int(input("Ingrese el número de película sobre la que desea obtener más información"))
        Infopeli(numero)
        Alquilarpeli(numero, disponibilidad)

recomendada = input("¿Desea que le recomendemos una pelicula? (s/n): ")
if recomendada == "s":
    Recomendacion()