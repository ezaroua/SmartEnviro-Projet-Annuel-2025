# Utiliser une image Node.js officielle
FROM node:18

# Définir le dossier de travail
WORKDIR /app

# Copier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier tout le code source
COPY . .

# Exposer le port 5173 (si Vite) ou 8080 (si Vue CLI)
EXPOSE 5173

# Démarrer l’application
CMD ["npm", "run", "dev"]
