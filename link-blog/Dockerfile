# Stage 1: Build the Hugo site
FROM debian:stable-slim@sha256:99fc6d2a0882fcbcdc452948d2d54eab91faafc7db037df82425edcdcf950e1f AS builder

# Install dependencies
RUN apt-get update && apt-get install -y git curl ca-certificates && rm -rf /var/lib/apt/lists/*

# Download and install Hugo Extended
ENV HUGO_VERSION=0.152.0
RUN set -eux; \
    arch="$(dpkg --print-architecture)"; \
    case "$arch" in \
      amd64) hugo_arch="amd64" ;; \
      arm64) hugo_arch="arm64" ;; \
      *) echo "Unsupported architecture: $arch" >&2; exit 1 ;; \
    esac; \
    curl -L "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-${hugo_arch}.tar.gz" | tar -xz -C /usr/local/bin hugo

WORKDIR /src
COPY . .

# PaperMod theme setup (no special moves needed usually)
# If PaperMod needs any specific setup, add it here.
# For now, we assume standard structure works.

# Build the site with minification
RUN hugo --minify

# Stage 2: Serve with Nginx Alpine
FROM nginx:alpine@sha256:f46cb72c7df02710e693e863a983ac42f6a9579058a59a35f1ae36c9958e4ce0

# 升級目前已知有修補版的 Alpine 套件，避免沿用 base image 內的高風險 CVE。
RUN apk upgrade --no-cache libexpat zlib

# Copy the generated static site from the builder stage
COPY --from=builder /src/public /usr/share/nginx/html

# Copy the Nginx configuration template
COPY config/nginx.conf.template /etc/nginx/nginx.conf.template

# Substitute $PORT and start Nginx
# nginx:alpine has envsubst. We use it to replace $PORT in the template.
CMD ["/bin/sh", "-c", "envsubst '$PORT' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'"]
