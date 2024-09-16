# Detener y eliminar el contenedor y las imágenes del servicio
docker compose down --rmi all --volumes --remove-orphans

# Volver a crear y levantar los servicios
docker compose -p "" up -d --build