from web3 import Web3
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Verificar si la variable RPC_URL se ha cargado
RPC_URL = os.getenv("RPC_URL")

if RPC_URL is None:
    print("❌ No se ha encontrado la URL del RPC.")
else:
    print(f"🔍 RPC_URL encontrada: {RPC_URL}")

    # Conectar a la blockchain
    web3 = Web3(Web3.HTTPProvider(RPC_URL))

    # Verificar si la conexión es exitosa
    if web3.is_connected():
        print("✅ Conexión exitosa a la BNB Chain")
    else:
        print("❌ Error: No se pudo conectar a la BNB Chain.")
