# Documentación de Hardware

## Descripción General

El módulo sensor de presión barométrica ICP-10111 es un sensor ambiental compacto con capacidades integradas de monitoreo ambiental, diseñado para aplicaciones IoT y mediciones atmosféricas precisas.

## Características Principales

- **Sensor de presión ICP-10111** (Alta precisión)
- **Sensor ambiental BME688** (Temperatura, humedad, gas)
- **Modos de bajo consumo** energético
- **Conectividad I2C/QWIIC**
- **Factor de forma compacto** con orificios castellanos

# Hardware

## ⚙️ Especificaciones Técnicas

### Especificaciones del Sensor

| Parámetro | Valor | Unidad | Notas |
|-----------|-------|--------|-------|
| Rango de Presión | 300-1250 | hPa | Presión absoluta |
| Precisión de Presión | ±0.4 | hPa | A 25°C |
| Rango de Temperatura | -40 a +85 | °C | Rango de operación |
| Rango de Humedad | 0-100 | %RH | Humedad relativa |
| Interfaz | I2C | - | Compatible QWIIC |

### Especificaciones de Alimentación

| Parámetro | Mín | Típ | Máx | Unidad | Condiciones |
|-----------|-----|-----|-----|--------|-------------|
| Voltaje de Alimentación | 3.0 | 3.3 | 5.0 | V | Operación Normal |
| Corriente Activa | - | 1.2 | 2.0 | mA | Medición continua |
| Corriente en Reposo | - | 0.1 | 0.5 | µA | Modo standby |
| Salida del Regulador | - | 1.8 | - | V | LDO interno |

## 🔌 Distribución de Pines

![Diagrama de Pines](unit_pinout_v_0_0_1_ue0094_icp10111_barometric_pressure_sensor_en.jpg)

| Etiqueta | Función | Notas |
|----------|---------|-------|
| VCC | Alimentación | 3.3V o 5V |
| GND | Tierra | Tierra común para todos los componentes |
| SDA | Datos I2C | Línea de datos serie |
| SCL | Reloj I2C | Línea de reloj serie |

## 📏 Dimensiones

![Dimensiones](unit_dimension_v_1_0_0_icp10111_barometric_pressure_sensor.png)

## 📃 Topología

![Topología](unit_topology_v_1_0_0_icp10111_barometric_pressure_sensor.png)

| Ref. | Descripción |
|------|-------------|
| IC1 | Sensor de Presión Barométrica ICP-10111 |
| IC2 | Sensor Ambiental BME688 |
| L1 | LED de Encendido |
| U1 | Regulador ME6206A18XG 1.8V | 
| JP1 | Orificios Castellanos de 2.54 mm |
| J1 | Conector QWIIC (JST paso 1 mm) para I2C |
## Interfaces de Comunicación

### Interfaz I2C
- **Dirección**: 0x63 (ICP-10111), 0x77 (BME688)
- **Velocidad**: Estándar (100 kHz), Rápido (400 kHz)
- **Características**: Conector compatible QWIIC
- **Resistencias Pull-up**: 4.7kΩ integradas

### Especificaciones de Interfaz Digital
- **Niveles Lógicos**: Compatible CMOS 3.3V
- **Entrada Alta**: 2.0V mínimo
- **Entrada Baja**: 0.8V máximo
- **Corriente de Salida**: 4mA típico

## Características Físicas

### Información del Encapsulado

| Parámetro | Valor | Unidad |
|-----------|-------|--------|
| Tipo de Encapsulado | PCB Personalizado | - |
| Dimensiones | 25.4 x 15.24 x 3.2 | mm |
| Montaje | Orificios castellanos | Paso 2.54mm |
| Peso | 2.1 | g |

### Especificaciones Ambientales

| Parámetro | Mín | Máx | Unidad | Condiciones |
|-----------|-----|-----|--------|-------------|
| Temperatura de Operación | -40 | +85 | °C | Precisión completa |
| Temperatura de Almacenamiento | -55 | +125 | °C | - |
| Humedad | 0 | 100 | %HR | Sin condensación |
| Rango de Presión | 300 | 1250 | hPa | Presión absoluta |

## Soporte de Software

### Entorno de Desarrollo
- **Arduino IDE**: Soporte completo de librería
- **ESP-IDF**: Integración de driver nativo
- **PlatformIO**: Soporte multiplataforma
- **CircuitPython**: Librería Python disponible

### Librerías Principales
- Driver del sensor de presión ICP-10111
- Librería del sensor ambiental BME688
- Protocolos de comunicación I2C
- Filtrado y calibración de datos

## Aplicaciones

El módulo ICP-10111 es ideal para:

