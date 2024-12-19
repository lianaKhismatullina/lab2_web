from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

class ZodiacBase(BaseModel):
    name: str
    description: str
    popularity: int

class ZodiacCreate(ZodiacBase):
    pass

class Zodiac(ZodiacBase):
    id: int

ZODIAC_DB: List[Zodiac] = [
    Zodiac(id=1, name="Овен", description="Овны известны своим энтузиазмом и смелостью.", popularity=12),
    Zodiac(id=2, name="Телец", description="Тельцы ценят стабильность и безопасность в жизни.", popularity=10),
    Zodiac(id=3, name="Близнецы", description="Близнецы любознательны и адаптивны, всегда готовы учиться.", popularity=8),
    Zodiac(id=4, name="Рак", description="Раки очень интуитивны и сентиментальны.", popularity=9),
    Zodiac(id=5, name="Лев", description="Львы драматичны, творчески и самоуверенны.", popularity=11),
    Zodiac(id=6, name="Дева", description="Девы практичны, верны и аналитичны.", popularity=7),
    Zodiac(id=7, name="Весы", description="Весы известны своим балансом, справедливостью и общительностью.", popularity=6),
    Zodiac(id=8, name="Скорпион", description="Скорпионы страстны, трудолюбивы и смелы.", popularity=5),
    Zodiac(id=9, name="Стрелец", description="Стрельцы оптимистичны, авантюрны и интеллектуальны.", popularity=4),
    Zodiac(id=10, name="Козерог", description="Козероги дисциплинированы, ответственны и амбициозны.", popularity=3),
    Zodiac(id=11, name="Водолей", description="Водолеи независимы, оригинальны и гуманитарны.", popularity=2),
    Zodiac(id=12, name="Рыбы", description="Рыбы сострадательны, артистичны и интуитивны.", popularity=1),
]

app = FastAPI()

@app.get("/")
def dead_root():
    return {}

@app.get("/zodiacs/", response_model=List[Zodiac])
def read_zodiacs():
    return ZODIAC_DB

@app.get("/zodiacs/{id}", response_model=Zodiac)
def read_zodiac(id: int):
    for zodiac in ZODIAC_DB:
        if zodiac.id == id:
            return zodiac
    raise HTTPException(status_code=404, detail="Zodiac sign not found")

@app.post("/zodiacs/", response_model=Zodiac)
async def create_zodiac(zodiac: ZodiacCreate):
    new_id = max(z.id for z in ZODIAC_DB) + 1 if ZODIAC_DB else 1
    new_zodiac = Zodiac(id=new_id, **zodiac.dict())
    ZODIAC_DB.append(new_zodiac)
    return new_zodiac

@app.put("/zodiacs/{zodiac_id}", response_model=Zodiac)
async def update_zodiac(zodiac_id: int, updated_zodiac: ZodiacCreate):
    for zodiac in ZODIAC_DB:
        if zodiac.id == zodiac_id:
            zodiac.name = updated_zodiac.name
            zodiac.description = updated_zodiac.description
            zodiac.popularity = updated_zodiac.popularity
            return zodiac
    raise HTTPException(status_code=404, detail="Zodiac sign not found")

@app.delete("/zodiacs/{zodiac_id}")
async def delete_zodiac(zodiac_id: int):
    global ZODIAC_DB
    ZODIAC_DB = [zodiac for zodiac in ZODIAC_DB if zodiac.id != zodiac_id]
    return {"message": "Zodiac sign deleted"}

if name == "main":
    uvicorn.run(app, host='127.0.0.1', port=8000)