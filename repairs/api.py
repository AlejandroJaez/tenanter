import random

from ninja import Router

from repairs.schemas import UserSchema

repairs_router = Router()


@repairs_router.get("/")
def post_repair(request):
    return {"result": random.randint(0, 999999999999) + random.randint(0, 999999999999)}


@repairs_router.get("/me", response=UserSchema)
def me(request):
    return request.user
