import http.server
import socketserver
import webbrowser
import os

PORT = 5000
DIRECTORY = r"c:\Users\Admin\Desktop\python projects\aakash_academy_prompts"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print(f"==================================================")
        print(f"  AAKASH ACADEMY PROMPT HUB LOCAL SERVER STARTED  ")
        print(f"  Access website at: {url}")
        print(f"==================================================")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    start_server()
