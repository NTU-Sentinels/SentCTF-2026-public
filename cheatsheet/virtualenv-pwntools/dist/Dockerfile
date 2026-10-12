FROM python:3.12-slim

# Install system dependencies required by pwntools & network tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    git \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create a virtual environment at /opt/venv
RUN python3 -m venv /opt/venv

# Force Python/pip to use the virtual environment binaries by default
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install pwntools inside the venv
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir pwntools

# Create non-root user
RUN useradd -ms /bin/bash pwnuser

# Grant pwnuser permission to the /app directory and venv
RUN chown -R pwnuser:pwnuser /app /opt/venv

# Show (venv) prompt when running bash
RUN echo 'export PS1="(venv) \u@\h:\w\$ "' >> /home/pwnuser/.bashrc

USER pwnuser

# Open an interactive bash terminal on start
CMD ["/bin/bash"]