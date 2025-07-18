# README del Sistema de Generación Automática de Documentación

## Descripción

Este sistema automatiza la generación de documentación LaTeX desde archivos README/Markdown para crear datasheets profesionales con soporte para:

- ✅ Múltiples idiomas
- ✅ Tablas automáticas
- ✅ Caracteres especiales 
- ✅ Imágenes maestras compartidas
- ✅ Control de saltos de página
- ✅ Generación automática de PDF

## Estructura del Proyecto

```
proyecto/
├── generate_docs.py          # Script principal de generación
├── template.tex             # Template LaTeX mejorado
├── images/                  # Imágenes maestras compartidas
├── docs/                    # PDFs y archivos LaTeX generados
├── en/                      # Contenido en inglés
│   ├── content.md          # Contenido principal
│   └── metadata.yaml       # Metadatos del documento
├── es/                      # Contenido en español
│   ├── content.md          # Contenido principal
│   └── metadata.yaml       # Metadatos del documento
└── [otros idiomas]/         # Más idiomas según necesidad
```

## Instalación y Configuración

### Dependencias de Python

```bash
pip install PyYAML
```

### Dependencias de LaTeX

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install texlive-full
```

#### macOS:
```bash
brew install --cask mactex
```

#### Windows:
Instalar MiKTeX desde https://miktex.org/

## Uso

### Generación Completa

Generar documentación para todos los idiomas:

```bash
python generate_docs.py
```

### Generación por Idioma

Generar solo para un idioma específico:

```bash
python generate_docs.py --lang es
python generate_docs.py --lang en
```

### Especificar Directorio

```bash
python generate_docs.py --dir /ruta/a/tu/proyecto
```

## Configuración de Contenido

### Archivo metadata.yaml

Cada directorio de idioma debe tener un archivo `metadata.yaml`:

```yaml
title: "DevLab Module Datasheet"
subtitle: "Especificaciones Técnicas Completas"
author: "Equipo DevLab"
date: "2025-07-18"
version: "v1.0"
organization: "Tu Empresa"
logo: "logo.png"        # Opcional: logo en directorio images/
toc: true              # Generar tabla de contenidos
lof: true              # Generar lista de figuras
lot: true              # Generar lista de tablas
```

### Archivo content.md

Contenido principal en formato Markdown con extensiones:

#### Headers
```markdown
# Capítulo Principal
## Sección
### Subsección
#### Párrafo
```

#### Imágenes
```markdown
![Descripción de la imagen](images/diagrama.png)
```
Las imágenes se copian automáticamente desde el directorio `images/` a `docs/`

#### Tablas
```markdown
| Parámetro | Valor | Unidad |
|-----------|-------|--------|
| Voltaje   | 3.3   | V      |
| Corriente | 150   | mA     |
```

#### Listas
```markdown
- Elemento 1
- Elemento 2
  - Subelemento

1. Elemento numerado
2. Otro elemento
```

#### Formato de Texto
```markdown
**Texto en negrita**
*Texto en itálica*
`Código inline`
```

#### Bloques de Código
```markdown
```python
def ejemplo():
    return "Hola mundo"
```
```

#### Enlaces
```markdown
[Texto del enlace](https://ejemplo.com)
```

## Características Avanzadas

### Control de Saltos de Página

El sistema incluye control automático de saltos de página:

- Evita separar títulos de su contenido
- Añade espacios flexibles antes de nuevas secciones
- Previene viudas y huérfanas

### Manejo de Caracteres Especiales

Soporte completo para:
- Acentos y caracteres UTF-8
- Símbolos especiales de LaTeX
- Múltiples idiomas con babel

### Imágenes Maestras

- Coloca todas las imágenes en el directorio `images/`
- Se copian automáticamente a `docs/` con prefijo de idioma
- Soporte para formatos: PNG, JPG, PDF, SVG

### Tablas Profesionales

- Conversión automática de tablas Markdown
- Uso de booktabs para formato profesional
- Numeración automática y referencias cruzadas

## Personalización

### Modificar Template LaTeX

Edita `template.tex` para:
- Cambiar estilo de página
- Añadir packages adicionales
- Modificar formato de títulos
- Ajustar espaciado

### Añadir Nuevos Idiomas

1. Crear directorio `[codigo_idioma]/`
2. Añadir `content.md` y `metadata.yaml`
3. Ejecutar el generador

### Configuración de Código

Modifica la configuración de `listings` en el template para diferentes lenguajes de programación.

## Solución de Problemas

### Error de Compilación LaTeX

1. Verificar que todas las dependencias estén instaladas
2. Revisar caracteres especiales en el contenido
3. Verificar que las imágenes existan en el directorio

### Imágenes no Aparecen

1. Verificar que las imágenes estén en el directorio `images/`
2. Comprobar rutas en el archivo Markdown
3. Verificar permisos de archivos

### Tabla mal Formateada

1. Asegurar que todas las filas tengan el mismo número de columnas
2. Verificar que hay línea separadora después del header
3. Usar caracteres pipe `|` correctamente

## Ejemplos de Uso

### Datasheet de Microcontrolador

```markdown
# DevLab ESP32 Module

## Especificaciones Generales

| Parámetro | Valor | Notas |
|-----------|-------|-------|
| CPU | Dual-core Xtensa LX6 | 240 MHz |
| RAM | 520 KB | SRAM interna |

![Diagrama de pines](images/pinout.png)

## Características

- **Wi-Fi**: 802.11 b/g/n
- **Bluetooth**: v4.2 BR/EDR y BLE
- **GPIOs**: Hasta 27 pines configurables
```

### Documentación de API

```markdown
# API Reference

## Función de Inicialización

```c
int devlab_init(devlab_config_t *config);
```

### Parámetros

- `config`: Puntero a estructura de configuración

### Retorno

- `0`: Éxito
- `-1`: Error
```

## Contribución

1. Fork del repositorio
2. Crear rama de feature
3. Hacer commits con mensajes descriptivos
4. Crear Pull Request

## Licencia

[Especificar licencia aquí]
