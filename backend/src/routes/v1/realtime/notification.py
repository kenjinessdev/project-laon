# routes/realtime/notifications.py

from fastapi import WebSocketDisconnect
from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    Query
)
from broadcaster import Broadcast
from src.db.prisma import prisma as db
from src.models.notification import NotificationPayload
from jose import jwt, JWTError
from src.core.config import settings
import json
import uuid

router = APIRouter()

broadcast = Broadcast(settings.REDIS_URL)

INSTANCE_ID = str(uuid.uuid4())
clients = set()


@router.on_event("startup")
async def startup():
    await broadcast.connect()


@router.on_event("shutdown")
async def shutdown():
    await broadcast.disconnect()


# @router.websocket("/ws/notifications")
# async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
#     try:
#         # Decode and validate JWT
#         payload = jwt.decode(token, settings.JWT_SECRET,
#                              algorithms=[settings.JWT_ALGORITHM])
#         user_id = payload.get("sub")
#
#         if not user_id:
#             await websocket.close(code=1008, reason="Missing user_id")
#             return
#
#         await websocket.accept()
#         clients.add(websocket)
#
#         async with broadcast.subscribe(channel="notifications") as subscriber:
#             try:
#                 async for event in subscriber:
#                     # Broadcast to all connected clients
#                     for client in clients.copy():
#                         try:
#                             await client.send_text(event.message)
#                         except Exception:
#                             clients.remove(client)
#             except WebSocketDisconnect:
#                 clients.remove(websocket)
#
#     except JWTError:
#         await websocket.close(code=1008, reason="Invalid or expired token")


INSTANCE_ID = str(uuid.uuid4())  # Unique per FastAPI server instance
clients = set()


@router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    try:
        # Decode and validate JWT
        payload = jwt.decode(token, settings.JWT_SECRET,
                             algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            await websocket.close(code=1008, reason="Missing user_id")
            return

        await websocket.accept()
        clients.add(websocket)

        async with broadcast.subscribe(channel="notifications") as subscriber:
            try:
                async for event in subscriber:
                    try:
                        # Split message to get sender_id and content
                        sender_id, message = event.message.split(":", 1)
                        if sender_id == INSTANCE_ID:
                            continue  # Skip our own message

                        # Send to all connected clients
                        for client in clients.copy():
                            try:
                                await client.send_text(message)
                            except Exception:
                                clients.remove(client)
                    except Exception:
                        continue
            except WebSocketDisconnect:
                clients.remove(websocket)

    except JWTError:
        await websocket.close(code=1008, reason="Invalid or expired token")


@router.post("/send-notification")
async def send_notification(payload: NotificationPayload):
    await _send_notification(payload)
    return {"status": "Notification sent"}


async def _send_notification(payload: NotificationPayload):
    try:
        serialized_data = json.dumps(
            payload["data"]) if payload.get("data") else None
    except TypeError:
        raise HTTPException(status_code=400, detail="Invalid data payload")

    data = {
        "title": payload["title"],
        "message": payload["message"],
        "user_id": payload["user_id"],
        "actor_id": payload["actor_id"],
        "type": payload["type"],
        "data": serialized_data,
    }

    await db.notification.create(data=data)
    await broadcast.publish(
        channel="notifications",
        message=json.dumps(data)
    )