1. **Monitoreo Meteorológico**
   - Medición de presión atmosférica
   - Determinación de altitud
   - Sistemas de predicción meteorológica

2. **Sensores Ambientales IoT**
   - Automatización de edificios inteligentes
   - Monitoreo agrícola
   - Evaluación de calidad del aire

3. **Dispositivos Portátiles**
   - Rastreadores de fitness
   - Dispositivos de navegación al aire libre
   - Control de altitud de drones

## Seguridad y Cumplimiento

### Certificaciones
- **RoHS**: Cumple con directiva de la UE
- **REACH**: Cumple con regulación de la UE
- **CE**: Compatibilidad electromagnética

### Características de Seguridad
- **Protección ESD**: ±2kV HBM en todos los pines
- **Protección de Polaridad Inversa**: Integrada
- **Protección Térmica**: Monitoreo de rango de operación

## Referencias

- [Hoja de Datos ICP-10111](https://product.tdk.com/system/files/dam/doc/product/sensor/pressure/capacitive-pressure/data_sheet/ds-000177-icp-10111-v1.3.pdf)
- [Hoja de Datos BME688](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme688-ds000.pdf)
- [Hoja de Datos Regulador ME6206](https://www.microne.com.cn/uploads/file/20200904/ME6206.pdf)

## Información de Pedidos

| Número de Parte | Descripción | Empaque | MOQ |
|-----------------|-------------|---------|-----|
| ICP10111-001 | Módulo Estándar | Individual | 1 |
| ICP10111-DEV | Kit de Desarrollo | Caja de Kit | 1 |
| ICP10111-BULK | Pedido en Lote | Bandeja | 100 |

## Características Físicas

![Dimensiones Físicas](resources/unit_dimension_v_1_0_0_icp10111_barometric_pressure_sensor.png)

![Vista Superior](resources/unit_top_v_1_0_0_icp10111_barometric_pressure_sensor.png)

![Vista Inferior](resources/unit_btm_v_1_0_0_icp10111_barometric_pressure_sensor.png)

### Información del Encapsulado

| Parámetro | Valor | Unidad |
|-----------|-------|--------|
| Tipo de Encapsulado | QFN-48 | - |
| Dimensiones | 6 x 6 x 0.9 | mm |
| Separación de Pines | 0.4 | mm |
| Peso | 0.5 | g |

### Especificaciones Ambientales

| Parámetro | Mín | Máx | Unidad | Condiciones |
|-----------|-----|-----|--------|-------------|
| Temperatura de Operación | -40 | +85 | °C | Grado comercial |
| Temperatura de Almacenamiento | -55 | +125 | °C | - |
| Humedad | 10 | 95 | %HR | Sin condensación |

## Soporte de Software

### Entorno de Desarrollo
- **Arduino IDE**: Soporte completo con núcleo ESP32
- **ESP-IDF**: Framework nativo de Espressif
- **PlatformIO**: Soporte IDE multiplataforma
- **MicroPython**: Soporte Python para desarrollo rápido

### Librerías Principales
- Conectividad WiFi & Bluetooth
- Sistema operativo en tiempo real FreeRTOS
- Capa de abstracción de hardware (HAL)
- Soporte de actualización por aire (OTA)

## Aplicaciones

El módulo DevLab es ideal para:

1. **Sensores y Actuadores IoT**
   - Monitoreo ambiental
   - Dispositivos domóticos
   - Automatización industrial

2. **Prototipado y Desarrollo**
   - Pruebas de concepto rápidas
   - Proyectos educativos
   - Aplicaciones de investigación

3. **Productos Comerciales**
   - Electrodomésticos inteligentes
   - Dispositivos vestibles
   - Iluminación conectada

## Seguridad y Cumplimiento

### Certificaciones
- **FCC**: Parte 15.247 (USA)
- **CE**: EN 300 328, EN 301 489 (Europa)
- **IC**: RSS-210 (Canadá)

### Características de Seguridad
- **Protección ESD**: ±2kV HBM en todos los pines
- **Inmunidad Latch-up**: ±100mA
- **Protección Térmica**: Apagado térmico automático

## Información de Pedidos

| Número de Parte | Descripción | Empaque | MOQ |
|-----------------|-------------|---------|-----|
| DEVLAB-001 | Módulo Estándar | Bandeja | 100 |
| DEVLAB-001R | Compatible RoHS | Tape & Reel | 1000 |
| DEVLAB-DEV | Kit de Desarrollo | Caja Individual | 1 |

## Historial de Revisiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2025-07-18 | Lanzamiento inicial |

## Esquemáticos

![Esquemático del Circuito](resources/Schematics_icon.jpg)

---

*Para soporte técnico e información adicional, visita nuestro sitio web o contacta a nuestro equipo de ingeniería.*
