# FastFeed (FastAPI Media Sharing App)

FastFeed is a full-stack media sharing platform built with a high-performance **FastAPI** backend and an interactive **Streamlit** frontend. It allows users to create accounts, upload images and videos (powered by ImageKit.io), and browse a global feed of media posts with captions.

## 🚀 Features

- **JWT Authentication:** Secure user registration, login, and session management using `fastapi-users`.
- **Media Uploads:** Seamless, asynchronous image and video uploads to a CDN using the **ImageKit v5 SDK**.
- **Global Feed:** View chronological posts from all users with auto-formatted images and blurred-background videos.
- **Access Control:** Users can only delete their own posts.
- **Async Database:** Uses asynchronous SQLAlchemy 2.0 with SQLite (easily translatable to PostgreSQL) for non-blocking database queries.

## 🛠️ Tech Stack

- **Backend:** FastAPI, Python 3.13
- **Frontend:** Streamlit
- **Database:** SQLite & aiosqlite (SQLAlchemy ORM)
- **Auth:** FastAPI Users (JWT Strategy)
- **Media Storage & CDN:** ImageKit.io
- **Dependency Management:** `uv`

## 💻 Local Development

### 1. Setup Environment
Clone the repository and install dependencies using `uv`:

```bash
git clone https://github.com/YOUR-USERNAME/fastfeed-app.git
cd fastfeed-app
uv sync
```

### 2. Environment Variables
Create a `.env` file in the root directory and add your ImageKit credentials:

```ini
IMAGEKIT_PRIVATE_KEY=your_private_key
IMAGEKIT_PUBLIC_KEY=your_public_key
IMAGEKIT_URL=https://ik.imagekit.io/your_id
```

### 3. Run the Backend
Start the FastAPI server:

```bash
uv run main.py
```
*The API will be available at `http://localhost:8000` and Swagger docs at `http://localhost:8000/docs`.*

### 4. Run the Frontend
In a separate terminal, start the Streamlit app:

```bash
uv run streamlit run frontend.py
```
*The web interface will open at `http://localhost:8501`.*

## ☁️ Deployment

- **Backend:** Designed to be easily deployed on Render as a Web Service.
- **Frontend:** Configured to deploy on Streamlit Community Cloud.
- **Dynamic Routing:** The frontend uses an `API_URL` environment variable to connect to the deployed backend automatically.
