# simple-dns-proxy

This project is for learning purpose. I use python to create simple dns proxy. Please find the project under the `python` directory. I use python since I quite familiar with it and easy to provide the libraries.

## python
a simple python script to listen to socket (53), and forward to cloudflare dns `1.1.1.1` with tls.

### How to setup
- `cd python/`
- `docker build -t simple-dns .`
- `docker run -itd simple-dns`

### Test query with dig+docker
- `dig @$(sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' simple-dns) google.com`

### Test query without docker
- `cd python/`
- `chmod +x pycloudflare.py`
- `./pycloudflare.py`
- `dig @127.0.0.1 google.com`

if port `53` already used in your system, please change it to another port. for example:
- `cd python/`
- `chmod +x pycloudflare.py`
- `./pycloudflare.py -p 1053`
- `dig -p 1053 @127.0.0.1 google.com`

### Q&A

- Q: Imagine this proxy being deployed in an infrastructure. What would be the security
concerns you would raise?
    - A: key rotation, service scaling
- Q: How would you integrate that solution in a distributed, microservices-oriented and
containerized architecture?
    - A: This project is containerized, it would be easy to integrate with other microservice / to be a part of containerized architecture
- Q: What other improvements do you think would be interesting to add to the project?
    - A: I'm thinking to provide the API, then the application can use it with direct API call