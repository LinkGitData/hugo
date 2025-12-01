# Stage 1: Build the Hugo site
FROM debian:stable-slim AS builder

# Install dependencies
RUN apt-get update && apt-get install -y git curl ca-certificates && rm -rf /var/lib/apt/lists/*

# Download and install Hugo Extended
ENV HUGO_VERSION=0.121.1
RUN curl -L https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz | tar -xz -C /usr/local/bin hugo

WORKDIR /src
COPY . .

# Build the site with minification
RUN hugo --minify

# Stage 2: Serve with Chainguard Nginx
FROM cgr.dev/chainguard/nginx:latest

# Copy the generated static site from the builder stage
COPY --from=builder /src/public /usr/share/nginx/html

# Copy the Nginx configuration template
COPY config/nginx.conf.template /etc/nginx/nginx.conf.template

# Use a shell command to substitute the PORT environment variable and start Nginx
# We write to /tmp/nginx.conf because the default location might not be writable by the non-root user
CMD ["/bin/sh", "-c", "sed \"s/\\${PORT}/$PORT/g\" /etc/nginx/nginx.conf.template > /tmp/nginx.conf && nginx -c /tmp/nginx.conf -g 'daemon off;'"]
