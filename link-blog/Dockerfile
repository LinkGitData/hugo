# Stage 1: Build the Hugo site
FROM cibuilds/hugo:latest AS builder

# cibuilds/hugo usually has git and shell
# We don't need to reset ENTRYPOINT usually, but let's be safe or check docs. 
# cibuilds/hugo entrypoint is usually empty or shell.
# It is based on Alpine.

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
