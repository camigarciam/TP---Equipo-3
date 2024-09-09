import random
from pelis import listapelis


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
   print("Nuestro catálogo es el siguiente")
   for i, peli in enumerate(listapelis):
        print(f"{i+1}. {peli['Titulo']}")
       
   
#3. elegir una peli y mostrar detalles 
def Infopeli(numpeli):
    while numpeli<1 or numpeli>len(listapelis):
        numpeli=int(input("Número de película inválido. Ingrese un número válido: "))
    peli = listapelis[numpeli - 1]
    print(f"{peli['Titulo']}\nGéneros: {peli['Generos']}\nAño: {peli['Año']}")

#4. mostrar disponibilidad y seleccionar 
def Alquilarpeli(numero):
    peli = listapelis[numero - 1]
    if peli["Disponibilidad"] > 0:
        print(f"Hay {peli['Disponibilidad']} unidades disponibles de '{peli['Titulo']}'")
        confirmacion = input("¿Deseas alquilar esta película? (s/n): ")
        if confirmacion == 's':
            peli["Disponibilidad"]-= 1
            print(f"Has alquilado '{peli['Titulo']}'. Quedan {peli['Disponibilidad']} unidades disponibles.")
        else:
            print("No se ha realizado el alquiler.")
            return False
    else:
        print(f"Lo siento, '{peli['Titulo']}' no está disponible en este momento.")
    return True

#5. recomendacion de una pelicula por si no sabes qué elegir! 
def Recomendacion():
    pelis_disponibles = [i for i, peli in enumerate(listapelis) if peli['Disponibilidad'] > 0]
    if pelis_disponibles:
        indice_random = random.randint(0, len(pelis_disponibles) - 1)
        peli_recomendada = pelis_disponibles[indice_random]
        print(f"Te recomendamos: {listapelis[peli_recomendada]}")
        return peli_recomendada
    else: 
        print("Lo siento, no hay peliculas disponibles para recomendar")
        return None

#6. finalizar
def Finalizar():
    pass


#programa principal

usuario=input("Cree su nombre de usuario: ")
usuario=validarusuario(usuario)
nuevacontra=input("Cree su contraseña, debe contener al menos 8 caracteres: ")
contraseña=validarcontraseña(nuevacontra)

Mostrarpelis()

numero=int(input("Ingrese el número de película sobre la que desea obtener más información: "))
# Comprobar disponibilidad y alquilar
while True:
    Infopeli(numero)
    if Alquilarpeli(numero):
        break
    else:
        Mostrarpelis()
        numero=int(input("Ingrese el número de película sobre la que desea obtener más información"))
        

recomendada = input("¿Desea que le recomendemos una pelicula? (s/n): ")
if recomendada.lower() == "s":
    Recomendacion()