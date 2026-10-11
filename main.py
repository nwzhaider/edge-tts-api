import io
import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

app = FastAPI()

class TTSRequest(BaseModel):
    text: str
    voice: str = "ur-PK-AsadNeural"

@app.get("/")
def home():
    return {"status": "ok", "message": "Edge-TTS is live!"}

@app.post("/generate")
async def generate_audio(req: TTSRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    communicate = edge_tts.Communicate(req.text, req.voice)
    mp3_buffer = io.BytesIO()
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            mp3_buffer.write(chunk["data"])
            
    mp3_buffer.seek(0)
    return Response(content=mp3_buffer.read(), media_type="audio/mpeg")
