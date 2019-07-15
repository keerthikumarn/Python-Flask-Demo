from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)


class Employee(db.Model):
    __tablename__ = "Employee"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    empNo = db.Column(db.Integer, nullable=False)
    designation = db.Column(db.String(50), nullable=False)

    def add_employee(name, empNo, designation):
        newEmployee = Employee(name=name, empNo=empNo, designation=designation)
        db.session.add(newEmployee)
        db.session.commit()

    def get_employees():
        return [Employee.json(emp) for emp in Employee.query.all()]

    def get_employee(empNo):
        return Employee.query.filter_by(empNo=empNo).first()

    def update_emp_name(empNo, name):
        emp = Employee.query.filter_by(empNo=empNo).first()
        emp.name = name
        db.session.commit()

    def update_emp_desg(empNo, designation):
        emp = Employee.query.filter_by(empNo=empNo).first()
        emp.designation = designation
        db.session.commit()

    def replace_emp(name, empNo, designation):
        emp = Employee.query.filter_by(empNo=empNo).first()
        emp.name = name
        emp.designation = designation
        db.session.commit()

    def delete_employee(empNo):
        Employee.query.filter_by(empNo=empNo).delete()
        db.session.commit()

    def json(self):
        return {'name': self.name, 'empNo': self.empNo, 'designation': self.designation}

    def __repr__(self):
        employee_object = {
            "name": self.name,
            "empNo": self.empNo,
            "designation": self.designation
        }
        return json.dumps(employee_object)
