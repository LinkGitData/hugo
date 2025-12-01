# Stage 1: Build the Hugo site
FROM debian:stable-slim AS builder

# Install dependencies
RUN apt-get update && apt-get install -y git curl ca-certificates && rm -rf /var/lib/apt/lists/*

# Download and install Hugo Extended
ENV HUGO_VERSION=0.121.1
RUN curl -L https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz | tar -xz -C /usr/local/bin hugo

WORKDIR /src
COPY . .

# Fix Congo theme directory structure (rename _partials to partials, etc)
RUN if [ -d "themes/congo/layouts/_partials" ]; then mv themes/congo/layouts/_partials themes/congo/layouts/partials; fi
RUN if [ -d "themes/congo/layouts/_shortcodes" ]; then mv themes/congo/layouts/_shortcodes themes/congo/layouts/shortcodes; fi

# Build the site with minification
RUN hugo --minify

# Stage 2: Serve with Nginx Alpine
FROM nginx:alpine

# Copy the generated static site from the builder stage
COPY --from=builder /src/public /usr/share/nginx/html

# Copy the Nginx configuration template
COPY config/nginx.conf.template /etc/nginx/nginx.conf.template

# Substitute $PORT and start Nginx
# nginx:alpine has envsubst. We use it to replace $PORT in the template.
CMD ["/bin/sh", "-c", "envsubst '$PORT' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'"]
