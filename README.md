# 🛠️ IT Service Request Manager(Flask + SQLAlchemy)

This backend project helps manage equipment and software issue tickets in an IT company. Employees can create requests when something breaks, needs replacement, or when software doesn’t work properly.

## 🧰 Technologies Used

- Python 3
- Flask
- Flask-SQLAlchemy
- MySQL (via `mysql-connector-python`)

## 🧾 Main Features

- Employees can create problem tickets
- Each ticket includes:
  - Description of the issue
  - Location of the equipment (office, room, workplace)
  - Date/time of creation
  - One or more responsible workers
- Tickets have:
  - **Status** 
  - **Priority** 
- You can add, update, delete, and view records
- Triggers and cursors are used to automate logic in the database

## ▶️ How to Run the Project

```
git clone https://github.com/VilenSolovey/Backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```
