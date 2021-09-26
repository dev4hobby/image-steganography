import time
from fastapi import FastAPI, Form, File, Response
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from steganography import Steganography

start_time = time.time()
s = Steganography()
origins = [
    "http://localhost:3000",
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def read_root():
    return {"uptime": f"{str(round(time.time() - start_time, 1))} sec"}

@app.post('/hide')
async def hide(file: bytes = File(...), message: str = Form(...)) -> Response:
    image = s.hide_message_for_web(file, message)
    return Response(content=image, media_type='image/png')

@app.post('/seek')
async def seek(file: bytes = File(...)):
    message = s.seek_message_for_web(file)
    return {"message": message}




