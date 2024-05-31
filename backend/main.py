from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import torch
import io

app = FastAPI()

# Load mô hình đã huấn luyện bằng PyTorch
model = torch.load(r'C:\Users\thuyl\OneDrive - Trường ĐH CNTT - University of Information Technology\My documents\AI\project\models\classifier_cifar10.pth', map_location=torch.device('cpu'))

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI classification app!"}

@app.get("/favicon.ico")
async def get_favicon():
    return {"favicon": "not available"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Đọc file ảnh
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image = image.resize((224, 224))  # Điều chỉnh kích thước ảnh cho phù hợp với model của bạn
    image = np.array(image) / 255.0   # Chuẩn hóa ảnh
    image = np.transpose(image, (2, 0, 1))  # Chuyển đổi kích thước ảnh

    # Chuyển đổi sang tensor và thêm batch dimension
    image = torch.tensor(image, dtype=torch.float).unsqueeze(0)

    # Dự đoán
    prediction = model(image)
    predicted_class = prediction.argmax(dim=1)

    return JSONResponse(content={"prediction": int(predicted_class)})
