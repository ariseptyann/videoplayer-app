from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os

app = FastAPI(title="Video Player API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],  # Vue.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pastikan folder static/videos ada
os.makedirs("static/videos", exist_ok=True)

# Mount static directory untuk video
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return {"message": "Video Player API is running"}

@app.get("/api/video-info")
async def get_video_info():
    video_path = "static/videos"
    # Cek apakah ada video di folder
    try:
        videos = [f for f in os.listdir(video_path) if f.endswith(('.mp4', '.webm'))]
        if not videos:
            raise HTTPException(status_code=404, detail="No video files found")
        
        # Gunakan video pertama yang ditemukan
        video_file = videos[0]
        return {
            "url": f"/static/videos/{video_file}",
            "name": video_file,
            "duration": None  # Bisa ditambahkan logika untuk mendapatkan durasi video
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Video directory not found")

@app.get("/api/qr-data")
async def get_qr_data():
    # URL yang akan di-encode ke dalam QR code
    return {
        "url": "https://ngobrolinhpv.com/",
        "title": "Scan untuk mengunjungi website"
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)