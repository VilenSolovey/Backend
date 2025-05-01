import mysql.connector
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Lab4DB.app.config.config import Config
from Lab4DB.app.auth.route import register_routes
import os
import sys
from mysql.connector import Error
print(sys.path)
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    register_routes(app)
    create_database()
    create_tables(app)
    populate_data()
    create_triggers()
    return app


def create_database():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='11111111',
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS Lab4DB")
        print("Database created successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def create_tables(app):
    with app.app_context():
        db.create_all()


def populate_data():
    sql_file_path = os.path.abspath('/Users/vilen/PycharmProjects/Lab4BD/Lab4DB/app/data.sql')
    if os.path.exists(sql_file_path):
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='11111111',
            database='Lab4DB'
        )
        cursor = connection.cursor()
        with open(sql_file_path, 'r') as sql_file:
            sql_text = sql_file.read()
            sql_statements = sql_text.split(';')
            for statement in sql_statements:
                statement = statement.strip()
                if statement:
                    try:
                        cursor.execute(statement)
                        connection.commit()
                    except mysql.connector.Error as error:
                        print(f"Error executing SQL statement: {error}")
                        connection.rollback()
        cursor.close()
        connection.close()


def create_triggers():
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='11111111',
        database='Lab4DB'
    )
    cursor = connection.cursor()

    cursor.execute("""
    DROP TRIGGER IF EXISTS check_phone_number_end
    """)
    cursor.execute("""
    CREATE TRIGGER check_phone_number_end
    BEFORE INSERT ON employees
    FOR EACH ROW
    BEGIN
        IF RIGHT(NEW.phone_number, 2) = '00' THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Phone number cannot end with two zeros';
        END IF;
    END
    """)

    cursor.execute("""
    DROP TRIGGER IF EXISTS prevent_update_employees
    """)
    cursor.execute("""
    CREATE TRIGGER prevent_update_employees
    BEFORE UPDATE ON employees
    FOR EACH ROW
    BEGIN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Modification of data is not allowed in employees table';
    END
    """)

    cursor.execute("""
    DROP TRIGGER IF EXISTS prevent_delete_software
    """)
    cursor.execute("""
    CREATE TRIGGER prevent_delete_software
    BEFORE DELETE ON Software
    FOR EACH ROW
    BEGIN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Deletion is not allowed in Software table';
    END
    """)

    connection.commit()
    cursor.close()
    connection.close()
