FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

WORKDIR /app/src

EXPOSE 3000

CMD ["npm", "start"]
