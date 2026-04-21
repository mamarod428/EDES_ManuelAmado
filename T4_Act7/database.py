import sqlite3

def conectar():
    return sqlite3.connect("empresa.db")

def inicializar_db():
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Crear tabla usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            rol TEXT
        )
    ''')
    
    # Crear tabla clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL,
            empresa TEXT,
            fecha_alta TEXT NOT NULL
        )
    ''')
    
    # Crear tabla pedidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER,
            fecha TEXT NOT NULL,
            importe REAL NOT NULL,
            estado TEXT NOT NULL,
            descripcion TEXT,
            FOREIGN KEY(id_cliente) REFERENCES clientes(id)
        )
    ''')
    
    # Insertar usuarios de prueba si no existen
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES ('admin', 'admin123', 'Administrador')")
        cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES ('ceo', 'ceo123', 'CEO')")
        
    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    inicializar_db()
    print("Base de datos inicializada correctamente.")