from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import status
from typing import List, Dict
from datetime import datetime
from app.models import Employee, OrganizationColumnConfig, SearchLog
from app.schema.employee_search_schema import EmployeeSearchRequest
import json
import logging
import time

logger = logging.getLogger(__name__)

def employee_search_helper(db: Session, filter_data: EmployeeSearchRequest) -> Dict:
    start_time = time.time()
    try:
        logger.info(f"Received employee search request: {filter_data.dict()}")

        filters = []

        if filter_data.name:
            filters.append(Employee.name.ilike(f"%{filter_data.name}%"))
        if filter_data.department:
            filters.append(Employee.department == filter_data.department)
        if filter_data.position:
            filters.append(Employee.position == filter_data.position)
        if filter_data.location:
            filters.append(Employee.location == filter_data.location)
        if filter_data.status:
            filters.append(Employee.status == filter_data.status)
    
        # Query employees with filters
        query = db.query(Employee).filter(and_(*filters))
        total_count = query.count()



        #pagination
        employee_list: List[Employee] = query.offset(filter_data.offset).limit(filter_data.limit).all()

        # Get allowed columns for the organization
        config_entries = db.query(OrganizationColumnConfig).filter_by(
            organization_id=filter_data.organization_id,
            is_visible=1
        ).all()

        allowed_columns = [entry.column_name for entry in config_entries]

        # Serialize employees with only allowed columns
        serialized_employees = []
        for emp in employee_list:
            emp_dict = {}
            for col in allowed_columns:
                val = getattr(emp, col, None)
                emp_dict[col] = val.isoformat() if isinstance(val, datetime) else val
            serialized_employees.append(emp_dict)

        # Log the search
        db.add(SearchLog(
            organization_id=filter_data.organization_id,
            search_filters=json.dumps(filter_data.dict()),
            results_count=total_count,
            response_time_ms=round((time.time() - start_time) * 1000, 2)
        ))
        db.commit()

        logger.info(f"Search completed with {len(serialized_employees)} results.")
        return {
            "status": 200,
            "message": "Search completed successfully",
            "data": serialized_employees,
            "pagination": {
                "total": total_count,
                "offset": filter_data.offset,
                "limit": filter_data.limit,
            }
        }

    except SQLAlchemyError as e:
        logger.error(f"Database error during employee search: {str(e)}")
        db.rollback()
        return {
            "status": 500,
            "message": "Internal server error during database operation"
        }

    except Exception as e:
        logger.exception("Unexpected error occurred during employee search")
        return {
            "status": 500,
            "message": "An unexpected error occurred"
        }
