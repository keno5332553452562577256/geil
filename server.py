import socketserver
import threading

clients = []


class MyHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print(f"[+] Client verbunden: {self.client_address}")
        clients.append(self.request)

        try:
            while True:
                data = self.request.recv(1024)

                if not data:
                    break

                message = data.decode()
                print(f"[{self.client_address}] {message}")

                # Nachricht an alle anderen Clients senden
                for client in clients:
                    if client != self.request:
                        client.sendall(f"{self.client_address}: {message}".encode())

        except:
            pass

        finally:
            print(f"[-] Client getrennt: {self.client_address}")
            clients.remove(self.request)
            self.request.close()


if __name__ == "__main__":
    with socketserver.ThreadingTCPServer(("localhost", 9999), MyHandler) as server:
        print("Chat-Server läuft auf Port 9999...")
        server.serve_forever()