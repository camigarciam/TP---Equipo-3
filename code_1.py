
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
   pass
#3. elegir una peli y mostrar detalles 
def Elegirpeli(numpeli,peli):
    pass
#4. mostrar disponibilidad y seleccionar 
def Disponibilidad(numpeli,dispo):
    pass
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

usuario=input("Cree su nombre de usuario: ")
usuario=validarusuario(usuario)
nuevacontra=input("Cree su contraseña, debe contener al menos 8 caracteres: ")
contraseña=validarcontraseña(nuevacontra)