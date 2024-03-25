from fastapi import APIRouter, Depends

from komodo.models.framework.appliance_runtime import ApplianceRuntime
from komodo.server.globals import get_email_from_header, get_appliance

router = APIRouter(
    prefix='/api/v1/user',
    tags=['User']
)


@router.get("/profile", response_model=dict, summary="Get user profile.", description="Get user profile.")
async def get_user_profile(email: str = Depends(get_email_from_header), appliance=Depends(get_appliance)):
    runtime = ApplianceRuntime(appliance)
    user = runtime.get_user(email)
    return user.to_dict() if user else {"error": "User not found."}
