from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.services.calculation_factory import CalculationFactory
from app.services.stats import summarize_calculations
from app.security import get_current_user

router = APIRouter(
    prefix="/calculations",
    tags=["calculations"],
)

# =========================================================
# 1. STATS ROUTE  (MUST COME BEFORE /{calc_id})
# =========================================================
@router.get("/stats")
def get_calculation_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Returns summary statistics for this user's calculations.
    """
    calcs = (
        db.query(models.Calculation)
        .filter(models.Calculation.user_id == current_user.id)
        .all()
    )

    # Return plain dictionary (no response_model → no validation issues)
    return summarize_calculations(calcs)


# =========================================================
# 2. CREATE (POST /calculations)
# =========================================================
@router.post("/", response_model=schemas.CalculationRead, status_code=status.HTTP_201_CREATED)
def create_calculation(
    calc_in: schemas.CalculationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
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
        user_id=current_user.id,
    )
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc


# =========================================================
# 3. BROWSE (GET /calculations)
# =========================================================
@router.get("/", response_model=list[schemas.CalculationRead])
def get_calculations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Return only this user's calculations.
    """
    return (
        db.query(models.Calculation)
        .filter(models.Calculation.user_id == current_user.id)
        .all()
    )


# =========================================================
# 4. READ ONE (GET /calculations/{calc_id})
# MUST COME AFTER /stats
# =========================================================
@router.get("/{calc_id}", response_model=schemas.CalculationRead)
def get_calculation(
    calc_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    calc = (
        db.query(models.Calculation)
        .filter(
            models.Calculation.id == calc_id,
            models.Calculation.user_id == current_user.id,
        )
        .first()
    )
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc


# =========================================================
# 5. EDIT (PUT /calculations/{calc_id})
# =========================================================
@router.put("/{calc_id}", response_model=schemas.CalculationRead)
def update_calculation(
    calc_id: int,
    update: schemas.CalculationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    calc = (
        db.query(models.Calculation)
        .filter(
            models.Calculation.id == calc_id,
            models.Calculation.user_id == current_user.id,
        )
        .first()
    )
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

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


# =========================================================
# 6. DELETE (DELETE /calculations/{calc_id})
# =========================================================
@router.delete("/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(
    calc_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    calc = (
        db.query(models.Calculation)
        .filter(
            models.Calculation.id == calc_id,
            models.Calculation.user_id == current_user.id,
        )
        .first()
    )

    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    db.delete(calc)
    db.commit()
    return {"message": "Deleted"}
