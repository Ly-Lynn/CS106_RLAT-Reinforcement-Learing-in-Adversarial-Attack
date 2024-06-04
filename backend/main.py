from fastapi import FastAPI, File, UploadFile, Request, Response
from fastapi.responses import StreamingResponse, JSONResponse
from PIL import Image
import numpy as np
import uuid
import torch
import io
# from backend.architect import VGG
from fastapi.middleware.cors import CORSMiddleware
import base64
import cv2
import json
import asyncio
from tqdm import tqdm
from collections import deque
from adversarial_attack.agent import Agent
from adversarial_attack.arch import *
from adversarial_attack.config import *
from adversarial_attack.dataset import *

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust according to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def buffered(np_img):
    
    # print("buffer input", np_img)
    np_img = Image.fromarray(np_img.astype('uint8'))
    
    buffered = io.BytesIO()
    np_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def image_processing(ori_image):
    # print("np shape", ori_image.shape or len(ori_image)) 
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

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):

    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image = image.resize((32, 32)) 
    image = np.transpose(image, (2, 0, 1))  
    resize, draw = image_processing(image)
    
    image = np.array(image) / 255.0   
    
    image = torch.tensor(image, dtype=torch.float).unsqueeze(0)
    
    image = (image.squeeze(0) * 255).numpy().astype(np.uint8)
    image = np.transpose(image, (1, 2, 0))

    img_str = buffered(image)
    img_resize = buffered(resize)
    img_draw = buffered(draw)
    return JSONResponse(content={"image": img_str,
                                 "resize_image": img_resize,
                                 "draw_image": img_draw})



attack_states = {}
act_list = []

async def attack_generator(session_id):
    agent, current_state, l2_norm, image_clone, pred, P_pred, attack_state, image, actions_list = attack_states[session_id]
    # print("clone inside", image_clone)

    for step in range(agent.max_iter + 1):
        attack_state["step"] = step
        yield f'data: {json.dumps(attack_state)}\n\n'
        
        if step == agent.max_iter:
            attack_state["success"] = 0
            yield f'data: {json.dumps(attack_state)}\n\n'
            await asyncio.sleep(0.25)
            break

        action = agent.select_action_model(current_state, "test")

        act_list.append(action)
        
        image_clone = agent.make_action(image_clone, action)
        l2_norm = agent.cal_l2(image_clone, image)
        actions_list.append(action)
        P_noise_pred = agent.classifier(image_clone.unsqueeze(0).cuda()).cpu()[0]
        noise_pred = P_noise_pred[torch.argmax(P_noise_pred).item()]

        if torch.argmax(P_noise_pred).item() != pred:
            attack_state["success"] = 1
            np_image = image_clone.numpy()
            attack_img, grid = image_processing(np_image)
            attack_img, grid = buffered(attack_img * 255), buffered(grid * 255)
            attack_state.update({
                "attacked": attack_img,
                "grid": grid,
                "prob": P_noise_pred.detach().numpy().tolist(),
                "pred": noise_pred.detach().numpy().tolist(),
                "l2": l2_norm
            })
            yield f'data: {json.dumps(attack_state)}\n\n'
            await asyncio.sleep(0.25)
            break
        else:
            attack_state["success"] = -1
            np_image = image_clone.numpy()
            attack_img, grid = image_processing(np_image)
            attack_img, grid = buffered(attack_img * 255), buffered(grid * 255)
            attack_state.update({
                "attacked": attack_img,
                "grid": grid,
                "prob": P_noise_pred.detach().numpy().tolist(),
                "pred": noise_pred.detach().numpy().tolist(),
                "l2": l2_norm
            })
            yield f'data: {json.dumps(attack_state)}\n\n'
            await asyncio.sleep(0.25)

        sensities = agent.cal_sensities(image_clone, P_pred, pred)
        features = agent.classifier.features(image_clone.unsqueeze(0).cuda()).view(-1).cpu()
        next_state = torch.cat((features, sensities, torch.flatten(torch.tensor(actions_list))))
        current_state = next_state
    

@app.post('/attack')
async def start_attack(request: Request):
    try:
        attack_state = {
            "attacked": None,
            "grid": None,
            "success": -1,
            "prob": None,
            "pred": None,
            "l2": None,
            "step": -1
        }
        data = await request.json()
        image_data = data.get('image')
        if image_data.startswith('data:image'):
            _, image_data = image_data.split(',', 1)
        
        decoded_image = base64.b64decode(image_data)

        image = Image.open(io.BytesIO(decoded_image))
        agent = Agent(True)
        agent.policy_net.load_state_dict(torch.load(DQN_TRAINED))
        image = transforms.ToTensor()(image).unsqueeze(0)
        
        image_clone = image.clone()
        P_GT = agent.classifier(image.cuda()).cpu()
        pred = torch.argmax(P_GT).item()
        P_pred = P_GT[0][pred]
        
        actions_list = deque([0.002, 0.003, 0.004, 0.005], maxlen=4)
        sensities = agent.cal_sensities(image_clone, P_pred, pred)
        features = agent.classifier.features(image_clone.cuda()).view(-1).cpu()
        current_state = torch.cat((features, sensities, torch.flatten(torch.tensor(actions_list))))
        l2_norm = agent.cal_l2(image_clone, image)


        image_np = image_clone.numpy().squeeze(axis=0)
        # print("np clone", image_np, image_clone,  sep='\n')
        attack_img, grid = image_processing(image_np)
        attack_img, grid = buffered(attack_img * 255), buffered(grid * 255)
        # print("outside attack img", attack_img)
        attack_state.update({
            "attacked": attack_img,
            "grid": grid,
            "prob": P_GT.detach().numpy().tolist(),
            "pred": P_pred.detach().numpy().tolist(),
            "l2": l2_norm
        })

        session_id = str(uuid.uuid4())
        attack_states[session_id] = (agent, current_state, l2_norm, image_clone, pred, P_pred, attack_state, image, actions_list)
        
        return JSONResponse(content={"session_id": session_id}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get('/attack/{session_id}')
async def get_attack(session_id: str):
    try:
        if session_id not in attack_states:
            return JSONResponse(content={"error": "Session ID not found"}, status_code=404)
        return StreamingResponse(attack_generator(session_id), media_type="text/event-stream")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
