# Product Requirement Document (PRD)
## Project Name: Eirene's Birthday RPG / Farm Simulation Gift

### 1. Project Overview
A personalized, interactive retro RPG/Farm Sim landing page built as a birthday gift for Eirene Debora Ulina. It features a pixel-art aesthetic inspired by Harvest Moon and Pokémon, dynamic interactive menus, and references to her white dog, Cairo.

### 2. Objectives
- Deliver a memorable digital birthday experience.
- Maintain a 100% domain-agnostic architecture for easy deployment anywhere.

### 3. Functional Requirements
- **Interactive Farm Profile Canvas:** Left-side display with Eirene and Cairo. Clicking Cairo triggers interaction.
- **RPG Action Menu:** Right-side buttons containing a birthday letter, a mini-game, farming fun stats, and her character sheet.
- **Domain Agnostic:** All assets are referenced via relative paths.


Infrastructure & Deployment
Hosting Model: Static Site Hosting.

Target Platforms: GitHub Pages (100% Free) or Netlify/Vercel (Free tier).

Domain Portability: No hardcoded URLs in the script or style documents. The site must render perfectly whether accessed via a raw IP address, a testing subdomain (e.g., *.github.io)

🚀 Step-by-Step Deployment Guide (Free & Quick)
Option A: Deploying on GitHub Pages (Recommended)
Prepare Your Image: Rename the photo from your Instagram screenshot to exactly cairo_and_eirene.jpg and place it in the same directory/folder as your index.html file.

Go to GitHub and create a free account (if you don't have one).

Create a New Repository named eirene-birthday.

Upload both your index.html and cairo_and_eirene.jpg files directly using your browser.

Head to the repository Settings tab ⚙️ → Pages section on the left sidebar.

Under Build and deployment, change the Branch source to main (or master) and click Save.

Your site will be live for free at https://<your-username>.github.io/eirene-birthday/ within minutes!
