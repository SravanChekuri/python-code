from app import Flask_app
from controllers.staticData import addsuperadmin
 
addsuperadmin()
 
if __name__ == '__main__':
   
    Flask_app.run(debug=True)
   
 

