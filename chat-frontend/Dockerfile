# --- Этап 1: Сборка (Build) ---
FROM node:18-alpine as build
LABEL authors="makksesh"

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build


# --- Этап 2: Запуск (Production) ---
FROM nginx:alpine

# Копируем из ПЕРВОГО этапа (build) папку dist в папку, откуда Nginx раздает файлы
COPY --from=build /app/dist /usr/share/nginx/html

# Копируем наш конфиг nginx, чтобы React роутинг работал
# (иначе при обновлении страницы будет 404)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# Запускаем Nginx в фоне
CMD ["nginx", "-g", "daemon off;"]