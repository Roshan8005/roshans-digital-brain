# Roshan Kumar Sah's Digital Brain - Local Web Dashboard Server
# Location: Root / brain_server.py

import os
import sys
import json
import urllib.parse
import http.server
import socketserver
import subprocess
import webbrowser

# Prevent console crashes due to unicode/emoji characters on Windows cmd/powershell
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

base_dir = r"E:\rgai brain"

# Insert paths to allow importing from root and sub-modules
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, "4_Limbic_System"))
sys.path.append(os.path.join(base_dir, "2_Cerebellum"))

from brain_kernel import process_query, load_neuroplasticity_weights

PORT = 8080

class BrainHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Override to suppress standard HTTP logging in the console
        return

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # 1. API: Get Neuroplasticity Stats
        if path == "/api/stats":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            weights = load_neuroplasticity_weights()
            self.wfile.write(json.dumps(weights).encode('utf-8'))
            return
            
        # 2. API: Get Connected Projects list
        elif path == "/api/projects":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            projects_dir = os.path.join(base_dir, "1_Cerebrum", "Frontal_Lobe", "Projects")
            projects = []
            if os.path.exists(projects_dir):
                projects = [p for p in os.listdir(projects_dir) if not p.startswith('.')]
            self.wfile.write(json.dumps(projects).encode('utf-8'))
            return
            
        # 3. API: Query the Brain Kernel
        elif path == "/api/query":
            q = query_params.get("q", [""])[0]
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            res = process_query(q)
            self.wfile.write(json.dumps(res).encode('utf-8'))
            return
            
        # 4. API: Simulate Synaptic Transmission
        elif path == "/api/simulate":
            start_id = query_params.get("start", ["1"])[0]
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            signal_script = os.path.join(base_dir, "transmit_signal.py")
            output_text = ""
            if os.path.exists(signal_script):
                cmd = f'python "{signal_script}" --start {start_id} --message "Web_Dashboard_Pulse" --hops 3'
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
                output_text = res.stdout
            else:
                output_text = "Error: transmit_signal.py script not found."
                
            self.wfile.write(json.dumps({"output": output_text}).encode('utf-8'))
            return
            
        # 5. Serve Web Frontend
        elif path == "/":
            html_path = os.path.join(base_dir, "2_Cerebellum", "dashboard.html")
            if os.path.exists(html_path):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                with open(html_path, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                self.send_error(404, "Frontend dashboard.html not found.")
            return
            
        else:
            self.send_error(404, "Page Not Found")

def run_server():
    # Use standard TCPServer with reuse_address option
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), BrainHTTPRequestHandler) as httpd:
        print("==================================================")
        print(f"🚀 BRAIN DASHBOARD SERVER STARTED: http://localhost:{PORT}")
        print("==================================================")
        print("Press Ctrl+C to terminate the server.")
        
        # Auto-open browser
        try:
            webbrowser.open(f"http://localhost:{PORT}")
        except Exception as e:
            print(f"[Warning] Failed to open browser automatically: {e}")
            
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down brain server... Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    run_server()
