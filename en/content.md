# DevLab Overview

DevLab is a compact embedded module with Wi-Fi and Bluetooth capabilities, designed for IoT applications and rapid prototyping.

## Features

- **Dual-core microcontroller** (240 MHz)
- **Up to 27 GPIOs** configurable
- **Integrated wireless support** (Wi-Fi & Bluetooth)
- **Low power consumption** modes
- **Extensive peripheral support**

## Technical Specifications

![System Topology](resources/unit_topology_v_1_0_0_icp10111_barometric_pressure_sensor.png)

### Processor & Memory

| Parameter | Value | Unit | Notes |
|-----------|-------|------|-------|
| CPU | Dual-core Xtensa LX6 | 240 MHz | 32-bit RISC |
| Flash Memory | 4 MB | MB | External SPI Flash |
| SRAM | 520 KB | KB | Internal SRAM |
| RTC Memory | 16 KB | KB | Ultra Low Power |

### Power Specifications

| Parameter | Min | Typ | Max | Unit | Conditions |
|-----------|-----|-----|-----|------|------------|
| Supply Voltage | 2.2 | 3.3 | 3.6 | V | Normal Operation |
| Active Current | - | 160 | 260 | mA | Wi-Fi Tx @ 19.5dBm |
| Sleep Current | - | 5 | 10 | µA | Deep Sleep Mode |
| Standby Current | - | 240 | 350 | µA | Light Sleep Mode |

### Wireless Capabilities

#### Wi-Fi Specifications
- **Standards**: 802.11 b/g/n (2.4 GHz)
- **Data Rate**: Up to 150 Mbps
- **Output Power**: +19.5 dBm max
- **Antenna**: Integrated PCB antenna

#### Bluetooth Specifications
- **Version**: Bluetooth v4.2 BR/EDR and BLE
- **Output Power**: +9 dBm max
- **Range**: Up to 100m (open field)

## GPIO Configuration

![Pinout Diagram](resources/unit_pinout_v_0_0_1_ue0094_icp10111_barometric_pressure_sensor_en.png)

### Available Pins

| Pin | Function | Voltage | Drive Current | Special Features |
|-----|----------|---------|---------------|------------------|
| GPIO0 | Digital I/O | 3.3V | 40 mA | Boot control |
| GPIO1 | UART0_TXD | 3.3V | 40 mA | Default debug output |
| GPIO2 | Digital I/O | 3.3V | 40 mA | LED control |
| GPIO3 | UART0_RXD | 3.3V | - | Default debug input |
| GPIO4-5 | Digital I/O | 3.3V | 40 mA | General purpose |

### ADC Capabilities

The module includes a 12-bit SAR ADC with the following characteristics:

- **Resolution**: 12-bit (4096 levels)
- **Input Range**: 0 - 3.3V
- **Channels**: 8 channels available
- **Sampling Rate**: Up to 2 Msps

## Communication Interfaces

### UART
- **Channels**: 3 hardware UART controllers
- **Baud Rate**: Up to 5 Mbps
- **Features**: Hardware flow control, DMA support

### SPI
- **Channels**: 4 SPI controllers
- **Speed**: Up to 80 MHz
- **Modes**: Master/Slave operation
- **Features**: DMA support, flexible pin mapping

### I2C
- **Channels**: 2 I2C controllers  
- **Speed**: Standard (100 kHz), Fast (400 kHz), Fast+ (1 MHz)
- **Features**: Multi-master support, 7/10-bit addressing

## Physical Characteristics

![Physical Dimensions](resources/unit_dimension_v_1_0_0_icp10111_barometric_pressure_sensor.png)

![Top View](resources/unit_top_v_1_0_0_icp10111_barometric_pressure_sensor.png)

![Bottom View](resources/unit_btm_v_1_0_0_icp10111_barometric_pressure_sensor.png)

### Package Information

| Parameter | Value | Unit |
|-----------|-------|------|
| Package Type | QFN-48 | - |
| Dimensions | 6 x 6 x 0.9 | mm |
| Pin Pitch | 0.4 | mm |
| Weight | 0.5 | g |

### Environmental Specifications

| Parameter | Min | Max | Unit | Conditions |
|-----------|-----|-----|------|------------|
| Operating Temperature | -40 | +85 | °C | Commercial grade |
| Storage Temperature | -55 | +125 | °C | - |
| Humidity | 10 | 95 | %RH | Non-condensing |

## Software Support

### Development Environment
- **Arduino IDE**: Full support with ESP32 core
- **ESP-IDF**: Native Espressif framework
- **PlatformIO**: Cross-platform IDE support
- **MicroPython**: Python support for rapid development

### Key Libraries
- WiFi & Bluetooth connectivity
- FreeRTOS real-time operating system
- Hardware abstraction layer (HAL)
- Over-the-air (OTA) update support

## Applications

The DevLab module is ideal for:

1. **IoT Sensors & Actuators**
   - Environmental monitoring
   - Smart home devices
   - Industrial automation

2. **Prototyping & Development**
   - Rapid proof-of-concept
   - Educational projects
   - Research applications

3. **Commercial Products**
   - Smart appliances
   - Wearable devices
   - Connected lighting

## Safety & Compliance

### Certifications
- **FCC**: Part 15.247 (USA)
- **CE**: EN 300 328, EN 301 489 (Europe)
- **IC**: RSS-210 (Canada)

### Safety Features
- **ESD Protection**: ±2kV HBM on all pins
- **Latch-up Immunity**: ±100mA
- **Thermal Protection**: Automatic thermal shutdown

## Ordering Information

| Part Number | Description | Package | MOQ |
|-------------|-------------|---------|-----|
| DEVLAB-001 | Standard Module | Tray | 100 |
| DEVLAB-001R | RoHS Compliant | Tape & Reel | 1000 |
| DEVLAB-DEV | Development Kit | Individual Box | 1 |

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-07-18 | Initial release |

## Schematics

![Circuit Schematic](resources/Schematics_icon.jpg)

---

*For technical support and additional information, visit our website or contact our engineering team.*
