from web3 import Web3
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env en la raíz del proyecto
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Cargar la URL del RPC desde el archivo .env
RPC_URL = os.getenv("RPC_URL")

# Verificar que la URL RPC esté cargada
if not RPC_URL:
    print("❌ No se ha encontrado la URL del RPC en el archivo .env.")
    exit()

# Conectar con la blockchain si RPC_URL está disponible
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Verificar si la conexión a la blockchain fue exitosa
if web3.is_connected():
    print("✅ Conexión exitosa a la BNB Chain")
    print(f"🔗 Número de bloque actual: {web3.eth.block_number}")
else:
    print("❌ Error: No se pudo conectar a la blockchain. Verifica la URL RPC.")
    exit()

# Direcciones de los routers de los DEXs
PANCAKESWAP_ROUTER = Web3.to_checksum_address("0x10ED43C718714eb63d5aA57B78B54704E256024E")
APESWAP_ROUTER = Web3.to_checksum_address("0xC0788A3aD43d79aa53B09c2EaCc313A787d1d607")

# ABI del contrato (solo necesitamos getAmountsOut)
DEX_ABI = '[{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"}]'

# Crear instancias de los contratos
pancake_router = web3.eth.contract(address=PANCAKESWAP_ROUTER, abi=DEX_ABI)
apeswap_router = web3.eth.contract(address=APESWAP_ROUTER, abi=DEX_ABI)

# Direcciones de tokens (BNB y USDT)
BNB = Web3.to_checksum_address("0xbb4CdB9Cbd36B01bD1cBaEBF2De08d9173bc095c")  # Wrapped BNB (WBNB)
USDT = Web3.to_checksum_address("0x55d398326f99059fF775485246999027B3197955")  # USDT (BEP-20)

# Obtener las variables de entorno relacionadas con la transacción
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")
GAS_LIMIT = int(os.getenv("GAS_LIMIT", 100000))
GAS_PRICE = Web3.to_wei(os.getenv("GAS_PRICE", '5'), 'gwei')

# Verificar que la clave privada esté cargada
if not PRIVATE_KEY:
    print("❌ No se ha encontrado la clave privada en el archivo .env.")
    exit()

# Función para obtener el precio en un DEX
def get_token_price(router, amount_in_wei=Web3.to_wei(1, 'ether')):
    try:
        # Obtener los precios
        amounts = router.functions.getAmountsOut(amount_in_wei, [BNB, USDT]).call()
        return Web3.from_wei(amounts[1], 'ether')
    except Exception as e:
        print(f"❌ Error al obtener precio: {e}")
        return None

# Obtener precios en cada DEX
price_pancake = get_token_price(pancake_router)
price_apeswap = get_token_price(apeswap_router)

# Mostrar precios
if price_pancake:
    print(f"🥞 PancakeSwap: {price_pancake} USDT")
else:
    print("❌ No se pudo obtener el precio en PancakeSwap.")

if price_apeswap:
    print(f"🦍 ApeSwap: {price_apeswap} USDT")
else:
    print("❌ No se pudo obtener el precio en ApeSwap.")

# Detectar oportunidad de arbitraje
if price_pancake and price_apeswap:
    spread = abs(price_pancake - price_apeswap)
    print(f"📊 Diferencia de precio: {spread} USDT")

    # Verificar si hay oportunidad de arbitraje significativa
    if spread > 1:  # Umbral de 1 USDT para arbitraje
        if price_pancake > price_apeswap:
            print("⚡ Oportunidad de arbitraje: Comprar en ApeSwap y vender en PancakeSwap")
        else:
            print("⚡ Oportunidad de arbitraje: Comprar en PancakeSwap y vender en ApeSwap")
    else:
        print("🔍 No hay oportunidad de arbitraje significativa.")

# Función para enviar una transacción (ejemplo de uso de clave privada, gas y transacciones)
def send_transaction(from_address, to_address, value_in_wei):
    try:
        # Crear la transacción
        transaction = {
            'from': from_address,
            'to': to_address,
            'value': value_in_wei,
            'gas': GAS_LIMIT,  # Usar la variable cargada desde el archivo .env
            'gasPrice': GAS_PRICE,  # Usar la variable cargada desde el archivo .env
            'nonce': web3.eth.getTransactionCount(from_address),
        }

        # Firmar la transacción
        signed_txn = web3.eth.account.signTransaction(transaction, PRIVATE_KEY)

        # Enviar la transacción
        txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(f"✅ Transacción enviada con éxito: {txn_hash.hex()}")
        return txn_hash
    except Exception as e:
        print(f"❌ Error al enviar transacción: {e}")
        return None
