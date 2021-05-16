sudo apt-get -y update

# Kafka
```

bin/zookeeper-server-start.sh -daemon config/zookeeper.properties
bin/kafka-server-start.sh -daemon config/server.properties
bin/kafka-topics.sh --create --topic vehicle-events --bootstrap-server localhost:9092
```

# MongoDB / Elasticsearch / Kibana
```

docker-compose up -d # (Re)Crear y subir contenedores.
docker-compose start # Subir contenedores.
docker-compose stop # Parar contenedores.
```


# Arrancar mondodb_consumer.py en background
```
python mongodb_consumer.py 2>&1 > /dev/null &
```

# Mirar indice en Elasticsearch.
```
curl -XGET http://localhost:9200/_cat/indices/vehicle-events
```

# Logstash
# Descargar, instalar, y agregar configuracion del pipeline.
```
wget https://artifacts.elastic.co/downloads/logstash/logstash-7.12.1-linux-x86_64.tar.gz
tar xvf logstash-7.12.1-linux-x86_64.tar.gz
rm logstash-7.12.1-linux-x86_64.tar.gz
cp logstash-kafka.conf logstash-7.12.1/conf/
```

# Iniciar logstash en background.
```
cd logstash-7.12.1
bin/logstash -f config/logstash-kafka.conf 2>&1 > /dev/null &
```

# Implementación de API-REST con flask
Con el fin de proveer un punto de comunicación entre los
dispositivos de monitoreo y kafka, se propone implementar una 
api que exponga un endpoint accesible por medio del protocolo HTTP. 
Utilizamos el framework de python llamado flask para dicho implementación gracias 
a su versatilidad y fácil configuración.

El primer paso es instaciar una máquina EC2 t2.medium con Ubuntu 20, con acceso al puerto 80. Luego de esto,
procedemos a instalar los requerimientos, en este caso python y NGINX para redirigir
la aplicación al puerto 80.
```
sudo apt-get -y install python3 python3-venv python3-dev
sudo apt-get -y install nginx
```

Luego, estando en el directorio del proyecto, procedemos a crear un ambiente virtual
de python y a instalar allí todas las dependencias:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Luego de esto, podemos verificar que el servicio se pueda ejecutar sin problemas,
simplemente corriendo:
```
python app.py
```
Una vez verificado esto, configuramos NGINX para que redirija la aplicación de
localhost:8080 al puerto 80, para que sea publicamente visible y accesible 
a los dispositivos.
```
sudo nano /etc/systemd/system/app.service
```
Copiamos allí el contenido de app.service y guardamos. Luego:
```
sudo systemctl start app
sudo systemctl enable app
sudo nano /etc/nginx/sites-available/app
```
Copiamos el contenido de sites_available_app y guardamos. Luego:
```
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled
sudo rm -r /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```
Verificamos que todo este funcionando correctamente mediante:
```
sudo systemctl status app
sudo systemctl status nginx
```

# Configuración de dispositivo de monitoreo
El OVMS se configura mediante un archivo de configuración en javascript el cual 
se encuentra como ovms_vehicle.js. Allí básicamente se leen diferentes variables
del vehículo y se añaden como query parameters a la url del servicio de flask. 
Se configura para que cada 8 segundos haga el envío de información.

# Para cargar cambios en la aplicación:
```
git pull
sudo systemctl restart app
```

