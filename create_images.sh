#!/bin/bash

# Script para crear imágenes de ejemplo para la documentación
cd /media/mr/firmware/personal/docs_tes1/images

echo "Creando imágenes de ejemplo..."

# Crear imagen de pinout usando SVG y convertir a PNG
cat > pinout_diagram.svg << 'EOF'
<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="300" fill="#f0f0f0" stroke="#000" stroke-width="2"/>
  <text x="200" y="30" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">DevLab Module Pinout</text>
  
  <!-- Módulo principal -->
  <rect x="150" y="80" width="100" height="120" fill="#333" stroke="#000" stroke-width="2"/>
  <text x="200" y="140" text-anchor="middle" fill="white" font-family="Arial" font-size="12">DevLab</text>
  <text x="200" y="155" text-anchor="middle" fill="white" font-family="Arial" font-size="10">ESP32</text>
  
  <!-- Pines izquierda -->
  <line x1="130" y1="90" x2="150" y2="90" stroke="#000" stroke-width="2"/>
  <text x="125" y="95" text-anchor="end" font-family="Arial" font-size="10">GPIO0</text>
  
  <line x1="130" y1="110" x2="150" y2="110" stroke="#000" stroke-width="2"/>
  <text x="125" y="115" text-anchor="end" font-family="Arial" font-size="10">GPIO1</text>
  
  <line x1="130" y1="130" x2="150" y2="130" stroke="#000" stroke-width="2"/>
  <text x="125" y="135" text-anchor="end" font-family="Arial" font-size="10">GPIO2</text>
  
  <line x1="130" y1="150" x2="150" y2="150" stroke="#000" stroke-width="2"/>
  <text x="125" y="155" text-anchor="end" font-family="Arial" font-size="10">3V3</text>
  
  <line x1="130" y1="170" x2="150" y2="170" stroke="#000" stroke-width="2"/>
  <text x="125" y="175" text-anchor="end" font-family="Arial" font-size="10">GND</text>
  
  <!-- Pines derecha -->
  <line x1="250" y1="90" x2="270" y2="90" stroke="#000" stroke-width="2"/>
  <text x="275" y="95" font-family="Arial" font-size="10">GPIO4</text>
  
  <line x1="250" y1="110" x2="270" y2="110" stroke="#000" stroke-width="2"/>
  <text x="275" y="115" font-family="Arial" font-size="10">GPIO5</text>
  
  <line x1="250" y1="130" x2="270" y2="130" stroke="#000" stroke-width="2"/>
  <text x="275" y="135" font-family="Arial" font-size="10">RX</text>
  
  <line x1="250" y1="150" x2="270" y2="150" stroke="#000" stroke-width="2"/>
  <text x="275" y="155" font-family="Arial" font-size="10">TX</text>
  
  <line x1="250" y1="170" x2="270" y2="170" stroke="#000" stroke-width="2"/>
  <text x="275" y="175" font-family="Arial" font-size="10">EN</text>
  
  <!-- Antena -->
  <path d="M 210 80 Q 230 70 250 80" stroke="#666" stroke-width="2" fill="none"/>
  <text x="230" y="65" text-anchor="middle" font-family="Arial" font-size="8">WiFi/BT</text>
</svg>
EOF

# Crear imagen de diagrama de bloques
cat > block_diagram.svg << 'EOF'
<svg width="500" height="350" xmlns="http://www.w3.org/2000/svg">
  <rect width="500" height="350" fill="white" stroke="#000" stroke-width="1"/>
  <text x="250" y="25" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">DevLab Block Diagram</text>
  
  <!-- CPU -->
  <rect x="200" y="50" width="100" height="60" fill="#ffeeaa" stroke="#000" stroke-width="2"/>
  <text x="250" y="75" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold">ESP32</text>
  <text x="250" y="90" text-anchor="middle" font-family="Arial" font-size="10">Dual Core</text>
  <text x="250" y="105" text-anchor="middle" font-family="Arial" font-size="10">240MHz</text>
  
  <!-- Flash -->
  <rect x="50" y="70" width="80" height="40" fill="#ccccff" stroke="#000" stroke-width="2"/>
  <text x="90" y="90" text-anchor="middle" font-family="Arial" font-size="11">Flash</text>
  <text x="90" y="105" text-anchor="middle" font-family="Arial" font-size="9">4MB</text>
  
  <!-- WiFi/BT -->
  <rect x="370" y="70" width="80" height="40" fill="#ffcccc" stroke="#000" stroke-width="2"/>
  <text x="410" y="85" text-anchor="middle" font-family="Arial" font-size="10">WiFi/BT</text>
  <text x="410" y="100" text-anchor="middle" font-family="Arial" font-size="9">2.4GHz</text>
  
  <!-- GPIO -->
  <rect x="200" y="150" width="100" height="40" fill="#ccffcc" stroke="#000" stroke-width="2"/>
  <text x="250" y="175" text-anchor="middle" font-family="Arial" font-size="11">GPIO</text>
  <text x="250" y="185" text-anchor="middle" font-family="Arial" font-size="9">27 pins</text>
  
  <!-- Periféricos -->
  <rect x="50" y="220" width="60" height="30" fill="#ffffcc" stroke="#000" stroke-width="1"/>
  <text x="80" y="240" text-anchor="middle" font-family="Arial" font-size="9">UART</text>
  
  <rect x="130" y="220" width="60" height="30" fill="#ffffcc" stroke="#000" stroke-width="1"/>
  <text x="160" y="240" text-anchor="middle" font-family="Arial" font-size="9">SPI</text>
  
  <rect x="210" y="220" width="60" height="30" fill="#ffffcc" stroke="#000" stroke-width="1"/>
  <text x="240" y="240" text-anchor="middle" font-family="Arial" font-size="9">I2C</text>
  
  <rect x="290" y="220" width="60" height="30" fill="#ffffcc" stroke="#000" stroke-width="1"/>
  <text x="320" y="240" text-anchor="middle" font-family="Arial" font-size="9">ADC</text>
  
  <rect x="370" y="220" width="60" height="30" fill="#ffffcc" stroke="#000" stroke-width="1"/>
  <text x="400" y="240" text-anchor="middle" font-family="Arial" font-size="9">PWM</text>
  
  <!-- Conexiones -->
  <line x1="130" y1="90" x2="200" y2="80" stroke="#000" stroke-width="2"/>
  <line x1="300" y1="90" x2="370" y2="90" stroke="#000" stroke-width="2"/>
  <line x1="250" y1="110" x2="250" y2="150" stroke="#000" stroke-width="2"/>
  
  <!-- Conexiones a periféricos -->
  <line x1="220" y1="190" x2="80" y2="220" stroke="#666" stroke-width="1"/>
  <line x1="230" y1="190" x2="160" y2="220" stroke="#666" stroke-width="1"/>
  <line x1="240" y1="190" x2="240" y2="220" stroke="#666" stroke-width="1"/>
  <line x1="250" y1="190" x2="320" y2="220" stroke="#666" stroke-width="1"/>
  <line x1="280" y1="190" x2="400" y2="220" stroke="#666" stroke-width="1"/>
  
  <!-- Power -->
  <rect x="200" y="280" width="100" height="30" fill="#ffdddd" stroke="#000" stroke-width="2"/>
  <text x="250" y="300" text-anchor="middle" font-family="Arial" font-size="11">Power: 3.3V</text>
