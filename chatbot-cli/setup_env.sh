#!/bin/bash

# Define the placeholder filename
EXAMPLE_FILE=".env.example"
GITIGNORE_FILE=".gitignore"

echo "Creating $EXAMPLE_FILE..."

# Use a 'Here Document' to create the file with placeholder keys
cat <<EOF > $EXAMPLE_FILE
# ------------------------------------------------------------------------------
# ENVIRONMENT VARIABLES TEMPLATE
# Copy this file to .env and fill in the actual values.
# DO NOT commit the .env file to version control.
# ------------------------------------------------------------------------------

# API Keys
OPENAI_API_KEY=your_api_key_here
STRIPE_SECRET_KEY=your_stripe_key_here
AWS_ACCESS_KEY_ID=your_aws_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_here

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=admin
DB_PASSWORD=password_here

# Application Settings
DEBUG=True
APP_ENV=development
EOF

echo "$EXAMPLE_FILE created successfully."

# Check if .gitignore exists, if not create it
if [ ! -f "$GITIGNORE_FILE" ]; then
    echo "Creating $GITIGNORE_FILE..."
    touch "$GITIGNORE_FILE"
fi

# Check if .env is already in .gitignore; if not, add it
if grep -q ".env" "$GITIGNORE_FILE"; then
    echo ".env is already being ignored by git."
else
    echo ".env" >> "$GITIGNORE_FILE"
    echo "Added .env to $GITIGNORE_FILE to prevent accidental leaks."
fi

echo "------------------------------------------------------------------"
echo "Setup complete!"
echo "Next steps:"
echo "1. Run 'cp $EXAMPLE_FILE .env' to create your local environment file."
echo "2. Open .env and replace the placeholders with your actual API keys."
echo "3. Commit $EXAMPLE_FILE and $GITIGNORE_FILE to your repository."
