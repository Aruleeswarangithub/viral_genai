import time
from datetime import datetime
from storage import update_record
from services import choose_demo_image


def process_generation_job(job_id: str, persona: str, platform: str):
    update_record(job_id, {
        "status": "processing",
        "updated_at": datetime.utcnow().isoformat()
    })

    time.sleep(4)

    image_url = choose_demo_image(persona, platform)

    update_record(job_id, {
        "status": "completed",
        "image_url": image_url,
        "final_asset_url": image_url,
        "updated_at": datetime.utcnow().isoformat()
    })
