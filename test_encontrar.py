import pytest

from code_1 import encontrar_usuario

def test_usuario_encontrado():
    usuarios = [
        {"nombreUsuario": "user1", "contrasena": "buenastardesxd12"},
        {"nombreUsuario": "user2", "contrasena": "contraseniadificil"},
    ]
    resultado = encontrar_usuario("user1", usuarios)
    assert resultado == {"nombreUsuario": "user1", "contrasena": "buenastardesxd12"}

def test_usuario_no_encontrado():
    usuarios = [
        {"nombreUsuario": "user1", "contrasena": "buenastardesxd12"},
        {"nombreUsuario": "user2", "contrasena": "contraseniadificil"},
    ]
    resultado = encontrar_usuario("user3", usuarios)
    assert resultado is None
