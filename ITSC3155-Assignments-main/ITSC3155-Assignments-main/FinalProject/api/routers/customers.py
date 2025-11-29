from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import customers as controller
from ..schemas import menu_item as schema
from ..dependencies.database import engine, get_db