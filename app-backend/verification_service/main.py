import redis
import strawberry
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from .database import verify_doctor_id

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
r = redis.Redis(host="localhost", port=6379, decode_responses=True)


@strawberry.type
class VerificationResponse:
    success: bool
    message: str


@strawberry.type
class Query:
    @strawberry.field
    def verify_doctor_id(self, doctorid: str) -> VerificationResponse:
        try:
            if verify_doctor_id(doctorid):
                r.set(doctorid, "step1", ex=300)  
                return VerificationResponse(
                    success=True, message=f"{doctorid}: Doctor ID is valid"
                )
            return VerificationResponse(success=False, message="Invalid Doctor ID.")
        except Exception:
            return VerificationResponse(success=False, message="Error has occured. {e}")


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema=schema)

app.include_router(graphql_app, prefix="/graphql")
