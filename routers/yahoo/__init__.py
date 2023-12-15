from fastapi.routing import APIRouter

router = APIRouter(prefix='/yahoo')

from . import vehicle