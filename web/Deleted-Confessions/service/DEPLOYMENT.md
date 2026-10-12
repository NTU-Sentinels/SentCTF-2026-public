# Hosted CTFd Deployment

`docker-compose.yml` is for local testing only. Hosted CTFd deploys this challenge as one Docker image.

## Image Requirements

- Build the image from `service/`.
- The image already exposes port `5000` in its Dockerfile.
- Hosted CTFd requires a `linux/amd64` image.
- Do not upload or deploy the local `docker-compose.yml` file to Hosted CTFd.
- Keep the organiser repository private until after the CTF. It contains `challenge.yml`, the flag, and the internal solution.
- The service generates a fresh server-side session-signing secret when it starts. A container restart invalidates existing moderator sessions, which is acceptable for this stateless challenge.

## Deploy The Image

1. In Hosted CTFd, open **Admin Panel** > **Containers**.
2. Under **Images**, select the plus icon and create an image named `deleted-confessions`.
3. On the organiser computer, log in to the CTFd registry using the account and subdomain shown by Hosted CTFd:

   ```powershell
   docker login -u '<username>@<subdomain>.ctfd.io' registry.ctfd.io
   ```

4. From the challenge folder, build a Linux AMD64 image:

   ```powershell
   docker build --platform linux/amd64 -t deleted-confessions:latest .\service
   ```

5. Tag it with your Hosted CTFd subdomain and image name:

   ```powershell
   docker tag deleted-confessions:latest registry.ctfd.io/<subdomain>/deleted-confessions
   ```

6. Push it to the registry:

   ```powershell
   docker push registry.ctfd.io/<subdomain>/deleted-confessions
   ```

7. Return to **Admin Panel** > **Containers**. Under **Services**, select the plus icon. Use a lowercase service title such as `deleted-confessions` and select the pushed image.
8. Wait for Hosted CTFd to deploy the service. Copy its generated HTTPS hostname.
9. Import or sync `challenge.yml` into CTFd, then set the challenge's **Connection Info** to the generated service URL.

## Verify Before Publishing

1. Open the generated service URL in a private/incognito browser window.
2. Complete the intended solve once as a player.
3. Confirm that the public page contains no flag or internal solution text.
4. Confirm that the final flag is accepted by the CTFd challenge.
