FROM ubuntu:22.04

# Install socat and clean up apt cache
RUN apt-get update && apt-get install -y \
    socat \
    && rm -rf /var/lib/apt/lists/*

# Create an unprivileged user
RUN useradd -m -u 1000 ctf

WORKDIR /challenge

# Copy target binary and flag
COPY pivot2gadgets /challenge/pivot2gadgets
COPY flag.txt /challenge/flag.txt

# Lock down permissions:
# - Root owns the directory so 'ctf' user cannot create/delete/rename files
# - Binary is readable & executable
# - Flag is strictly read-only
RUN chown -R root:root /challenge && \
    chmod 755 /challenge && \
    chmod 755 /challenge/pivot2gadgets && \
    chmod 444 /challenge/flag.txt

# Switch context to the non-root user
USER ctf

EXPOSE 1337

# Serve binary over TCP as the 'ctf' user
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:/challenge/pivot2gadgets"]