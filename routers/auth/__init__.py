from fastapi.routing import APIRouter

router = APIRouter(prefix='/auth')

from . import user