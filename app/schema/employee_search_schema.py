from typing import Optional

from pydantic.v1 import BaseModel, constr, EmailStr, validator
import re



from pydantic import BaseModel, Field
from typing import Optional
from app.models import EmployeeStatus

class EmployeeSearchRequest(BaseModel):
    organization_id: int = Field(..., description="Organization ID")
    name: Optional[str] = Field(None, description="Employee name")
    department: Optional[str] = Field(None, description="Department name")
    position: Optional[str] = Field(None, description="Job position")
    location: Optional[str] = Field(None, description="Location of employee")
    status: Optional[EmployeeStatus] = Field(None, description="Employment status")
    offset: int = Field(0, ge=0, description="Offset for pagination")
    limit: int = Field(10, ge=1, le=100, description="Max number of results to return")
