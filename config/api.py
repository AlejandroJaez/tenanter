from ninja import NinjaAPI
from repairs.api import repairs_router

api_v1 = NinjaAPI()

api_v1.add_router(prefix="v1", router=repairs_router)


@api_v1.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}
