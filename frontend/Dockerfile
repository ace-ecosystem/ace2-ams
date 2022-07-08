# BUILD STAGE
FROM node:16-alpine as builder

ARG http_proxy
ARG https_proxy
ARG no_proxy
ARG npm_strict_ssl=true

ENV http_proxy=$http_proxy
ENV https_proxy=$https_proxy
ENV no_proxy=$no_proxy

WORKDIR /app

COPY package*.json .

RUN apk --no-cache add --virtual native-deps \
  g++ gcc libgcc libstdc++ linux-headers make python 

RUN npm config set strict-ssl ${npm_strict_ssl} && \
  npm install node-gyp -g && \
  npm install && \
  apk del native-deps

COPY . .

RUN npm run build

# PRODUCTION STAGE
FROM nginx:stable-alpine as production

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]