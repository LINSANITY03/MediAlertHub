"""Main application module defining the GraphQL API for doctor ID verification."""

import uuid
import redis
import strawberry

from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from .database import get_id, get_username

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
class Body:
    """
    Body type returned in a successful verification response.
    """
    id:str
    step:int

@strawberry.type
class VerificationResponse:
    """
    Response type returned from doctor verification.
    """
    success: bool
    message: str
    body: Body | None = None


@strawberry.type
class Query:
    """
    Root GraphQL query class with doctor ID verification logic.
    """

    @strawberry.field
    def verify_doctor_id(self, doctorid: str) -> VerificationResponse:
        """
        Verifies if a doctor ID is valid UUID and exists in the database.

        Params:
            doctorid (str): The doctor's UUID string.

        Returns:
            VerificationResponse: Result of the verification.
        """
        print("asdasd", doctorid)
        try:
            # Validate UUID format first — this will raise ValueError if invalid
            uuid.UUID(doctorid)
            if get_id(doctorid):
                r.set(doctorid, 1, ex=300)
                return VerificationResponse(
                    success=True, message=f"{doctorid}: Doctor ID is valid",
                    body=Body(id=doctorid, step=1)
                )
            return VerificationResponse(success=False, message="Invalid Doctor ID.")
        except ValueError:
            return VerificationResponse(success=False, message="Doctor ID is not a valid UUID.")
        except Exception:
            return VerificationResponse(success=False,
                                        message="Something went wrong. Try again later.")
    
    @strawberry.field
    def verify_username(f_name: str, l_name: str, info: Info) -> VerificationResponse:
        
        try:
            request: Request = info.context["request"]
            headers = request.headers
            token = headers.get("authorization")
            print(token)
            if not token:
                raise HTTPException(status_code=401, detail="Token required")
            print(headers)
            
            if get_username(f_name, l_name):
                return VerificationResponse(
                    success=True, message="Username is valid",
                    # body=Body(id=doctorid, step=1)
                )
            return VerificationResponse(success=False, message="Invalid Username.")
        # except ValueError:
        #     return VerificationResponse(success=False, message="Doctor ID is not a valid UUID.")
        except HTTPException as e:
            return VerificationResponse(success=False,
                                        message=e.detail)
        except Exception:
            return VerificationResponse(success=False,
                                        message="Something went wrong. Try again later.")

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema=schema)

app.include_router(graphql_app, prefix="/graphql")
