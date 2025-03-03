from web3 import Web3
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Verificar si la variable RPC_URL se ha cargado
RPC_URL = os.getenv("RPC_URL")

if RPC_URL is None:
    print("❌ No se ha encontrado la URL del RPC.")
else:
    print(f"🔍 RPC_URL encontrada: {RPC_URL}")

# Conectar a la blockchain
web3 = Web3(Web3.HTTPProvider(RPC_URL)) if RPC_URL else None

if web3 and web3.is_connected():
    print("✅ Conectado a la BNB Chain")
    print(f"Último bloque: {web3.eth.block_number}")
else:
    print("❌ No se pudo conectar a la blockchain. Verifica la URL RPC.")



