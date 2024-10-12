from fastapi import FastAPI, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import AnimalImage
from PIL import Image, ImageOps
from io import BytesIO
import requests
import base64
import random
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

ANIMAL_URLS = {
    "duck": "https://random-d.uk/api/randomimg",
    "dog": "https://place.dog",
    "bear": "https://placebear.com"
}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fetch_and_resize_image(animal_type, size=(200, 200)):
    # Determine the image URL based on animal type
    if animal_type == "duck":
        url = ANIMAL_URLS[animal_type]
    else:
        # Generate random dimensions between 200 and 600
        width = random.randint(300, 700)
        height = random.randint(300, 700)
        url = f"{ANIMAL_URLS[animal_type]}/{width}/{height}"

    # Fetch and resize the image
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        
        # Convert image to RGB if it's not in a format compatible with JPEG
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize image while maintaining the aspect ratio
        img.thumbnail(size, Image.LANCZOS)
        
        # Create a new blank canvas with the target size and paste the resized image on it
        background = Image.new("RGB", size, (255, 255, 255))  # white background
        img_x = (size[0] - img.width) // 2
        img_y = (size[1] - img.height) // 2
        background.paste(img, (img_x, img_y))
        
        buffer = BytesIO()
        background.save(buffer, format="JPEG")
        buffer.seek(0)
        return buffer

@app.post("/save/{animal_type}/{count}")
async def save_images(animal_type: str, count: int, db: Session = Depends(get_db)):
    if animal_type not in ANIMAL_URLS:
        raise HTTPException(status_code=400, detail="Animal type not supported.")
    
    images = []
    for _ in range(count):
        resized_image = fetch_and_resize_image(animal_type)
        if resized_image:
            image_base64 = base64.b64encode(resized_image.getvalue()).decode('utf-8')
            new_image = AnimalImage(animal_type=animal_type, image_url=image_base64)
            db.add(new_image)
            db.commit()
            db.refresh(new_image)
            images.append(new_image)
    return {"message": f"Saved {count} images", "images": images}

@app.get("/last/{animal_type}")
async def get_last_image(animal_type: str, db: Session = Depends(get_db)):
    image = db.query(AnimalImage).filter(AnimalImage.animal_type == animal_type).order_by(AnimalImage.id.desc()).first()
    if not image:
        raise HTTPException(status_code=404, detail="No images found.")
    return {"animal_type": image.animal_type, "image_url": image.image_url}

@app.get("/all")
async def get_all_images(db: Session = Depends(get_db)):
    images = db.query(AnimalImage).all()
    if not images:
        raise HTTPException(status_code=404, detail="No images found.")
    
    # Return a list of images with their animal types
    return {"images": [{"animal_type": image.animal_type, "image_url": image.image_url} for image in images]}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
