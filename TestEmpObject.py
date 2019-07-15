def isValidEmpObject(empObject):
    if("name" in empObject and "designation" in empObject and "empNo" in empObject):
        return True
    else:
        return False


valid_emp_object = {
    'name': 'Tarun Sharma',
    'empNo': 701250,
    'designation': "L2"
}

emp_object_name_missing = {
    'empNo': 701250,
    'designation': "L2"
}

emp_object_empNo_missing = {
    'name': 'Tarun Sharma',
    'designation': "L2"
}

emp_object_desg_missing = {
    'name': 'Tarun Sharma',
    'empNo': 701250
}
