# Stage 1: Build the Hugo site
FROM gohugoio/hugo:latest AS builder

# Reset entrypoint to allow running shell commands
ENTRYPOINT []

# Install git as it might be required by the theme
RUN apk add --no-cache git

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
