#!/bin/bash

# Check if a title was provided
if [ -z "$1" ]; then
  echo "Usage: ./create_post.sh \"Post Title\""
  exit 1
fi

TITLE="$1"
# Convert title to filename-friendly slug (lowercase, spaces to hyphens)
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g' | sed 's/[^a-z0-9-]//g')
FILENAME="content/posts/${SLUG}.md"

# Check if file already exists
if [ -f "link-blog/$FILENAME" ]; then
  echo "Error: Post already exists at link-blog/$FILENAME"
  exit 1
fi

# Create the post using Hugo (to harness archetypes if needed, or just manual file creation)
# Since we are in the root, we run hugo new relative to link-blog
cd link-blog
hugo new posts/${SLUG}.md --kind post

echo "✅ Created new post: link-blog/$FILENAME"
echo "You can edit it now."
