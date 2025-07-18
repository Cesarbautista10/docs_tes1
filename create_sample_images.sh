# Imagen de ejemplo para testing
# Esta es una imagen placeholder que se puede reemplazar con diagramas reales
echo "P3 100 100 255" > /media/mr/firmware/personal/docs_tes1/images/sample.ppm
for i in {1..100}; do
  for j in {1..100}; do
    echo "$((i*2 % 256)) $((j*2 % 256)) $((i*j % 256))"
  done
done >> /media/mr/firmware/personal/docs_tes1/images/sample.ppm

# Convertir a PNG si imagemagick está disponible
if command -v convert &> /dev/null; then
  convert /media/mr/firmware/personal/docs_tes1/images/sample.ppm /media/mr/firmware/personal/docs_tes1/images/sample.png
  rm /media/mr/firmware/personal/docs_tes1/images/sample.ppm
fi
