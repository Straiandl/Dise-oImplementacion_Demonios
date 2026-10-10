# Práctica: Sistema de Ciberseguridad y Monitoreo de Integridad (FIM)

##  Descripción General
Este repositorio contiene la implementación de un sistema de ciberseguridad básico dividido en dos capas:
1. **Aplicación Web Protegida (WAF Simulado):** Un formulario de inicio de sesión en Flask que detecta y bloquea intentos de inyección de código (SQLi, XSS).
2. **Monitor de Integridad de Archivos (FIM):** Un demonio/proceso en segundo plano que vigila un archivo de configuración crítico. Si detecta una modificación no autorizada mediante el cálculo de hashes SHA-256, restaura automáticamente la versión segura desde un respaldo en formato JSON.

---

##  Estructura del Repositorio

| Archivo | Descripción / Contenido |
| :--- | :--- |
| 📄 **`app.py`** | Servidor web Flask con el formulario de login y la lógica de detección de payloads maliciosos. |
| 📄 **`fim_monitor.py`** | Script de monitoreo continuo que verifica los hashes y aplica la restauración (Resiliencia). |
| 📄 **`config.json`** | Archivo crítico del sistema (Objetivo de los ataques de modificación). |
| 📄 **`config_backup.json`** | Copia maestra (Golden Record) utilizada para restaurar el sistema en caso de falla o ataque. |
| 📄 **`security_events.json`** | Bitácora (Log) donde se registran los ataques bloqueados y las restauraciones automáticas. |

---

##  Resumen de Conceptos Clave Aplicados

### 1. Detección de Intrusiones (IDS / WAF)
El sistema intercepta las peticiones HTTP antes de procesarlas. Si la carga útil (*payload*) coincide con expresiones regulares de ataques conocidos (ej. `' OR '1'='1`), se bloquea el acceso para prevenir compromisos en la base de datos (Inyección SQL).

### 2. File Integrity Monitoring (FIM)
Técnica de seguridad que consiste en calcular la huella digital (Hash Criptográfico) de un archivo. En este caso se utiliza **SHA-256**. Si un solo bit del archivo `config.json` es alterado, el hash resultante cambia drásticamente, disparando la alerta.

### 3. Tolerancia a Fallas y Restauración
Al detectar una anomalía (estado de *Error* provocado por un ataque), el sistema no colapsa. Extrae el estado seguro desde `config_backup.json` (Checkpoint seguro) y sobreescribe el archivo vulnerado, garantizando la continuidad del negocio.

---

## 📸 Capturas de Pantalla (Evidencias de la Práctica)

> **Nota para el alumno:** Reemplaza las rutas de las imágenes `(./img/tu_captura.png)` con las rutas reales de tus capturas de pantalla.

### 1. Aplicación Web Ejecutándose
*Formulario de inicio de sesión cargado exitosamente en localhost:*
![Formulario Web](https://github.com/Straiandl/Dise-oImplementacion_Demonios/blob/6b976f7229dacef59a63f780899aba4c2d5459cc/Seguridad1.png)

### 2. Bloqueo de Ataque (Inyección SQL)
*Evidencia del bloqueo en la web al intentar ingresar el payload malicioso `' OR '1'='1`:*
![Ataque Bloqueado](https://github.com/Straiandl/Dise-oImplementacion_Demonios/blob/6b976f7229dacef59a63f780899aba4c2d5459cc/Seguridad2.png)

### 3. Monitor FIM Restaurando el Archivo
*Consola del monitor detectando la alteración del archivo `config.json` y aplicando la restauración automática:*
![Restauración FIM](https://github.com/Straiandl/Dise-oImplementacion_Demonios/blob/6b976f7229dacef59a63f780899aba4c2d5459cc/Seguridad3.png)

### 4. Registro de Eventos (Logs)
*Archivo `security_events.json` mostrando la bitácora de los incidentes de seguridad reportados:*
![Registro JSON](https://github.com/Straiandl/Dise-oImplementacion_Demonios/blob/6b976f7229dacef59a63f780899aba4c2d5459cc/Seguridad4.png)

---

##  Instrucciones de Ejecución

Para correr este entorno en modo local, se requieren dos terminales simultáneas:

1. **Levantar el servidor web:**
   ```bash
   python app.py
   ```
   *(Acceder a http://127.0.0.1:5000 en el navegador)*

2. **Iniciar el Monitor de Integridad (En otra terminal):**
   ```bash
   python fim_monitor.py
   ```

---
