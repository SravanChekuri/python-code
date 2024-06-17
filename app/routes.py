from functools import wraps
from app import Flask_app
from config import db
from controllers.employeeController import *
from controllers.userController import *
from controllers.empProfileController import *
from controllers.templateController import *


def verify_token(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
 
        try:
 
            auth_header = request.headers.get('Authorization')
 
            token = auth_header.split(' ')[1]
 
            print("token", token)
 
            if not token:
 
 
                return jsonify({'error': 'Access denied'}), 401
 
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            print(decoded_token)
            secret = decoded_token.get('User_Id')
            if not secret:
                return jsonify({'error': 'Invalid token'}), 401
 
            print("secret", secret)
 
            try:
 
                decoded = jwt.decode(token, secret, algorithms=["HS256"])
 
                request.userId = decoded.get('userId')
 
                request.decodedData = decoded
 
                return func(*args, **kwargs)
 
            except jwt.ExpiredSignatureError:
 
 
                return jsonify({'error': 'Token expired'}), 401
 
            except jwt.InvalidTokenError as e:
 
 
                return jsonify({'error': str(e)}), 401
 
        except Exception as error:
 
            return jsonify({'error': str(error)}), 401
 
    return decorated_function






# add admin/registration
@Flask_app.route('/add_user_details', methods=['POST'])
@verify_token
def add_User():
    token = request.headers.get('Authorization')
    print("token",token)
    return addUser()

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


# @Flask_app.route('/search_by_empnum/<num>', methods=['GET'])
# def search_by_empnum(num):
#     print("search_by_empnum",search_by_empnum)
#     return search_empnum(num)

# search employees by emp number
@Flask_app.route('/searchempnum/<num>', methods=['GET']) ##
def searchempnum(num):
    return searchemp_num(num)

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

# to download sample excel sheet
@Flask_app.route('/get_excel',methods=['GET'])
def get_excel():
    return getexcel1()
 
# get template
@Flask_app.route('/get_template',methods=['GET'])
def get_template():
    return gettemplate()

# get letter by employee number
@Flask_app.route('/get_letter/<empNumber>',methods=['GET'])
def get_letter(empNumber):
    print("xcvbnm,mnbv")
    return getletter(empNumber)

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

# # to download sample excel sheet
# @Flask_app.route('/get_excel',methods=['GET'])
# def get_excel():
#     return getexcel1()
 
@Flask_app.route('/get_address_detail/<id>/<esd>/<end>/<addressType>', methods=['GET'])
def get_address_detail(id,esd,end,addressType):
    return getAddressdetail(id,esd,end,addressType)

