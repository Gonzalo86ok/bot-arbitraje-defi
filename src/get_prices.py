from web3 import Web3
import os

# Cargar RPC_URL desde el .env
RPC_URL = os.getenv("RPC_URL")

# Conectar con la blockchain
web3 = Web3(Web3.HTTPProvider(RPC_URL))

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

# Función para obtener el precio en un DEX
def get_token_price(router, amount_in_wei=Web3.to_wei(1, 'ether')):
    try:
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

    if spread > 1:  # Umbral de 1 USDT para arbitraje
        if price_pancake > price_apeswap:
            print("⚡ Oportunidad de arbitraje: Comprar en ApeSwap y vender en PancakeSwap")
        else:
            print("⚡ Oportunidad de arbitraje: Comprar en PancakeSwap y vender en ApeSwap")
    else:
        print("🔍 No hay oportunidad de arbitraje significativa.")
