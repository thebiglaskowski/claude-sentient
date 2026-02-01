# Snippet: fastapi-endpoint

## Description

FastAPI endpoint with proper validation, error handling, and async patterns using Pydantic models.

## When to Use

- Creating new Python API endpoints
- REST resource operations with FastAPI
- Async backend route handlers

## Code

```python
from fastapi import APIRouter, HTTPException, Query, Path, Depends
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from uuid import UUID

router = APIRouter(prefix="/resources", tags=["resources"])


# Pydantic models
class ResourceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    description: Optional[str] = Field(None, max_length=500)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Example Resource",
                "email": "example@test.com",
                "description": "A sample resource"
            }
        }


class ResourceResponse(BaseModel):
    id: UUID
    name: str
    email: str
    description: Optional[str]
    created_at: str


class PaginatedResponse(BaseModel):
    data: List[ResourceResponse]
    total: int
    page: int
    limit: int
    total_pages: int


# GET /resources
@router.get("/", response_model=PaginatedResponse)
async def list_resources(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    sort: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
):
    """List all resources with pagination."""
    result = await resource_service.find_all(
        page=page,
        limit=limit,
        sort=sort,
    )

    return PaginatedResponse(
        data=result.data,
        total=result.total,
        page=page,
        limit=limit,
        total_pages=(result.total + limit - 1) // limit,
    )


# GET /resources/{id}
@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: UUID = Path(..., description="Resource ID"),
):
    """Get a single resource by ID."""
    resource = await resource_service.find_by_id(resource_id)

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    return resource


# POST /resources
@router.post("/", response_model=ResourceResponse, status_code=201)
async def create_resource(data: ResourceCreate):
    """Create a new resource."""
    resource = await resource_service.create(data.model_dump())

    return resource


# PUT /resources/{id}
@router.put("/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: UUID = Path(..., description="Resource ID"),
    data: ResourceCreate = ...,
):
    """Update an existing resource."""
    resource = await resource_service.update(resource_id, data.model_dump())

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    return resource


# DELETE /resources/{id}
@router.delete("/{resource_id}", status_code=204)
async def delete_resource(
    resource_id: UUID = Path(..., description="Resource ID"),
):
    """Delete a resource."""
    deleted = await resource_service.delete(resource_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Resource not found")

    return None
```

### Dependency Injection Example

```python
# dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Validate JWT token and return current user."""
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return await user_service.find_by_id(user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


# Use in endpoint
@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user
```

## Customization Points

- `resource_service` — Replace with your service layer
- `ResourceCreate` / `ResourceResponse` — Adjust fields for your data
- Route prefix — Change `/resources` to your resource name
- Add authentication with `Depends(get_current_user)`

## Related Snippets

- [error-class](../utility/error-class.md) — Custom error classes
- [pytest-test](../testing/pytest-test.md) — Test this endpoint
