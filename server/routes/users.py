from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import shutil
import os
import uuid
from server.model.user import User
from server.config.database import get_db


router = APIRouter()

@router.get('/users')
def get_users():
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}

@router.get('/login')
def login():
    
    pass