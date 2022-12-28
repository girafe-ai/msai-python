# Network

Content:

1. Theory: Basics, TCP UDP, HTTP, SSL
2. Client: requests
3. Server: flask
4. Telegram bots


# 1. Theory

Connection via Internet (example):

```
client1, client2, ...
  ||       //  wifi router
  ||      //  internet provider
  ..     ..  intermediate nodes
  ||    //  ...
  ||   //  data center
  server
```



### 1.1 How the client finds the server

- IP is an address of the server in internet
- IPv4 (0.0.0.0 - 255.255.255.255) and IPv6 are widely used
- to get an IP by its alias (domain) a DNS used
- DNS available via IP that automatically comes with internet connection or set manually
- Client send request to Server by IP onto specified port
- By default, 80 used for http, 443 for https, 22 for ssh, ...
- Example:
```
- when you type `https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages` in browser
- browser gets ip of developer.mozilla.org which is 65.9.164.9
- and open connection with 65.9.164.9:443
```


### 1.2 How connection works

- Data is transmitted by cables, waves, so it can be partially lost or corrupted
- There are several methods, like checksum and multiple repeats, how to detect corrupted data and restore it
- There are low level protocols, which use these methods and allows to send bytes and be sure that they are received without corruption
- Most popular are TCP and UDP
- TCP guaranteed with very high precision that no data lost or corrupted (most communications used TCP)
- UDP guaranteed that no data corrupted, but some data can be lost (used when data quickly became irrelevant, e.g. in video streaming)


### 1.3 Hyper Text Transfer Protocol

- [Detailed docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages)
- [List of HTTP status codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes)
- [List of HTTP headers](https://en.wikipedia.org/wiki/List_of_HTTP_header_fields)

HTTP request example:
```
GET /en-US/docs/Web/HTTP/Messages HTTP/1.1
Accept: text/html, */*

```

HTTP response example:
```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 145447

<!doctype html><html lang="en-US" prefix="og: https://ogp.me/ns#"><head>... 
```


### 1.4 SSL

- SSL over HTTP (HTTPS) can be used to send HTTP message securely
- SSL uses cryptography so message can be encrypted by anyone, but decrypted only by receiver
- all https messages (method, URL, status code, headers and bodies) became inaccessible for those who listen network
- for example for internet provider, other wifi users
- IP address and approximate body size still accessible


# 2. Client

See examples on making a client via Python's [`requests`](https://pypi.org/project/requests/) in `client.py`.

You can also use `curl` command in terminal to make http request.


# 3. Server

See server example made with [`flask`](https://pypi.org/project/Flask/) in `server.py` and it's client in `myserverclient.py`.


# 4. Telegram bots

- Telegram bots can be created via long pulling or via webhooks
- Webhooks required publicly accessible server, so it's harder to implement
- Long pulling bots make requests for updates every several milliseconds
- So there are small delay between user's message and its handling, but these bots works only as clients
- Telegram has [HTTP API and instructions](https://core.telegram.org/bots) for bots
- But writing integration based on raw API would be too hard
- Better to use one of [ready-to-use packages](https://core.telegram.org/bots/samples#python)
- These packages can help to receive and send messages with Python function, may be even to create dialog trees
- Example with `python-telegram-bot` in `bot.py`
