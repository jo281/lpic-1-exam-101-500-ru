# ── Stage 1: Сборка ──
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .
RUN npm run build

# ── Stage 2: Nginx ──
FROM nginx:alpine

# Убираем дефолтный конфиг
RUN rm /etc/nginx/conf.d/default.conf

# Копируем свой конфиг
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Копируем собранные файлы
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
