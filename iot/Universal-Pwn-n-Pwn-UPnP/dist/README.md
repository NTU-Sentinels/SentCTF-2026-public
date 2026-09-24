## Docker setup for local testing

Test that yo are able to retrieve the flag on your local machine first before attempting on the remote server!

Open a terminal in the directory on the same directory as the Dockerfile:

```shell
docker build --no-cache -t upnpd-ctf .

docker run --rm \
    -p 5000:5000/tcp \
    -p 1900:1900/tcp \
    upnpd-ctf
```

You can now access the server on UDP/1900 and TCP/5000 respectively.
