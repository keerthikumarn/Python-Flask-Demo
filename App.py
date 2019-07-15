from flask import Flask, jsonify, request, Response
import json
from settings import *
from EmployeeModel import *
import jwt
import datetime

DEFAULT_PAGE_LIMIT = 3
app.config['SECRET_KEY'] = 'keerthi'

'''employees = [
    {
        'name': 'Keerthi Kumar N',
        'empNo': 700460,
        'designation': "L4"
    },
    {
        'name': 'Raghavendra Nayak',
        'empNo': 700337,
        'designation': "L0"
    },
    {
        'name': 'Tarun Sharma',
        'empNo': 701250,
        'designation': "L2"
    },
    {
        'name': 'Harshal Chardava',
        'empNo': 701260,
        'designation': "L2"
    }
]'''


def isValidEmpObject(empObject):
    if("name" in empObject and "designation" in empObject and "empNo" in empObject):
        return True
    else:
        return False


@app.route('/login')
def get_token():
    exp_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
    token = jwt.encode({'exp': exp_date}, app.config['SECRET_KEY'], algorithm='HS256')
    return token


@app.route('/employees')
def get_employees():
    token = request.args.get('token')
    try:
        jwt.decode(token, app.config['SECRET_KEY'])
    except:
        return jsonify({'error': 'Need a valid token to access this page !'})
    return jsonify({'employees': Employee.get_employees()})


@app.route('/employees', methods=['POST'])
def add_employee():
    if request.method == "POST":
        requestData = request.get_json()
        if(isValidEmpObject(requestData)):
            '''newEmployee = {
                'name': requestData['name'],
                'empNo': requestData['empNo'],
                'designation': requestData['designation']
            }
            employees.insert(0, newEmployee)'''
            Employee.add_employee(
                name=requestData['name'], empNo=requestData['empNo'], designation=requestData['designation'])
            resp = Response("", 201, mimetype="application/json")
            resp.headers['Location'] = "/employees/" + str(requestData['empNo'])
            return resp
        else:
            invalidEmployeeObjErrorMsg = {
                "error": "Invalid employee object passed in the request",
                "helpString": "Data should be passed similar to {'name' : 'Keerthi Kumar', 'empNo' : 123456, 'designation' : 'L1'}"
            }
            resp = Response(json.dumps(invalidEmployeeObjErrorMsg),
                            status=400, mimetype="application/json")
            return resp


@app.route('/employees/<int:empNo>', methods=['PUT'])
def replace_employee(empNo):
    requestData = request.get_json()
    '''newEmployee = {
        'name': requestData['name'],
        'empNo': empNo,
        'designation': requestData['designation']
    }
    count = 0
    for emp in employees:
        currEmpNo = emp['empNo']
        if currEmpNo == empNo:
            employees[count] = newEmployee
        count += 1'''
    Employee.replace_emp(requestData['name'], empNo, requestData['designation'])
    response = Response("", status=204)
    return response


@app.route('/employees/<int:empNo>', methods=['PATCH'])
def update_employee(empNo):
    if request.method == 'PATCH':
        requestData = request.get_json()
        updatedEmployee = {}
        if("name" in requestData):
            updatedEmployee['name'] = requestData['name']
        for emp in employees:
            if emp['empNo'] == empNo:
                emp.update(updatedEmployee)
            response = Response("", status=204)
            response.headers['Location'] = "/employees/" + str(empNo)
        return response


@app.route('/employees/<int:empNo>', methods=['DELETE'])
def delete_employee(empNo):
    if request.method == 'DELETE':
        requestData = request.get_json()
        count = 0
        for emp in employees:
            if emp['empNo'] == empNo:
                employees.pop(count)
            count += 1
            invalidEmployeeObjErrorMsg = {
                "error": "Employee with the provided empNo is not found !"
            }
            resp = Response(json.dumps(invalidEmployeeObjErrorMsg),
                            status=400, mimetype="application/json")
        return resp


@app.route('/employees/<int:empNo>')
def get_employee_by_no(empNo):
    result = Employee.get_employee(empNo)
    '''for emp in employees:
        if emp["empNo"] == empNo:
            result = {
                'name': emp['name'],
                'designation': emp['designation']
            }'''
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
