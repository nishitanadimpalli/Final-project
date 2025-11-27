# app/routers/calculations.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.services.calculation_factory import CalculationFactory

router = APIRouter(
    prefix="/calculations",
    tags=["calculations"],
)


# ⭐ 1) CREATE calculation
@router.post("/", response_model=schemas.CalculationRead, status_code=status.HTTP_201_CREATED)
def create_calculation(calc_in: schemas.CalculationCreate, db: Session = Depends(get_db)):
    # use factory to get the right operation
    op = CalculationFactory.get_operation(calc_in.type)

    try:
        result = op.compute(calc_in.a, calc_in.b)
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")

    db_calc = models.Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type,
        result=result,
    )
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc


# ⭐ 2) BROWSE all calculations
@router.get("/", response_model=list[schemas.CalculationRead])
def get_calculations(db: Session = Depends(get_db)):
    return db.query(models.Calculation).all()


# ⭐ 3) READ one calculation (by ID)
@router.get("/{calc_id}", response_model=schemas.CalculationRead)
def get_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc


# ⭐ 4) EDIT calculation (PUT)
# ⭐ 4) EDIT calculation (PUT)
@router.put("/{calc_id}", response_model=schemas.CalculationRead)
def update_calculation(calc_id: int, update: schemas.CalculationCreate, db: Session = Depends(get_db)):

    calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    # use factory + compute(), same as POST
    op = CalculationFactory.get_operation(update.type)
    try:
        new_result = op.compute(update.a, update.b)
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")

    calc.a = update.a
    calc.b = update.b
    calc.type = update.type
    calc.result = new_result

    db.commit()
    db.refresh(calc)
    return calc

# ⭐ 5) DELETE calculation
@router.delete("/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calc_id: int, db: Session = Depends(get_db)):

    calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    db.delete(calc)
    db.commit()

    return {"message": "Deleted successfully"}
