import pytest
import json
import shutil
import os
from code_1 import registrarUsuario

def cargar_usuarios_test():
    with open('usuarios_test.json', 'r') as file:
        return json.load(file)


def test_registrar_usuario():
    if os.path.exists('usuarios.json'):
        shutil.copy('usuarios.json', 'usuarios_test.json')

    try:
        usuarios = cargar_usuarios_test()
        usuario_input = "nuevo_usuario"
        contra_input = "contraseña123"

        resultado, usuarios_actualizados = registrarUsuario(usuario_input, contra_input, usuarios)
        assert resultado == True
        assert any(u['nombreUsuario'] == usuario_input for u in usuarios_actualizados)
    finally:
        if os.path.exists('usuarios_test.json'):
            shutil.copy('usuarios_test.json', 'usuarios.json')

def test_usuario_existente():
  
    if os.path.exists('usuarios.json'):
        shutil.copy('usuarios.json', 'usuarios_test.json')

    try:
        usuarios = cargar_usuarios_test()
        registrarUsuario("usuario1", "pass123", usuarios)

        resultado, usuarios_actualizados = registrarUsuario("usuario1", "nueva_contra", usuarios)
        assert resultado == False
    finally:
        if os.path.exists('usuarios_test.json'):
            shutil.copy('usuarios_test.json', 'usuarios.json')
