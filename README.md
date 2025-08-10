# 🖼️ Image Generator Backend

Welcome to the **Image Generator Backend**! 🚀 This is the backend service for an AI-powered image generation app, built with **Python**, **FastAPI**, **Celery**, **Redis**, **Postgres**, **MinIO**, and the **Stability AI API**.

> ⚠️ This is **only the backend** – it exposes an API for generating images but does not include a frontend.

---

## ✨ Features

* 🔑 API key–protected endpoints
* 📸 Text-to-image generation using Stability AI
* 📦 Async task processing with Celery + Redis
* ☁️ S3-compatible storage via MinIO
* 📄 API documentation via Swagger UI
* 🛡️ Configurable and production-ready architecture

---

## 🛠️ Getting Started

### 1. Clone the repo & set up `.env`

```bash
git clone <your-repo-url>
cd <project-folder>
cp .env.example .env
```

Edit `.env` and add your **Stability API key** plus other configs.

### 2. Start the backend services

```bash
docker compose up --build
```

Wait until `api`, `worker`, `db`, `redis`, and `minio` are running.

### 3. Open API docs

Go to:

```
http://localhost:8000/docs
```

Here you can view and test all endpoints.

---

## 📌 How to Use

### 1️⃣ Create a generation job

```bash
curl -X POST http://localhost:8000/v1/generations \
  -H "X-API-Key: dev-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"A high detail photo of a snow leopard in the mountains","aspect_ratio":"16:9"}'
```

Replace `dev-secret-key` with your actual API key.

### 2️⃣ Poll for job status

```bash
curl -H "X-API-Key: dev-secret-key" \
  http://localhost:8000/v1/generations/<JOB_ID>
```

If `status` is `succeeded`, you’ll get an `output_urls` array with a presigned download link.

### 3️⃣ Download the image

Open the presigned URL in a browser or use `curl` to download.

---

## 🗂️ MinIO Console

You can explore generated images in the MinIO web UI:

```
http://localhost:9001
```

Login with the credentials in `.env` (`MINIO_ROOT_USER` & `MINIO_ROOT_PASSWORD`).

---

## 🚀 Deployment Notes

* Change default credentials in `.env` before production
* Keep `.env` out of version control
* Swap MinIO for AWS S3, Cloudflare R2, or other S3-compatible storage for cloud deployment

---

💡 **Pro tip:** This backend is designed so the job → poll → download flow works the same in local dev or in production cloud setups.
