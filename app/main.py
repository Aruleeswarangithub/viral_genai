import os
import uuid
from datetime import datetime

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import GenerateRequest
from services import generate_brand_text, enhance_prompt
from storage import ensure_storage, add_record, get_record, load_history
from jobs import process_generation_job

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="ViralGen AI Demo")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

ensure_storage()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/history-page", response_class=HTMLResponse)
async def history_page(request: Request):
    records = load_history()
    return templates.TemplateResponse("history.html", {"request": request, "records": records[:20]})


@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "ViralGen AI is running"}


@app.post("/api/generate")
async def generate(payload: GenerateRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    generated_text = generate_brand_text(
        payload.brand_name,
        payload.persona,
        payload.platform,
        payload.product_brief
    )

    enhanced_prompt = enhance_prompt(
        payload.product_brief,
        payload.persona,
        payload.platform
    )

    record = {
        "job_id": job_id,
        "brand_name": payload.brand_name,
        "persona": payload.persona,
        "platform": payload.platform,
        "product_brief": payload.product_brief,
        "generated_text": generated_text,
        "enhanced_prompt": enhanced_prompt,
        "image_url": None,
        "final_asset_url": None,
        "status": "queued",
        "created_at": now,
        "updated_at": now
    }

    add_record(record)
    background_tasks.add_task(process_generation_job, job_id, payload.persona, payload.platform)

    return JSONResponse({
        "job_id": job_id,
        "status": "queued",
        "generated_text": generated_text,
        "enhanced_prompt": enhanced_prompt
    })


@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    record = get_record(job_id)
    if not record:
        return JSONResponse({"error": "Job not found"}, status_code=404)
    return record


@app.get("/api/history")
async def history():
    return load_history()
