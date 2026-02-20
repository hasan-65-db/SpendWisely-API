from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy.orm import Session
from database import get_db,engine
import schemas,models,security,oauth2
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Response, Query
from sqlalchemy import or_, func
from datetime import date

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/expenses/",response_model=schemas.ResponseTransaction)
def post_expense(
    expense:schemas.CreateTransaction,
     db:Session=Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
    ):
      new_expense = models.Transaction(**expense.model_dump(), owner_id=current_user.id)
      db.add(new_expense)
      db.commit()
      db.refresh(new_expense)
      return new_expense

@app.post("/users/",response_model=schemas.ResponseUser)
def post_user(user:schemas.CreateUser, db:Session=Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=404, detail="User already registered on this email")
    hashed_pwd = security.get_password_hash(user.password)
    new_user = models.User(
        email = user.email,
        password = hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user or not security.verify_password(user_credentials.password,user.password):
        raise HTTPException(
            status_code=404,
            detail="Invalid Credentials"
        )
    access_token = security.create_access_token(data={"user_id":user.id})
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }
@app.delete("/expenses/{id}",status_code=204)
def delete_expense(
    id:int,
    db: Session=Depends(get_db),
    current_user_id=Depends(oauth2.get_current_user)
):
    expense_query = db.query(models.Transaction).filter(models.Transaction.id==id)
    expense = expense_query.first()
    if expense is None:
        raise HTTPException(status_code=404, detail=f"Expense not found at {id}")
    if int(expense.owner_id) != int(current_user_id.id):
        raise HTTPException(status_code=403,detail="Not authorized to perform this action!")
    
    expense_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204) #204 means success but nothing to show

@app.get("/expenses")
def get_expenses(
    # Move parameters without '=' or with simple defaults to the top
    search: str = "",
    start_date: date = None,
    end_date: date = None,
    min_price: int = 0,
    max_price: int = 1000000,
    sort: str = "desc",
    limit: int = 10,
    # Move dependencies to the bottom
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)
):
    # 1. Base query
    query = db.query(models.Transaction).filter(models.Transaction.owner_id == current_user.id)
    
    # 2. Price Range
    query = query.filter(models.Transaction.amount >= min_price, 
                         models.Transaction.amount <= max_price)
    
    # 3. Search
    if search:
        term = f"%{search}%"
        query = query.filter(or_(models.Transaction.title.ilike(term), 
                                 models.Transaction.category.ilike(term)))
    
    # 4. Date Filter (using func.date to handle timestamps)
    if start_date:
        query = query.filter(func.date(models.Transaction.created_at) >= start_date)
    if end_date:
        query = query.filter(func.date(models.Transaction.created_at) <= end_date)

    # 5. Sorting
    if sort == "desc":
        query = query.order_by(models.Transaction.amount.desc())
    else:
        query = query.order_by(models.Transaction.amount.asc())

    return query.limit(limit).all()
    
@app.put("/expenses/{expense_id}",response_model=schemas.ResponseTransaction)
def update_transaction(
    expense_id : int,
    transaction : schemas.CreateTransaction,
    db : Session = Depends(get_db),
    current_user_id = Depends(oauth2.get_current_user)
): 
    transaction_query = db.query(models.Transaction).filter(models.Transaction.id == expense_id)
    db_transaction = transaction_query.first()

    if db_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = "Transaction Not found!!")
    
    if db_transaction.owner_id != current_user_id.id:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform this action"
        )
    
    transaction_query.update(transaction.dict(), synchronize_session=False)

    db.commit()
    return transaction_query.first()
    
     