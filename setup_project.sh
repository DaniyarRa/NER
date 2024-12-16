#!/bin/bash

# Set project name
PROJECT_NAME="my_project"
BACKEND_DIR="$PROJECT_NAME/backend"
FRONTEND_DIR="$PROJECT_NAME/frontend"

# Create main project directory
echo "Creating project structure..."
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME || exit

# Create Backend
echo "Setting up FastAPI backend..."
mkdir -p $BACKEND_DIR/app/{routers,models,dependencies}
cat > $BACKEND_DIR/app/main.py <<EOL
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Backend"}
EOL

cat > $BACKEND_DIR/requirements.txt <<EOL
fastapi
uvicorn
EOL

# Optional: Add Dockerfile for backend
cat > $BACKEND_DIR/Dockerfile <<EOL
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY app ./app

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
EOL

# Create Frontend
echo "Setting up React frontend..."
mkdir -p $FRONTEND_DIR
cd $FRONTEND_DIR || exit
npx create-react-app . --use-npm

# Optional: Add Dockerfile for frontend
cat > Dockerfile <<EOL
# Use the official Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json ./
RUN npm install

# Copy the rest of the application
COPY . ./

# Build the React app
RUN npm run build

# Start the application
CMD ["npm", "start"]

# Expose port
EXPOSE 3000
EOL

# Add Axios and React Router DOM
npm install axios react-router-dom

# Return to project root
cd ../../

# Create .gitignore
echo "Creating .gitignore..."
cat > .gitignore <<EOL
__pycache__/
node_modules/
.env
*.pyc
EOL

# Create README
echo "Creating README..."
cat > README.md <<EOL
# $PROJECT_NAME

This is a full-stack project with:
- **Backend**: FastAPI
- **Frontend**: React

## Running the Project

### Backend
1. Navigate to the backend directory:
    \`\`\`bash
    cd backend
    \`\`\`
2. Install Python dependencies:
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`
3. Start the backend server:
    \`\`\`bash
    uvicorn app.main:app --reload
    \`\`\`

### Frontend
1. Navigate to the frontend directory:
    \`\`\`bash
    cd frontend
    \`\`\`
2. Install dependencies:
    \`\`\`bash
    npm install
    \`\`\`
3. Start the React development server:
    \`\`\`bash
    npm start
    \`\`\`

### Optional: Docker
You can use Docker to containerize both the backend and frontend.
EOL

echo "Project setup complete!"
