#!/bin/bash
# create_new_module.sh
# Usage: ./create_new_module.sh <number> <topic> <author> <difficulty>
# Example: ./create_new_module.sh 12 advanced-taxi-play "John Doe" "advanced"

# Validate inputs
if [ $# -ne 4 ]; then
    echo "Usage: $0 <number> <topic> <author> <difficulty>"
    exit 1
fi

NUMBER=$1
TOPIC=$2
AUTHOR=$3
DIFFICULTY=$4

# Validate number
if ! [[ "$NUMBER" =~ ^[0-9]+$ ]]; then
    echo "ERROR: Number must be a positive integer"
    exit 1
fi

# Generate filename
FILE_NAME="${NUMBER}-advanced-${TOPIC//[^a-zA-Z0-9]/-}.md"
DIR_PATH="content/modules/${NUMBER}-advanced-${TOPIC//[^a-zA-Z0-9]/-}"

# Create directory
mkdir -p "$DIR_PATH"

# Generate module template
cat > "$DIR_PATH/$FILE_NAME" << EOF
---
title: Advanced ${TOPIC^}
date: $(date +%Y-%m-%d)
author: $AUTHOR
difficulty-level: $DIFFICULTY
---

# Advanced ${TOPIC^}

## Overview
[Insert overview content here]

## Core Principles
- [Principle 1]
- [Principle 2]
- [Principle 3]

## Techniques
[Insert techniques documentation here]

## Case Studies
[Insert case studies documentation here]

## Safety Protocols
[Insert safety protocols]

## Testing
[Insert testing requirements]

---

EOF

# Update navigation files
cd "$(dirname "$0")/.."
./update_navigation.sh

echo "✅ New module template created at: $DIR_PATH/$FILE_NAME"
echo "   - Added to navigation scripts"
echo "   - Ready for content development"