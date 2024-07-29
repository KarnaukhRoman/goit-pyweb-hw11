from fastapi import FastAPI

from src.routes.route_contacts import router as router_contacts

app = FastAPI()

app.include_router(router_contacts, prefix="/contacts", tags=["contacts"])