</svg>
EOF

# Crear imagen de dimensiones físicas
cat > physical_dimensions.svg << 'EOF'
<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="300" fill="white" stroke="#000" stroke-width="1"/>
  <text x="200" y="25" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">Physical Dimensions</text>
  
  <!-- Módulo principal -->
  <rect x="150" y="100" width="100" height="100" fill="#e0e0e0" stroke="#000" stroke-width="2"/>
  
  <!-- Dimensiones -->
  <!-- Ancho -->
  <line x1="150" y1="80" x2="250" y2="80" stroke="#000" stroke-width="1" marker-end="url(#arrowhead)"/>
  <line x1="250" y1="80" x2="150" y2="80" stroke="#000" stroke-width="1" marker-end="url(#arrowhead)"/>
  <text x="200" y="75" text-anchor="middle" font-family="Arial" font-size="12">6.0 mm</text>
  
  <!-- Alto -->
  <line x1="130" y1="100" x2="130" y2="200" stroke="#000" stroke-width="1" marker-end="url(#arrowhead)"/>
  <line x1="130" y1="200" x2="130" y2="100" stroke="#000" stroke-width="1" marker-end="url(#arrowhead)"/>
  <text x="110" y="150" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-90 110 150)">6.0 mm</text>
  
  <!-- Pines -->
  <circle cx="165" cy="115" r="2" fill="#333"/>
  <circle cx="175" cy="115" r="2" fill="#333"/>
  <circle cx="185" cy="115" r="2" fill="#333"/>
  <text x="175" y="135" text-anchor="middle" font-family="Arial" font-size="8">0.4mm pitch</text>
  
  <!-- Grosor -->
  <text x="200" y="230" text-anchor="middle" font-family="Arial" font-size="12">Thickness: 0.9 mm</text>
  <text x="200" y="250" text-anchor="middle" font-family="Arial" font-size="12">Package: QFN-48</text>
  
  <!-- Definir marcadores de flecha -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>
EOF

echo "Convirtiendo SVG a PNG..."

# Convertir SVG a PNG si rsvg-convert está disponible
if command -v rsvg-convert &> /dev/null; then
    rsvg-convert -w 800 -h 600 pinout_diagram.svg -o pinout_diagram.png
    rsvg-convert -w 800 -h 600 block_diagram.svg -o block_diagram.png
    rsvg-convert -w 800 -h 600 physical_dimensions.svg -o physical_dimensions.png
    rm *.svg
    echo "✓ Imágenes PNG creadas"
elif command -v inkscape &> /dev/null; then
    inkscape pinout_diagram.svg --export-png=pinout_diagram.png --export-width=800
    inkscape block_diagram.svg --export-png=block_diagram.png --export-width=800
    inkscape physical_dimensions.svg --export-png=physical_dimensions.png --export-width=800
    rm *.svg
    echo "✓ Imágenes PNG creadas con Inkscape"
elif command -v convert &> /dev/null; then
    # ImageMagick puede manejar SVG pero necesita librsvg
    convert pinout_diagram.svg pinout_diagram.png
    convert block_diagram.svg block_diagram.png
    convert physical_dimensions.svg physical_dimensions.png
    rm *.svg
    echo "✓ Imágenes PNG creadas con ImageMagick"
else
    echo "⚠ No se encontró rsvg-convert, inkscape o imagemagick."
    echo "⚠ Manteniendo archivos SVG (también funcionan en LaTeX)"
fi

echo "Imágenes de ejemplo creadas en el directorio images/"
ls -la
