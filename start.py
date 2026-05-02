import socket
import subprocess
import sys
import threading
import time

def hold_port():
    """Bind port 8069 immediately to satisfy Render's health check."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8069))
    s.listen(5)
    # Accept and close connections for 60 seconds while Odoo loads
    s.settimeout(60)
    start = time.time()
    while time.time() - start < 60:
        try:
            conn, _ = s.accept()
            conn.close()
        except:
            pass
    s.close()

# Start port holder in background
t = threading.Thread(target=hold_port, daemon=True)
t.start()

# Give it a moment to bind
time.sleep(1)

# Launch Odoo
result = subprocess.run([
    'odoo', '--config=/etc/odoo/odoo.conf'
])
sys.exit(result.returncode)