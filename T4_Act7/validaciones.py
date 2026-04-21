import re

def validar_email(email):
    # Verifica que tenga @ (no al principio ni final) y termine en .com, .es o .org
    patron = r"^[^@]+@[^@]+\.(com|es|org)$"
    es_valido = False
    if re.match(patron, email):
        es_valido = True
    return es_valido

def validar_telefono(telefono):
    # Verifica que tenga exactamente 9 números
    es_valido = False
    if len(telefono) == 9 and telefono.isdigit():
        es_valido = True
    return es_valido

def validar_campos_llenos(lista_campos):
    # Verifica que ningún campo obligatorio esté vacío
    todos_llenos = True
    for campo in lista_campos:
        if str(campo).strip() == "":
            todos_llenos = False
    return todos_llenos