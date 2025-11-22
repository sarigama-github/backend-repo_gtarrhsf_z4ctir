from typing import Any, Dict, List, Optional
import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(DATABASE_URL)
    return _client


def get_db() -> AsyncIOMotorDatabase:
    global _db
    if _db is None:
        _db = get_client()[DATABASE_NAME]
    return _db


async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = get_db()
    data_with_meta = {**data, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
    res = await db[collection_name].insert_one(data_with_meta)
    return {"id": str(res.inserted_id), **data_with_meta}


async def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 20) -> List[Dict[str, Any]]:
    db = get_db()
    cursor = db[collection_name].find(filter_dict or {}).limit(limit)
    results: List[Dict[str, Any]] = []
    async for doc in cursor:
        doc["id"] = str(doc.get("_id"))
        doc.pop("_id", None)
        results.append(doc)
    return results
