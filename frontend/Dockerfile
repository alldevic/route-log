FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
COPY tsconfig.json ./
RUN npm install
RUN npm run build
COPY . .
