from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.crud.db_crud_operation import fetch_model_entries_sync
from app.db import get_db
from app.models import Employee, EmployeeStatus, OrganizationColumnConfig
from app.utils.model_utils import model_to_dict

hr_router = APIRouter()

@hr_router.get("/health")
async def health_check():
    return {
        "status_code": 200,
        "message": "Server is up and Running!"
    }

@hr_router.get("/api/employees/search")
def search_employees(
    request: Request,
    db: Session = Depends(get_db),
    organization_id: int = Query(..., description="Organization ID"),
    name: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    position: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    status: Optional[EmployeeStatus] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    try:
        # Step 1: Clean filters
        filters = {
            "organization_id": organization_id,
            "name": name,
            "department": department,
            "position": position,
            "location": location,
            "status": status.value if status else None
        }
        filters = {k: v for k, v in filters.items() if v is not None}

        # Step 2: Fetch employee records
        employee_details = fetch_model_entries_sync(
            db, model=Employee, filter_data=filters
        )

        if not employee_details:
            return JSONResponse(
                status_code=200,
                content={
                    "status": 200,
                    "message": "No employees found",
                    "data": [],
                    "count": 0
                }
            )

        # Step 3: Fetch allowed visible columns for org
        visible_columns = fetch_model_entries_sync(
            db,
            model=OrganizationColumnConfig,
            filter_data={"organization_id": organization_id, "is_visible": 1}
        )

        if not visible_columns:
            return JSONResponse(
                status_code=400,
                content={
                    "status": 400,
                    "message": "Organization column configuration not found.",
                    "data": [],
                    "count": 0
                }
            )

        allowed_columns = [entry.column_name for entry in visible_columns]

        # Step 4: Format employee result
        employees = []
        for emp in employee_details:
            try:
                # Try using helper if defined
                emp_dict = model_to_dict(emp, allowed_fields=allowed_columns)
            except Exception:
                # Fallback to manual dict build
                emp_dict = {}
                for col in allowed_columns:
                    if hasattr(emp, col):
                        val = getattr(emp, col)
                        emp_dict[col] = val.isoformat() if isinstance(val, date) else val
            employees.append(emp_dict)

        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "message": "Employees fetched successfully",
                "data": employees,
                "count": len(employees)
            }
        )

    except Exception as e:
        # Catch-all fallback for unexpected issues
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "message": f"An unexpected error occurred: {str(e)}",
                "data": [],
                "count": 0
            }
        )
