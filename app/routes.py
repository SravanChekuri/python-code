from app import Flask_app
from config import db
from controllers.employeeController import *
from controllers.userController import *
from controllers.empProfileController import *
from controllers.templateController import *









# add admin
@Flask_app.route('/add_admin_details', methods=['POST'])
def add_admin():
    print("fghjkl")
    return addadmin()

# login
@Flask_app.route('/login', methods=['POST'])
def log_in():
    return login()

# generate otp and send to email
@Flask_app.route('/email', methods=['POST'])
def e_mail():
    print("sedfghjkl")
    return email()

# verify otp
@Flask_app.route('/verify', methods=['POST'])
def verif_y():
    print("sedfghjkl")
    return verify()

@Flask_app.route('/change_password', methods=['PUT'])
def change_password():
    print("sdtfyguio;")
    return changePassword()


# ////////////////employee////////
# add employee
@Flask_app.route('/add_emp_details', methods=['POST'])
def add_Employee():
    print("add_Employee")
    return addEmployee()
 
# add employees in bulk
@Flask_app.route('/add_emp_bulk', methods=['POST'])
def add_bulk():
    print("add bulk")
    return addbulk()

@Flask_app.route('/Bulk_update', methods=['PUT'])
def Bulk_Update():
    print("dfghjk")
    return bulk_update()

# # get employeedetails
# @Flask_app.route('/get_employee_details/<id>', methods=['GET'])
# def get_Employeedetails(id):
#     return getEmployeedetails(id)


# get all employees
@Flask_app.route('/get_emp_details', methods=['GET'])
def get_Employee():
    print("sdfghjk")
    return getEmployee()


# get employeedetails
@Flask_app.route('/get_employee_details/<id>/<date>/<enddate>', methods=['GET'])
def get_Employeedetails(id,date,enddate):
    print("getemp",date)
    return getEmployeedetails(id,date,enddate)

@Flask_app.route('/Search_employee_details/<empNum>/<date>/<enddate>', methods=['GET'])
def Search_Employeedetails(empNum,date,enddate):
    print("SearchEmployeedetails",empNum,date,enddate)
    return SearchEmployeedetails(empNum,date,enddate)

@Flask_app.route('/get_emp_detail/<id>', methods=['GET'])
def get_Empdetails(id):
    return getEmpdetails(id)
 
# # get by employees id
# @Flask_app.route('/get_emp_details/<int:id>', methods=['GET'])
# def get_Employee_By_Id(id):
#     return getEmployeeById(id)

# update employee details
@Flask_app.route('/update_emp/<id>', methods=['PUT'])
def update_emp(id):
    print("fdghjklkjhgfgojhb")
    return updateemp(id)

# delete employee
# @Flask_app.route('/delete_data/<id>',methods=['DELETE'])
# def delete_data(id):
#     return deletedata(id)


# add & update employement details
@Flask_app.route('/employement_details/<id>', methods=['POST'])
def employement_details(id):
    return employementdetails(id)

# get employement details
@Flask_app.route('/get_employement_details/<id>', methods=['GET'])
def get_Employeement(id):
    print("dxfghjkl")
    return getEmployementdetails(id)

@Flask_app.route('/get_employement_detail/<id>/<date>/<enddate>', methods=['GET'])
def get_Employementdetail(id,date,enddate):
    print("getEmployementdetail")
    return getEmployementdetail(id,date,enddate)



# ////////////address details///////////
# add & update address
@Flask_app.route('/address_details/<id>', methods=['POST'])
def address_details(id):
    print("gfhjkkljh")
    return addressdetails(id)

# ////////////////////////////
# get all admins
@Flask_app.route('/get_admin_details', methods=['GET'])
def get_admin():
    return getadmin()

# get admin by id
@Flask_app.route('/get_admin_by_id/<id>', methods=['GET'])
def get_adminid(id):
    return getadmin_id(id)

# search
@Flask_app.route('/filterPersons/<search_data>', methods=['GET']) ##
def filter_Persons(search_data):
    return filterPersons(search_data)
 


# PUT/UPDATE Method


# update admin details
@Flask_app.route('/update_admindetails/<id>',methods=['PUT'])
def update_admindetails(id):
    return updateadmin_details(id)


# DELETE Method


# delete admin
@Flask_app.route('/delete_admin/<id>',methods=['DELETE'])
def delete_admin(id):
    return deleteadmin(id)

# /////////empProfile//////
# # add address
# @Flask_app.route('/add_address',methods=['POST'])
# def add_address():
#     return addaddress()

# add template
@Flask_app.route('/add_template',methods=['POST'])
def add_template():
    return addtemplate()

# retrieve template
@Flask_app.route('/retrieve_template/<string:Id>', methods=['GET'])
def retrieve_template(Id):
    print("sdfghjgvyvb")
    return temp(Id)
# convertpdf
@Flask_app.route('/convert_rtf/<string:Id>', methods=['GET'])
def convert_rtf(Id):
    print("sdfghjgvyvb")
    return convertrtf(Id)

# update template
@Flask_app.route('/update_temp/<string:Id>', methods=['PUT'])
def update_temp(Id):
    print("sdfghjgvyvb")
    return updatetemp(Id)

@Flask_app.route('/generate_letter', methods=['POST'])
def generate_Letter():
    print("tgyhbjnm")
    return Generateletter()



# generate letter
@Flask_app.route('/add_data_pdf', methods=['POST'])
def adddata_pdf():
    print("tgyhbjnm")
    return add_data_pdf()
 
# view pdf
@Flask_app.route('/view_pdf', methods=['GET'])
def view_pdf():
    print("fcgvbhjnmkjio")
    return viewpdf()


