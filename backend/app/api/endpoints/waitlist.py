from typing import List, Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from app.api import deps
from app.core.config import settings
import pymongo

router = APIRouter()

myclient = pymongo.MongoClient(settings.MONGO_URI)
mydb = myclient["waitlist"]
mycol = mydb["waitlist"]

@router.post("/")
async def waitlist(user: List[str]) -> Dict[str, str]:
    """
    Waitlist endpoint.
    """

    mydict = { "name": user[0], "email": user[1], "organisation": user[2]}
    x = mycol.insert_one(mydict)

    return {"message": "Congrats. You have been added to the waitlist"}




