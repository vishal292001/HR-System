from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.crud.db_crud_operation import fetch_model_entries_sync
from app.db import get_db
from app.models import Employee, EmployeeStatus, OrganizationColumnConfig
from app.schema.employee_search_schema import EmployeeSearchRequest
from app.services.employee_search_service import employee_search_helper
from app.utils.api_request_handler import handle_api_request
from app.utils.model_utils import model_to_dict

hr_router = APIRouter()

@hr_router.get("/health")
async def health_check():
    return {
        "status_code": 200,
        "message": "Server is up and Running!"
    }


@hr_router.get("/api/employees/search")
def search_employees(request: Request, db: Session = Depends(get_db)):
    return handle_api_request(
        request=request,
        db=db,
        query_schema=EmployeeSearchRequest,
        helper_function=employee_search_helper,
    )


   