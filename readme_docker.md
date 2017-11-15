### Docker de la base de datos ###
#       'NAME': 'radarsys',
#       'USER': 'developer',
#       'PASSWORD': 'idi2015',

#Preparar Base de Datos para la aplicacion:
## Crear imagen "mysql:5.6"
docker create -v /var/lib/mysql --name mysql-radarsys-data mysql:5.6 /bin/true
## Ejecutar Container "mysql-radarsys-server"
docker run --name mysql-radarsys-server -d -e MYSQL_ROOT_PASSWORD=r00tJRO -e MYSQL_DATABASE=radarsys \
          -e MYSQL_USER=developer -e MYSQL_PASSWORD=idi2015 --volumes-from mysql-radarsys-data mysql:5.6

#Aplicacion Sistema Integrado de Radar
## Debe crearse *Dockerfile*
## Crear la imagen
docker build  -t radarsys:v01 .
# Ejecutar Container
docker run -d --name radarsys01 --link mysql-radarsys-server -p 3000:3000 \
-v /home/ubuntu/docker_shared/radarsys/media:/radarsys/media \
--add-host smtp_server:172.17.0.1  radarsys:v01

## Dentro del Container: se debe realizar las siguiente modificaciones
### Es necesario ejecutar: 
	apt-get update
	apt-get install nano
### Modificar radarsys.setting.py, HOST debe estar habilitado
	'HOST': 'mysql-sysinv-server', 
### Asegurarse que:
	MEDIA_ROOT: 'media'
### En el script abs/utils/Graphics_OverJro.py, matplotlib Agg debe estar habilitado
	matplotlib.use("Agg")

### Ejecutar los siguientes comandos (solo si ya se creo mysql-radarsys-server):
 python manage.py makemigrations \
 && python manage.py migrate \
 && python manage.py loaddata apps/main/fixtures/main_initial_data.json \
 && python manage.py loaddata apps/rc/fixtures/rc_initial_data.json \
 && python manage.py loaddata apps/jars/fixtures/initial_filters_data.json \
 && python manage.py collectstatic

### Por ultimo reiniciar el docker
	docker stop radarsys01
	docker start radarsys01


####  Archivos Compartidos:
# /home/ubuntu/docker_shared/radarsys/media
# (debe coincidir con la carpeta que se ingresar en "docker run")
