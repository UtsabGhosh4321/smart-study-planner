from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schema import UserCreate
from app.core.database import db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()


# ===============================
# ✅ REGISTER USER
# ===============================
@router.post("/register")
async def register(user: UserCreate):

    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(user.password)

    # Create user document
    new_user = {
        "email": user.email,
        "password": hashed_password
    }

    # Insert into MongoDB
    await db.users.insert_one(new_user)

    return {"message": "User registered successfully"}


# ===============================
# ✅ LOGIN USER
# ===============================
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    # Find user by email (username field contains email)
    user = await db.users.find_one({"email": form_data.username})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Safety check (prevents KeyError crash)
    if "password" not in user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User data corrupted. Please re-register."
        )

    # Verify password
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = create_access_token(
        data={"sub": user["email"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }