import uuid
from pydantic import BaseModel
from datetime import datetime

class ActiveTimerRedis(BaseModel):
    start_time: datetime
    last_ping_at: datetime
    last_confirmed_at: datetime

class ActiveTimerRedisResponse(ActiveTimerRedis):
    task_id: uuid.UUID