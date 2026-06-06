## skd-bot-de-whatsapp

SDK orientado a la creación de herramientas compatibles con bots de WhatsApp.

Permite desarrollar módulos reutilizables, integrar servicios externos y organizar funcionalidades de forma modular para simplificar el desarrollo de bots.

## Características

- Arquitectura modular.
- Fácil integración de nuevas herramientas.
- Compatible con proyectos Node.js.
- Soporte para servicios externos y APIs.
- Escalable y fácil de mantener.
- Diseñado para automatizaciones en WhatsApp.

---

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/LozanoTH/skd-bot-de-whatsapp.git
```

Accede al directorio:

```bash
cd skd-bot-de-whatsapp
```

Instala las dependencias:

```bash
npm install
```

---

## Estructura recomendada

```text
skd-bot-de-whatsapp/
│
├── tools/
│   ├── ejemplo.js
│   ├── firebase.js
│   └── whatsapp.js
│
├── handlers/
│   └── mensajes.js
│
├── config/
│   └── config.js
│
├── index.js
├── package.json
└── README.md
```

---

## Crear una herramienta

Cada herramienta debe exportar un objeto con la información necesaria para ser utilizada por el sistema.

Ejemplo:

```javascript
module.exports = {
    name: "saludo",

    description: "Devuelve un saludo",

    async execute(context) {
        return {
            success: true,
            message: "Hola mundo"
        };
    }
};
```

---

## Registrar una herramienta

```javascript
const saludo = require("./tools/saludo");

sdk.register(saludo);
```

---

## Ejecutar una herramienta

```javascript
const result = await sdk.run("saludo");

console.log(result);
```

Salida:

```json
{
  "success": true,
  "message": "Hola mundo"
}
```

---

## Contexto

Las herramientas reciben un objeto de contexto con información relevante.

Ejemplo:

```javascript
module.exports = {
    name: "usuario",

    async execute(ctx) {
        return {
            numero: ctx.sender,
            nombre: ctx.pushName
        };
    }
};
```

---

## Uso con WhatsApp

Ejemplo de integración:

```javascript
bot.onMessage(async (message) => {

    const result = await sdk.run("saludo", {
        sender: message.from
    });

    await message.reply(result.message);

});
```

---

## Firebase Realtime Database

Ejemplo de almacenamiento:

```javascript
const db = firebase.database();

await db.ref("usuarios/123").set({
    nombre: "Juan",
    fecha: Date.now()
});
```

Lectura:

```javascript
const snapshot = await db
    .ref("usuarios/123")
    .once("value");

console.log(snapshot.val());
```

---

## Herramientas Web

El SDK puede utilizarse para:

- Formularios web.
- APIs REST.
- Firebase.
- WhatsApp.
- Automatización de mensajes.
- Sistemas de tickets.
- Registro de usuarios.
- Paneles administrativos.

---

## Flujo típico

```text
Usuario
   │
   ▼
WhatsApp
   │
   ▼
Bot
   │
   ▼
SDK
   │
   ├── Herramienta A
   ├── Herramienta B
   ├── Firebase
   └── API Externa
```

---

## Buenas prácticas

- Mantener cada herramienta independiente.
- Validar todos los parámetros de entrada.
- Manejar errores mediante try/catch.
- Documentar cada módulo.
- Evitar lógica duplicada.

---

## Ejemplo completo

```javascript
module.exports = {
    name: "ping",

    description: "Comprueba el funcionamiento",

    async execute() {

        return {
            success: true,
            message: "pong"
        };

    }
};
```

Uso:

```javascript
const result = await sdk.run("ping");

console.log(result.message);
```

Resultado:

```text
pong
```

---

## Contribuciones

1. Haz un fork.
2. Crea una rama nueva.
3. Realiza tus cambios.
4. Envía un Pull Request.

---

## Licencia

Este proyecto puede modificarse y utilizarse libremente según las condiciones establecidas por su autor.

---

Desarrollado para facilitar la creación de herramientas y automatizaciones para bots de WhatsApp.
