from flask import Flask, Response, request
import requests

app = Flask(__name__)

backend_servers = [
    'http://localhost:8081', 
    'http://localhost:8082', 
    'http://localhost:9081', 
    'http://localhost:9082'
]

current_server = 0

def get_next_server():
    global current_server
    server = backend_servers[current_server]
    current_server = (current_server + 1) % len(backend_servers)
    return server

@app.route("/", methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def load_balancer():
    # Log incoming request
    print("Received request from", request.remote_addr)
    print(f"{request.method} {request.path}")

    # Select backend server
    backend_server = get_next_server()
    print(f"Forwarding request to {backend_server}")

    # Forward the request to the backend server
    try:
        forwarded_response = requests.request(
            method=request.method,
            url=f"{backend_server}{request.full_path}",
            headers=request.headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )

        # Forward the response back to the client
        response = Response(
            forwarded_response.content,
            status=forwarded_response.status_code,
            headers=dict(forwarded_response.headers)
        )
        return response

    except requests.exceptions.RequestException as e:
        print(f"Error forwarding request: {e}")
        return Response("Error forwarding request.\n", status=502)

if __name__ == "__main__":
    print("Starting load balancer on port 8000")
    app.run(host="0.0.0.0",port=8000)