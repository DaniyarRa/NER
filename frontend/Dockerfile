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
