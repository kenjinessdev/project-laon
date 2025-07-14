# in routes/user.py or similar
from fastapi import APIRouter, Depends, Request, HTTPException
from src.dependencies.auth import get_current_user
from prisma.models import User
from prisma.errors import UniqueViolationError
from src.db.prisma import prisma
from src.models.user import UserUpdate, PasswordChangeRequest
from src.core.limiter import limiter
from src.utils.security import hash_password, verify_password

user_router = APIRouter()


@user_router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@user_router.put("/me", response_model=User)
@limiter.limit("5/minute")
async def update_profile(
    request: Request,
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    update_fields = update_data.dict(exclude_unset=True)

    # Check if email is changing and already taken
    if "email" in update_fields and update_fields["email"] != current_user.email:
        existing_email_user = await prisma.user.find_unique(where={"email": update_fields["email"]})
        if existing_email_user and existing_email_user.id != current_user.id:
            raise HTTPException(
                status_code=400, detail="Email is already registered.")

    # Check if phone number is changing and already taken
    if "phone_number" in update_fields and update_fields["phone_number"] != current_user.phone_number:
        existing_phone_user = await prisma.user.find_unique(where={"phone_number": update_fields["phone_number"]})
        if existing_phone_user and existing_phone_user.id != current_user.id:
            raise HTTPException(
                status_code=400, detail="Phone number is already registered.")

    # Try to perform the update
    try:
        updated_user = await prisma.user.update(
            where={"id": current_user.id},
            data=update_fields
        )
    except UniqueViolationError:
        raise HTTPException(
            status_code=400, detail="Email or phone number already in use.")

    return updated_user


@user_router.put("/me/password")
async def change_password(
    payload: PasswordChangeRequest,
    current_user: User = Depends(get_current_user)
):
    user = await prisma.user.find_unique(where={"id": current_user.id})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(payload.current_password, user.password):
        raise HTTPException(
            status_code=400, detail="Incorrect current password")

    new_hashed_password = hash_password(payload.new_password)

    await prisma.user.update(
        where={"id": current_user.id},
        data={"password": new_hashed_password}
    )

    return {"message": "Password updated successfully"}
