FROM node:12-alpine as builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

RUN npm run build

# ----

FROM nginx:1.17.10-alpine

COPY --from=builder /app/dist /usr/share/nginx/html
