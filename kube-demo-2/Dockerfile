from node:carbon

# Create a working directory
WORKDIR /usr/src/app

COPY package.json .
COPY package-lock.json ,

RUN npm install

COPY . .

EXPOSE 8080

CMD ["npm", "start"]
