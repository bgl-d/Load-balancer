# Load Balancer Demo

This project demonstrates a simple round-robin load balancer built with Flask. It distributes incoming HTTP requests across four backend Flask servers and returns the response from the selected backend instance.

## Overview

The application consists of:

- 4 backend servers running in Docker containers
- A Python-based load balancer that forwards requests in round-robin order
- A small Flask app on each backend that returns a message identifying the server

## Project Structure

```text
Load-balancer/
├── app/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── main.py
├── load-balancer/
│   └── load-balancer.py
└── README.md
```

## How It Works

- The backend app in `app/main.py` exposes a single route `/`.
- Each backend server responds with a message like `Hello from Server 1`.
- The load balancer in `load-balancer/load-balancer.py` selects a backend in a rotating sequence and forwards the original request.
- Requests are proxied while preserving method, path, headers, cookies, and body.

## Prerequisites

- Docker
- Docker Compose
- Python 3
- pip

## Run the Backend Servers

From the `app` directory:

```bash
cd app

docker build -t server .
docker compose up -d
```

This starts four Flask services using the Docker image built from `app/Dockerfile`.

## Run the Load Balancer

From the project root:

```bash
cd load-balancer
python load-balancer.py
```

The load balancer will listen on port `8000`.

## Test the Load Balancer

Open the following URL in a browser or use curl:

```bash
curl http://localhost:8000
```

You should see a response like:

```text
Hello from Server 1
```

Refresh the page multiple times to see the requests rotate across the backend servers.
