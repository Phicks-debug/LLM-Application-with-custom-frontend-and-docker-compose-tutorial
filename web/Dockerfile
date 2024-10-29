FROM node:18-alpine

# Add a build argument to force rebuild
ARG REBUILD
RUN echo "Rebuild trigger: ${REBUILD:-1}"

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]