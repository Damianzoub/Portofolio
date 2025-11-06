---
title: "Building My ML Portfolio with Next.js and FastAPI"
date: "2025-11-07"
tags: ["nextjs", "fastapi", "ml", "portfolio"]
excerpt: "A walkthrough of how I combined a Python backend and a modern React frontend to showcase my projects."
---

Welcome to my first post! 👋  

In this article, I’ll explain how I created my **machine learning portfolio** using:

- **FastAPI** for the backend (serving models and APIs)
- **Next.js** for the frontend (React + TailwindCSS)
- **GitHub Actions** for CI/CD

---

### 🧠 The idea
I wanted a website that was more than a static résumé — something interactive that demonstrates my real work.

### ⚙️ Tech stack
- Python + FastAPI
- Node.js + Next.js
- TailwindCSS
- Docker (for deployment)

---

### 🧩 Project structure

```text
frontend/
  app/
  components/
  lib/
  content/posts/
backend/
  main.py
  models/
