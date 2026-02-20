# SpendWisely API 💰
A secure, production-ready REST API for personal expense tracking. Built to demonstrate the transition from Data Science to robust Backend Engineering.

## 🚀 Key Features
* **Full CRUD Functionality**: Create, Read, Update, and Delete financial transactions.
* **JWT Authentication**: Secure user login and stateless authorization using OAuth2 with Bearer Tokens.
* **Row-Level Security**: Sophisticated ownership validation—users can only manage their own data.
* **Relational Database**: Powered by SQLite and SQLAlchemy ORM for reliable data persistence.

## 🛠️ Tech Stack
* **Framework**: FastAPI
* **Database**: SQLAlchemy (ORM), SQLite
* **Security**: Passlib (Bcrypt), Jose (JWT)
* **Validation**: Pydantic

## 💻 How to Run
1. Clone the repo: `git clone https://github.com/hasan-65-db/SpendWisely-API.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `uvicorn main:app --reload`
4. Access interactive docs: `http://127.0.0.1:8000/docs`