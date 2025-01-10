# Use Debian Bookworm as the base image ©2024, Ovais Quraishi
FROM python:3.13-bookworm

WORKDIR /app

# Debian 12 thing
ENV PIP_BREAK_SYSTEM_PACKAGES=1
ENV USER_AGENT="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"

# Copy necessary files to /app directory
COPY config.py /app
COPY ui.py /app
COPY setup.config /app
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Service config
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Run
CMD ["/app/ui.py"]
