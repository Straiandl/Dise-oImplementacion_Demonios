from flask import Flask, request, render_template_string, jsonify
import json
import datetime
import re

app = Flask(__name__)

# Detector simple de patrones de ataque (Inyección SQL, XSS, Path Traversal)
PATRONES_SOSPECHOSOS = [
    r"' OR '1'='1",
    r"SELECT \* FROM",
    r"<script>",
    r"\.\./",
    r"UNION SELECT"
]

def registrar_evento_sospechoso(ip, payload, tipo_ataque):
    evento = {
        "timestamp": datetime.datetime.now().isoformat(),
        "ip_origen": ip,
        "tipo": tipo_ataque,
        "payload_detectado": payload,
        "accion": "Peticion bloqueada y registrada"
    }
    
    # Guardamos el incidente en nuestro log JSON
    try:
        with open("security_events.json", "r+") as f:
            logs = json.load(f)
            logs.append(evento)
            f.seek(0)
            json.dump(logs, f, indent=4)
    except FileNotFoundError:
        with open("security_events.json", "w") as f:
            json.dump([evento], f, indent=4)

    print(f" [ALERTA DE SEGURIDAD] Intento sospechoso detectado desde IP: {ip}")

# HTML simple para el formulario
FORM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Acceso al Sistema</title></head>
<body style="font-family: Arial; margin: 40px;">
    <h2> Iniciar Sesión en el Sistema</h2>
    <form method="POST" action="/login">
        <label>Usuario:</label><br>
        <input type="text" name="username" required><br><br>
        <label>Contraseña:</label><br>
        <input type="password" name="password" required><br><br>
        <button type="submit">Ingresar</button>
    </form>
    {% if msg %}<p style="color: red;">{{ msg }}</p>{% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(FORM_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    ip_cliente = request.remote_addr
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    # Verificamos si la entrada contiene patrones sospechosos
    entrada_completa = f"{username} {password}"
    for patron in PATRONES_SOSPECHOSOS:
        if re.search(patron, entrada_completa, re.IGNORECASE):
            registrar_evento_sospechoso(ip_cliente, entrada_completa, "Intento de Inyección / Payload Sospechoso")
            return render_template_string(FORM_TEMPLATE, msg="⚠️ Acceso Denegado: Actividad sospechosa detectada.")

    # Simulación de verificación normal
    if username == "admin" and password == "1234":
        return "<h3>Welcome Admin!</h3>"
    else:
        return render_template_string(FORM_TEMPLATE, msg="Credenciales incorrectas.")

if __name__ == '__main__':
    app.run(port=5000, debug=True)