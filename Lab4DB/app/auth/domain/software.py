from __future__ import annotations
from typing import Dict, Any
from time import time
from Lab4DB.app import db
from random import randint, choice
from sqlalchemy import text
class Software(db.Model):
    __tablename__ = 'Software'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    version = db.Column(db.String(45), nullable=True)
    locations_id = db.Column(db.Integer, db.ForeignKey('Locations.id'), nullable=True)

    location = db.relationship('Locations', back_populates='softwares')
    issues = db.relationship('SoftwareIssues', back_populates='software', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"Software({self.id}, name='{self.name}', version='{self.version}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'locations_id': self.locations_id,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Software:
        return Software(
            name=dto_dict.get('name'),
            version=dto_dict.get('version'),
            locations_id=dto_dict.get('locations_id'),
        )


def create_dynamic_databases_from_software():
    softwares = Software.query.all()
    if not softwares:
        return "No software found in the database."

    created_databases = []
    for software in softwares:
        db_name = software.name.replace(" ", "_")
        db_name = f"{db_name}_{int(time())}"
        table_count = randint(1, 9)

        create_db_sql = text(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        db.session.execute(create_db_sql)
        db.session.commit()

        created_tables = []
        for i in range(table_count):
            table_name = f"{db_name}_{i + 1}"
            column_defs = []
            for j in range(randint(1, 9)): 
                column_name = f"column_{j + 1}"
                column_type = choice(["INT", "VARCHAR(255)", "DATE"])
                column_defs.append(f"{column_name} {column_type}")
            column_defs_str = ", ".join(column_defs)
            create_table_sql = text(
                f"CREATE TABLE IF NOT EXISTS {db_name}.{table_name} (id INT PRIMARY KEY AUTO_INCREMENT, {column_defs_str});")
            db.session.execute(create_table_sql)
            db.session.commit()
            created_tables.append(table_name)

        created_databases.append({"database": db_name, "tables": created_tables})

    return created_databases