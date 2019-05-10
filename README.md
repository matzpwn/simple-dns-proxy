# simple-dns-proxy

This project is for learning purpose. I use python to create simple dns proxy. Please find the project under the `python` directory.

## python
a simple python script to listen to socket (53), and forward to cloudflare dns `1.1.1.1` qith tls.

### How to setup
- cd python/
- `docker build -t simple-dns .`
- `docker run -itd simple-dns`

### Test dns with dig
- `dig @$(sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' simple-dns) google.com`
