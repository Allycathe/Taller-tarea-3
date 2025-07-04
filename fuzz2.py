import socket

# Dirección IP y puerto del servidor FTP
FTP_SERVER = "172.17.0.2"
FTP_PORT = 21

# Crear socket TCP para el canal de control FTP
control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    print(f"[+] Conectando al servidor FTP en {FTP_SERVER}:{FTP_PORT}...")
    control_socket.connect((FTP_SERVER, FTP_PORT))

    # Recibir mensaje de bienvenida del servidor FTP
    banner = control_socket.recv(1024).decode()
    print(f"[+] Banner recibido: {banner.strip()}")

    # Lista de comandos FTP inválidos o aleatorios
    comandos_invalidos = [
        b"FZZZ archivo.txt\r\n",             # Comando inexistente
        b"USER\r\n",                         # USER sin argumento
        b"PASS\r\n",                         # PASS sin argumento
        b"RETR\r\n",                         # RETR sin nombre de archivo
        b"STOR \x00\xff\r\n",                # Argumento binario malformado
        b"\x01\x02\x03\x04\r\n",             # Completamente ilegible
        b"LIST -l /root\r\n",                # Argumento sensible si no está permitido
    ]

    # Enviar los comandos uno por uno
    for cmd in comandos_invalidos:
        print(f"[+] Enviando comando inválido: {repr(cmd)}")
        control_socket.send(cmd)
        respuesta = control_socket.recv(1024).decode(errors="ignore")
        print(f"[+] Respuesta del servidor: {respuesta.strip()}\n")

finally:
    control_socket.close()
    print("[+] Conexión cerrada")

