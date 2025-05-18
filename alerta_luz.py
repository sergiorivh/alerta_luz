import os, datetime, requests

# 1. Leer variables de entorno
TOKEN_ESIOS = os.getenv("TOKEN_ESIOS")
TOKEN_BOT   = os.getenv("TOKEN_BOT")
CHAT_ID     = os.getenv("CHAT_ID")

# 2. Obtener fecha de hoy
hoy = datetime.date.today().isoformat()

# 3. Llamada a la API PVPC de ESIOS
url = (
    "https://api.esios.ree.es/archives/70"
    f"?start_date={hoy}T00:00:00&end_date={hoy}T23:59:59"
)
headers = {"Authorization": f'Token token="{TOKEN_ESIOS}"'}
datos = requests.get(url, headers=headers).json()["PVPC"]["values"]

# 4. Encontrar hora más barata
minimo = min(datos, key=lambda x: x["value"])
hora   = minimo["hour"]
precio = minimo["value"]

# 5. Enviar mensaje por Telegram
texto = f"⏰ Hoy la hora más barata es {hora}:00–{hora}:59 con {precio:.3f} €/kWh"
tg_url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
payload = {"chat_id": CHAT_ID, "text": texto}
requests.post(tg_url, json=payload)
