import requests
import json

# URL del webhook en la aplicación Flask
webhook_url = 'http://127.0.0.1:4000/webhook'

# Datos que deseas enviar en el POST request
data = {
  "entry": [
    {
      "changes": [
        {
          "value": {
            "metadata": {
              "display_phone_number": "1234567890"
            },
            "messages": [
              {
                "from": "1234567890",
                "text": {
                  "body": "¡Entendido! Aquí está el resumen actualizado de tu pedido:<PEDIDO>{\"productos\": [{\"id\": 1,\"nombre\": \"Croissant con jamón y queso\",\"cantidad\": 10,\"precio\": 10.00,\"total\": 100.00}],\"total_pedido\": 182.00}</PEDIDO>¡Gracias por tu pedido!"
                }
              }
            ],
            "statuses": [
              {
                "status": "read"
              }
            ]
          }
        }
      ]
    }
  ]
}


#data_get = {
#    "hub.mode":"suscribe",
#    "hub.challenge":"168463300",
#    "hub.verify_token":"12345"
#}

# Cabeceras, si necesitas enviar alguna
headers = {
    'Content-Type': 'application/json'
}

# Enviar el POST request
#response = requests.get(webhook_url, params=data_get)
# Imprimir la respuesta del servidor
#print('Estado de la respuesta:', response.status_code)
#print('Contenido de la respuesta:', response.text)

response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

# Imprimir la respuesta del servidor
print('Estado de la respuesta:', response.status_code)
print('Contenido de la respuesta:', response.text)