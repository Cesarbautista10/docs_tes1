# Introducción a DevLab

DevLab es un módulo embebido compacto con capacidades de Wi-Fi y Bluetooth, diseñado para aplicaciones IoT y prototipado rápido.

## Características Principales

- **Microcontrolador de doble núcleo** (240 MHz)
- **Hasta 27 GPIOs** configurables
- **Soporte inalámbrico integrado** (Wi-Fi & Bluetooth)
- **Modos de bajo consumo** energético
- **Amplio soporte de periféricos**

## Especificaciones Técnicas

![Topología del Sistema](resources/unit_topology_v_1_0_0_icp10111_barometric_pressure_sensor.png)

### Procesador y Memoria

| Parámetro | Valor | Unidad | Notas |
|-----------|-------|--------|-------|
| CPU | Dual-core Xtensa LX6 | 240 MHz | RISC de 32-bit |
| Memoria Flash | 4 MB | MB | SPI Flash externa |
| SRAM | 520 KB | KB | SRAM interna |
| Memoria RTC | 16 KB | KB | Ultra Bajo Consumo |

### Especificaciones de Alimentación

| Parámetro | Mín | Típ | Máx | Unidad | Condiciones |
|-----------|-----|-----|-----|--------|-------------|
| Voltaje de Alimentación | 2.2 | 3.3 | 3.6 | V | Operación Normal |
| Corriente Activa | - | 160 | 260 | mA | Wi-Fi Tx @ 19.5dBm |
| Corriente en Reposo | - | 5 | 10 | µA | Modo Sleep Profundo |
| Corriente Standby | - | 240 | 350 | µA | Modo Light Sleep |

### Capacidades Inalámbricas

#### Especificaciones Wi-Fi
- **Estándares**: 802.11 b/g/n (2.4 GHz)
- **Velocidad de Datos**: Hasta 150 Mbps
- **Potencia de Salida**: +19.5 dBm máx
- **Antena**: Antena PCB integrada

#### Especificaciones Bluetooth
- **Versión**: Bluetooth v4.2 BR/EDR y BLE
- **Potencia de Salida**: +9 dBm máx
- **Alcance**: Hasta 100m (campo abierto)

## Configuración GPIO

![Diagrama de Pines](resources/unit_pinout_v_0_0_1_ue0094_icp10111_barometric_pressure_sensor_es.png)

### Pines Disponibles

| Pin | Función | Voltaje | Corriente | Características Especiales |
|-----|---------|---------|-----------|----------------------------|
| GPIO0 | E/S Digital | 3.3V | 40 mA | Control de arranque |
| GPIO1 | UART0_TXD | 3.3V | 40 mA | Salida debug por defecto |
| GPIO2 | E/S Digital | 3.3V | 40 mA | Control de LED |
| GPIO3 | UART0_RXD | 3.3V | - | Entrada debug por defecto |
| GPIO4-5 | E/S Digital | 3.3V | 40 mA | Propósito general |

### Capacidades ADC

El módulo incluye un ADC SAR de 12-bit con las siguientes características:

- **Resolución**: 12-bit (4096 niveles)
- **Rango de Entrada**: 0 - 3.3V
- **Canales**: 8 canales disponibles
- **Velocidad de Muestreo**: Hasta 2 Msps

## Interfaces de Comunicación

### UART
- **Canales**: 3 controladores UART por hardware
- **Velocidad**: Hasta 5 Mbps
- **Características**: Control de flujo por hardware, soporte DMA

### SPI
- **Canales**: 4 controladores SPI
- **Velocidad**: Hasta 80 MHz
- **Modos**: Operación Maestro/Esclavo
- **Características**: Soporte DMA, mapeo flexible de pines

### I2C
- **Canales**: 2 controladores I2C
- **Velocidad**: Estándar (100 kHz), Rápido (400 kHz), Rápido+ (1 MHz)
- **Características**: Soporte multi-maestro, direccionamiento 7/10-bit

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
