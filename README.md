# Taller-tarea-3
## Paso 1
### Instalar docker Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg lsb-release

# Agrega la clave GPG oficial de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/$(. /etc/os-release && echo "$ID")/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Agrega el repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$(. /etc/os-release && echo "$ID") \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instala Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verifica instalación
sudo docker version

```
### Arch Linux / Manjaro
```bash
sudo pacman -Syu docker

# Habilita e inicia el servicio
sudo systemctl enable --now docker

# Verifica instalación
docker version

```
### Fedora
```bash
sudo dnf install -y dnf-plugins-core

# Agrega el repositorio
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# Instala Docker
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Inicia Docker
sudo systemctl enable --now docker

# Verifica instalación
docker version

```
### Creación de contenedor FTP (PureFTP)
```bash
# Creación del contenedor
docker run -d --name ftpd_server -p 21:21 -p 30000-30009:30000-30009 -e "PUBLICHOST=localhost" -e "ADDED_FLAGS=-d -d" stilliard/pure-ftpd:hardened

# Ejecución
docker exec -it ftpd_server sh -c "export TERM=xterm && bash"

# Creación de usuario
pure-pw useradd bob -f /etc/pure-ftpd/passwd/pureftpd.passwd -m -u ftpuser -d /home/ftpusers/bob

```
### Creación de contenedor cliente (lFTP)
```bash
# Creación y ejecución
sudo docker run -it ubuntu

# Instalación de lFTP
apt install lftp

# Iniciar sesión
lftp ftp://bob:1234@172.17.0.2

```
### Creación de contenedor Scapy
```bash
docker run --rm -it \
  --network=host \
  --cap-add=NET_ADMIN \
  --cap-add=NET_RAW \
  -v $(pwd):/code \ # Modificar a la carpeta donde se encuentren los scripts
  --name scapy_test \
  scapy-env

```
### Uso de sniffer
Una vez dentro del contenedor con scapy ejecutar, leera los paquetes TCP y FTP
```bash
python3 sniff.py
```
### Uso de fuzz 1
```bash
python3 fuzz1.py
```
### Uso de fuzz 2
```bash
python3 fuzz2.py
```
### Uso de modify
En una terminal aparte, ejecutar modify.py
```bash
python3 modify.py
```
Es necesario que los 3 contenedores y sniff.py y modify.py estén corriendo, el script modify.py esta configurado para usar de referencia el archivo documento.txt.
1. Una vez preparado el entorno, se envia un archivo al server mediante el comando PUT.
2. Automáticamente sniff.py lo va a detectar, esperar hasta que no haya ningun mensaje entrante.
3. El último mensaje en pantalla de sniff.py es el que hay que usar.
4. Se ejecuta modify.py, y se rellena con los datos que necesita (puerto, ACK, SEQ, length).
5. Opcional: usar wireshark con la interfaz docker0.
