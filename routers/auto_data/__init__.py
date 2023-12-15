from fastapi.routing import APIRouter

router = APIRouter(prefix='/auto_data')

from . import vehicle