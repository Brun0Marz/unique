import pymongo
from datetime import datetime
pymongo_uri='mongodb+srv://lucbellintani:190897@cluster0.kqtvw.mongodb.net/?retryWrites=true&w=majority'

client = pymongo.MongoClient(pymongo_uri)
db = client['UniqueVisits']

def checkAccountExists(accountNumber:int) -> bool:
    col=db['Accounts']

    num_accounts=col.count_documents({'account_id':accountNumber})

    if num_accounts==0:
        return False
    elif num_accounts==1:
        return True
    else:
        return False

def checkIPExists(ip_address:str) -> bool:
    col=db['Visits']

    num_accounts=col.count_documents({'ip_address':ip_address})

    if num_accounts==0:
        return False
    else:
        return True

def check_ip_id_tuple(ip_address:str,id_code:str) -> bool:
    col=db['Visits']

    visits_old_code=col.count_documents({'ip_address':ip_address,'id_code_old':id_code})
    visits_new_code=col.count_documents({'ip_address':ip_address,'id_code_new':id_code})

    if (visits_old_code>0) or (visits_new_code>0):
        return True
    else:
        return False

def write_new_to_db(ip_address,code_new,code_old=None,isFirst=False,wasReferred=False,code_reused=False):
    col=db['Visits']
    now = datetime.now()

    insDict={
        'ip_address':ip_address,
        'id_code_old':code_old,
        'id_code_new':code_new,
        'entry_time':now
    }
    if isFirst:
        insDict['isFirst']=True
    else:
        insDict['isFirst']=False

    if wasReferred:
        insDict['wasReferred']=True
    else:
        pass

    if code_reused:
        insDict['code_reused']=True
    else:
        insDict['code_reused']=False
    
    col.insert_one(insDict)