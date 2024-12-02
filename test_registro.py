import pytest
import json
import shutil
import os
from code_1 import registrarUsuario

# Cargar los usuarios desde el archivo de prueba
def cargar_usuarios_test():
    with open('usuarios_test.json', 'r') as file:
        return json.load(file)

# Test de registrar usuario
def test_registrar_usuario():
    # Copiar el archivo original usuarios.json a usuarios_test.json antes de la prueba
    if os.path.exists('usuarios.json'):
        shutil.copy('usuarios.json', 'usuarios_test.json')

    try:
        # Cargar los usuarios desde el archivo de prueba
        usuarios = cargar_usuarios_test()
        usuario_input = "nuevo_usuario"
        contra_input = "contraseña123"

        resultado, usuarios_actualizados = registrarUsuario(usuario_input, contra_input, usuarios)
        assert resultado == True
        assert any(u['nombreUsuario'] == usuario_input for u in usuarios_actualizados)
    finally:
        # Restaurar el archivo original usuarios.json después de la prueba
        if os.path.exists('usuarios_test.json'):
            shutil.copy('usuarios_test.json', 'usuarios.json')

# Test para intentar registrar un usuario con un nombre ya existente
def test_usuario_existente():
    # Copiar el archivo original usuarios.json a usuarios_test.json antes de la prueba
    if os.path.exists('usuarios.json'):
        shutil.copy('usuarios.json', 'usuarios_test.json')

    try:
        # Cargar los usuarios desde el archivo de prueba
        usuarios = cargar_usuarios_test()
        registrarUsuario("usuario1", "pass123", usuarios)

        resultado, usuarios_actualizados = registrarUsuario("usuario1", "nueva_contra", usuarios)
        assert resultado == False
    finally:
        # Restaurar el archivo original usuarios.json después de la prueba
        if os.path.exists('usuarios_test.json'):
            shutil.copy('usuarios_test.json', 'usuarios.json')
