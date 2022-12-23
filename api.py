from distutils.log import debug
from flask import Flask,jsonify,request

from mongoDBqueries import *
from id_generator import generate_id

app = Flask(__name__)

@app.route('/check_account', methods=['GET'])
def check_account():
    account_number = int(request.args.get('accNum'))

    #Check if account exists

    if checkAccountExists(accountNumber=account_number):

        return jsonify({
            'account_exists':True,
                        })
    else:
        return jsonify({
            'account_exists':False,
                        })


@app.route('/process_id', methods=['GET'])
def id_processing_exists():

    ip_address=request.environ['REMOTE_ADDR']

    id_code = request.args.get('req_id')

    account_number = int(request.args.get('accNum'))

    #Check if ip in db
    if not checkIPExists(ip_address=ip_address):
        #New visitor, referred from someone else or is new entirely. Insert in db and issue a new code

        newCode=str(account_number)+'-'+generate_id()
        
        if id_code is not None:
            write_new_to_db(ip_address=ip_address,code_old=id_code,code_new=newCode,isFirst=True,wasReferred=True)
        else:
            write_new_to_db(ip_address=ip_address,code_old=None,code_new=newCode,isFirst=False,wasReferred=False)
    

    else:
        #Return visitor, with a code that could be theirs or someone else's, or no code at all.
        if check_ip_id_tuple(ip_address=ip_address,id_code=id_code):
            #So we have them using one of their old codes. Record this and issue a new one.
            newCode=str(account_number)+'-'+generate_id()
            write_new_to_db(ip_address=ip_address,code_old=id_code,code_new=newCode,isFirst=False,wasReferred=True,code_reused=True)

            

        else:
            #Previous visitor, referred again by someone else, or no code at all.
            newCode=str(account_number)+'-'+generate_id()
            if id_code is not None:
                write_new_to_db(ip_address=ip_address,code_old=id_code,code_new=newCode,isFirst=False,wasReferred=True,code_reused=False)
            else:
                write_new_to_db(ip_address=ip_address,code_old=None,code_new=newCode,isFirst=False,wasReferred=False,code_reused=False)
    
    response = jsonify({'id_code': newCode})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response




if __name__ == '__main__':
    app.run(host='localhost', port=8000,debug=False)