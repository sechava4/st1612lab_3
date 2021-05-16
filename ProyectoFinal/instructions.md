# Algunos Comandos Útiles
# Kafka

    bin/zookeeper-server-start.sh -daemon config/zookeeper.properties
    bin/kafka-server-start.sh -daemon config/server.properties
    bin/kafka-topics.sh --create --topic vehicle-events --bootstrap-server localhost:9092

# MongoDB / Elasticsearch / Kibana en Docker Compose

    docker-compose up -d # (Re)Crear y subir contenedores.
    docker-compose start # Subir contenedores.
    docker-compose stop # Parar contenedores.

# Arrancar mondodb_consumer.py en background

    python mongodb_consumer.py 2>&1 > /dev/null &

# Mirar indice en Elasticsearch.

    curl -XGET http://localhost:9200/_cat/indices/vehicle-events

# Logstash - Descargar, instalar, y agregar configuracion del pipeline.

    wget https://artifacts.elastic.co/downloads/logstash/logstash-7.12.1-linux-x86_64.tar.gz
    tar xvf logstash-7.12.1-linux-x86_64.tar.gz
    rm logstash-7.12.1-linux-x86_64.tar.gz
    cp logstash-kafka.conf logstash-7.12.1/conf/

# Iniciar logstash en background.

    cd logstash-7.12.1
    bin/logstash -f config/logstash-kafka.conf 2>&1 > /dev/null &


# Python3 y Nginx

    sudo apt-get -y install python3 python3-venv python3-dev
    sudo apt-get -y install nginx

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

# Servicio Rest

    sudo nano /etc/systemd/system/app.service
    sudo systemctl start app
    sudo systemctl enable app
    sudo nano /etc/nginx/sites-available/app
    sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled
    sudo rm -r /etc/nginx/sites-enabled/default
    sudo nginx -t
    sudo systemctl restart nginx

# Para cargar cambios en la aplicación:

    git pull
    sudo systemctl restart app
