from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import torch
import io
from backend.architect import VGG
from fastapi.middleware.cors import CORSMiddleware
import base64
import cv2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = VGG("VGG16", 10)

model.load_state_dict(torch.load(r'C:\Users\thuyl\OneDrive - Trường ĐH CNTT - University of Information Technology\My documents\AI\ai-project\models\classifier_cifar10.pth',map_location=torch.device('cpu')))
model.eval()

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):

    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image = image.resize((32, 32)) 
    image = np.transpose(image, (2, 0, 1))  
    resize, draw = image_processing(image)
    
    image = np.array(image) / 255.0   
    
    image = torch.tensor(image, dtype=torch.float).unsqueeze(0)

    with torch.no_grad():
        prediction = model(image)
    predicted_class = prediction.argmax(dim=1)
    
    image = (image.squeeze(0) * 255).numpy().astype(np.uint8)
    image = np.transpose(image, (1, 2, 0))

    img_str = buffered(image)
    img_resize = buffered(resize)
    img_draw = buffered(draw)
    return JSONResponse(content={"prediction": predicted_class.item(), 
                                 "image": img_str,
                                 "resize_image": img_resize,
                                 "draw_image": img_draw})

def buffered(np_img):
    print("np shape", np_img.shape or len(np_img)) 
    
    np_img = Image.fromarray(np_img.astype('uint8'))
    
    buffered = io.BytesIO()
    np_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def image_processing(ori_image):
    ori_image = np.transpose(ori_image, (2, 1, 0))  
    cell_size = 10
    grid_size = 32

    width = cell_size * grid_size
    height = cell_size * grid_size

    resize = cv2.resize(ori_image, (width, height))
    draw = cv2.resize(ori_image, (width, height))

    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            cv2.rectangle(draw, (x, y), (x + cell_size, y + cell_size), (0, 0, 0), 1)  
    resize = np.rot90(resize, k=1, axes=(1,0))
    resize = np.fliplr(resize)
    draw = np.rot90(draw, k=1, axes=(1,0))
    draw = np.fliplr(draw)
    return resize, draw

