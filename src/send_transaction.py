from web3 import Web3
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configura tu proveedor de la red BNB Chain
web3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))

# Función para enviar transacciones
def send_transaction(from_address, to_address, value_in_wei, gas_limit=200000, gas_price=None):
    try:
        # Obtener el nonce de la dirección
        nonce = web3.eth.getTransactionCount(from_address)

        # Establecer el precio del gas (si no se proporciona, se usa el predeterminado)
        if gas_price is None:
            gas_price = web3.eth.gas_price

        # Crear la transacción
        transaction = {
            'nonce': nonce,
            'to': to_address,
            'value': value_in_wei,
            'gas': gas_limit,
            'gasPrice': gas_price,
            'chainId': 56  # ID de la BNB Chain
        }

        # Firmar la transacción con la clave privada
        private_key = os.getenv("PRIVATE_KEY")  # Cargar la clave privada desde las variables de entorno
        signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

        # Enviar la transacción
        tx_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

        # Imprimir el hash de la transacción
        print(f"Transacción enviada, hash: {web3.toHex(tx_hash)}")

        return tx_hash
    except Exception as e:
        print(f"❌ Error al enviar transacción: {e}")
        return None

# Ejemplo de uso
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")  # Dirección de tu wallet
APESWAP_ROUTER = "direccion_de_router_de_apeswap"  # Dirección del router de ApeSwap
buy_transaction_hash = send_transaction(SENDER_ADDRESS, APESWAP_ROUTER, Web3.toWei(0.05, 'ether'))  # Comprar 0.05 BNB en ApeSwap
