from fastapi.routing import APIRouter

router = APIRouter(prefix='/tire_rack')

from . import vehicle