from fastapi import APIRouter, HTTPException, Depends

from app.core.auth import get_current_user, admin_required
from app.core.db import get_db
from app.core.time import utc_now
from app.models.Company import CompanyCreate, CompanyResponse
from bson import ObjectId

router = APIRouter(prefix="/company", tags=["company"])

@router.post("/create-company", response_model=CompanyResponse)
async def create_company(company: CompanyCreate, db=Depends(get_db), current_user=Depends(get_current_user)):
    """
    Create a new company.
    """
    await admin_required(current_user)
    company_data = company.model_dump()
    company_data["created_at"] = utc_now()
    company_data["updated_at"] = utc_now()

    # Check if the company already exists
    existing_company = await db.company.find_one({"name": company.name})
    if existing_company:
        raise HTTPException(status_code=400, detail="Company already exists!")

    result = await db.company.insert_one(company_data)
    created_company = await db.company.find_one({"_id": result.inserted_id})

    created_company["id"] = str(created_company["_id"])

    return CompanyResponse(**created_company)

@router.get("/get-company/{company_name}", response_model=CompanyResponse)
async def get_company(company_name: str, db=Depends(get_db), current_user=Depends(get_current_user)):
    """
    Get a company by name.
    """
    await admin_required(current_user)
    company = await db.company.find_one({"name": company_name})
    if not company:
        raise HTTPException(status_code=404, detail="Company not found!")
    company["id"] = str(company["_id"])

    company["name"] = str(company["name"])
    return CompanyResponse(**company)

@router.put("/update-company/{company_id}", response_model=CompanyResponse)
async def update_company(company_id: str, company: CompanyCreate, db=Depends(get_db), current_user=Depends(get_current_user)):
    """
    Update a company by ID.
    """
    await admin_required(current_user)
    company_data = company.model_dump()
    company_data["updated_at"] = utc_now()

    result = await db.company.update_one({"_id": ObjectId(company_id)}, {"$set": company_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Company not found or no changes made!")

    updated_company = await db.company.find_one({"_id": ObjectId(company_id)})
    updated_company["id"] = str(updated_company["_id"])

    return CompanyResponse(**updated_company)

@router.delete("/delete-company/{company_id}", response_model=dict)
async def delete_company(company_id: str, db=Depends(get_db),current_user=Depends(get_current_user)):
    """
    Delete a company by ID.
    """
    await admin_required(current_user)
    result = await db.company.delete_one({"_id": ObjectId(company_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Company not found!")

    return {"message": "Company deleted successfully!"}
