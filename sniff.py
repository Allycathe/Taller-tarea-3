from scapy.all import *
import re

INTERFAZ = "docker0"
contador = 1
COMANDOS_FTP = [
    'USER', 'PASS', 'RETR', 'STOR', 'QUIT',
    'PWD', 'CWD', 'LIST', 'PORT', 'PASV', 'TYPE'
]

def identificar_comando(payload):
    try:
        linea = payload.decode(errors='ignore').strip()
        for cmd in COMANDOS_FTP:
            if linea.upper().startswith(cmd):
                return f"Comando {cmd}"
        if re.match(r"^\d{3}", linea):
            return f"Respuesta FTP: {linea[:3]}"
    except:
        pass
    return None

def mostrar(pkt):
    global contador
    if IP in pkt and TCP in pkt:
        descripcion = ""
        payload_len = 0
        mostrar = True  # Ahora mostramos todo lo que sea TCP

        if Raw in pkt:
            raw = pkt[Raw].load
            payload_len = len(raw)
            comando = identificar_comando(raw)
            if comando:
                descripcion = f"FTP: {comando}"
            else:
                descripcion = "TCP con payload (no FTP)"
        else:
            descripcion = "TCP sin payload (ACK, SYN, etc.)"

        print(f"\nPaquete capturado: {contador}")
        print("=" * 21)
        print(f"MAC origen: {pkt[Ether].src}")
        print(f"MAC destino: {pkt[Ether].dst}")
        print(f"IP origen: {pkt[IP].src}")
        print(f"IP destino: {pkt[IP].dst}")
        print(f"Puerto origen: {pkt[TCP].sport}")
        print(f"Puerto destino: {pkt[TCP].dport}")
        print(f"SEQ: {pkt[TCP].seq}")
        print(f"ACK: {pkt[TCP].ack}")
        print(f"Payload length: {payload_len} bytes")
        print("=" * 21)
        print("Tipo:", descripcion)
        if Raw in pkt:
            try:
                print(pkt[Raw].load.decode(errors='ignore').strip())
            except:
                print("Payload no decodificable.")
        else:
            print("Sin datos.")
        print("+" * 21, flush=True)
        contador += 1

print(f"[*] Escuchando TODO el tráfico TCP en la interfaz {INTERFAZ}...")
sniff(iface=INTERFAZ, filter="tcp", prn=mostrar, store=0)

