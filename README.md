# Proxy Checker

A simple and fast **Smart Proxy Type Detector & Checker** script written in Python.

## Features

- Detects and checks proxies of types: HTTP, SOCKS4, SOCKS5.
- Tests proxy connectivity by sending a request to `http://httpbin.org/ip`.
- Saves working and dead proxies separately by type.
- Uses multithreading to check proxies concurrently for faster results.
- Easy to use command-line interface with a cool ASCII logo.

## Requirements

- Python 3.6+
- `requests` library (`pip install requests`)

## Usage

1. Place your mixed proxy list (one proxy per line, e.g., `ip:port`) in a text file.
2. Run the script:
   python proxy_chk.py
