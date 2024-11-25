from __future__ import annotations
from typing import Dict, Any
from Lab4DB.app import db
from sqlalchemy import event, select

class Tasks(db.Model):
    __tablename__ = 'Tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(45), nullable=False)
    employee_id = db.Column(db.Integer, nullable=True)

    def __repr__(self) -> str:
        return f"Tasks(id={self.id}, title='{self.title}', status='{self.status}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'employee_id': self.employee_id,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Tasks:
        return Tasks(
            title=dto_dict.get('title'),
            description=dto_dict.get('description'),
            due_date=dto_dict.get('due_date'),
            status=dto_dict.get('status'),
            employee_id=dto_dict.get('employee_id'),
        )

@event.listens_for(Tasks, "before_insert")
def check_employee_exists(mapper, connection, target):
    """
    Перевірка, чи існує співробітник для задачі перед її додаванням.
    """
    employee_table = db.Table('employees', db.metadata, autoload_with=db.engine)

    employee_exists = connection.execute(
        select(employee_table.c.id).where(employee_table.c.id == target.employee_id)
    ).first()

    if not employee_exists:
        raise ValueError(f"Employee with id {target.employee_id} does not exist in employees table.")

