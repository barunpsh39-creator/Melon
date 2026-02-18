import argparse
import http.server
import socketserver
import threading
import time
import webbrowser
from pathlib import Path


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def serve_and_open(port: int, no_open: bool = False, duration: int = 300) -> None:
    root = Path(__file__).resolve().parent
    html_path = root / "melon.html"
    if not html_path.exists():
        raise FileNotFoundError(f"melon.html not found: {html_path}")

    handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(*args, directory=str(root), **kwargs)
    with ReusableTCPServer(("127.0.0.1", port), handler) as httpd:
        url = f"http://127.0.0.1:{port}/melon.html"

        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()

        if not no_open:
            webbrowser.open(url)

        print(f"Serving Melon page at: {url}")
        print("Press Ctrl+C to stop.")

        try:
            start = time.time()
            while True:
                time.sleep(0.5)
                if duration > 0 and (time.time() - start) > duration:
                    break
        except KeyboardInterrupt:
            pass
        finally:
            httpd.shutdown()
            httpd.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch Melon HTML page via local server")
    parser.add_argument("--port", type=int, default=4173, help="Port to serve (default: 4173)")
    parser.add_argument("--no-open", action="store_true", help="Do not open the browser automatically")
    parser.add_argument(
        "--duration",
        type=int,
        default=300,
        help="Auto-shutdown seconds (default: 300, set 0 for no timeout)",
    )
    args = parser.parse_args()

    serve_and_open(port=args.port, no_open=args.no_open, duration=args.duration)


if __name__ == "__main__":
    main()
