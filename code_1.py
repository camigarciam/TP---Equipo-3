
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
   catalogo=["1.Laguna Azul", "2.Her", "3.Drive", "4.Whiplash", "5.Historia de un Matrimonio", "6.Mente indomable(drama)", "7.Como entrenar a tu Dragón" ]
   for n in catalogo:
       print(n)
   
#3. elegir una peli y mostrar detalles 
def Infopeli(numpeli):

    while numpeli<1 or numpeli>len(catalogo):
        numpeli=int(input("Número de película inválido. Ingrese un número válido"))
    if numpeli==1:
        print("La Laguna Azul\n Géneros:Romance, Drama. Año: 1980")
    elif numpeli==2:
        print("Her\n Géneros:Romance, Ciencia Ficción. Año: 2013")
    elif numpeli==3:
        print("Drive\n Géneros: Acción. Ryan Gosling. Año: 2011")
    elif numpeli==4:
        print("Whiplash\n Géneros: Suspenso, Drama. Año: 2014")
    elif numpeli==5:
        print("Historia de un Matrimonio\n Géneros: Romance, Drama. Año: 2014")
    elif numpeli==6:
        print("Mente indomable\n Géneros: Romance, Drama. Año: 1997")
    elif numpeli==7:
        print("Como Entrenar a tu Dragón\n Géneros: Animación, Aventura. Año: 2010")
    return numpeli
#4. mostrar disponibilidad y seleccionar 
def Alquilarpeli(numero,dispo):

    if disponibilidad[numero - 1] > 0:
        print(f"Hay {disponibilidad[numero - 1]} unidades disponibles de '{catalogo[numero - 1]}'")
        confirmacion = input("¿Deseas alquilar esta película? (s/n): ")
        if confirmacion == 's':
            disponibilidad[numero - 1] -= 1
            print(f"Has alquilado '{catalogo[numero - 1]}'. Quedan {disponibilidad[numero - 1]} unidades disponibles.")
        else:
            print("No se ha realizado el alquiler.")
            return False
    else:
        print(f"Lo siento, '{catalogo[numero - 1]}' no está disponible en este momento.")
    return True
#5. sacar la seleccion 
def Sacar(numpeli):
    pass
#6. recomendacion de una pelicula por si no sabes qué elegir! 
def Recomendacion(num,peli):


    pass
#7. finalizar
def Finalizar():
    pass


#programa principal

#usuario=input("Cree su nombre de usuario: ")
#usuario=validarusuario(usuario)
#nuevacontra=input("Cree su contraseña, debe contener al menos 8 caracteres: ")
#contraseña=validarcontraseña(nuevacontra)

Mostrarpelis()

disponibilidad = [5, 3, 4, 2, 6, 1, 5]
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