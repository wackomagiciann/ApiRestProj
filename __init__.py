#from flask import Flask, jsonify, request

#app = Flask(__name__)
from flask import Flask, jsonify, abort, request, make_response, Response
import json

app = Flask(__name__, static_url_path="")
app.config['JSON_SORT_KEYS'] = False

x = 6
host='127.0.0.1'

@app.route('/')
@app.route('/index')
def index():
    return "BAZA ALBUMÓW MUZYCZNYCH!"

#from app import routes

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}))


records = {
            'record1': {
        'Title': 'Space Oddity',
        'Year': 1969,
        'Artist': 'David Bowie',
        'Genre': 'Folk/Rock',
        'NumberOfTracks': 10,
        'Length': '45:12'}
    ,
            'record2': {
        'Title': '808s & Heartbreak',
        'Year': 2008,
        'Artist': 'Kanye West',
        'Genre': 'R&B/Electropop/Synth-Pop',
        'NumberOfTracks': 12,
        'Length': '51:58'}
    ,
              'record3': {
        'Title': 'Lets Stay Together' ,
        'Year': 1971,
        'Artist': 'Al Green',
        'Genre': 'Soul',
        'NumberOfTracks': 9,
        'Length': '33:53'}
    ,
              'record4': {
        'Title': 'In Colour',
        'Year': 2015,
        'Artist': 'Jamie XX',
        'Genre': 'Electronica/House/FutueGarage',
        'NumberOfTracks': 11,
        'Length': '42:44'}
    ,
    'record5': {
        'Title': '(Whats the Story) Morning Glory? ',
        'Year': 1995,
        'Artist': 'Oasis',
        'Genre': 'Rock/Britpop',
        'NumberOfTracks': 12,
        'Length': '50:06'}
}

@app.route('/ListOfRecords',methods=['GET'])
def get_records():
    records_list=[]
    for record in records:
        records_list.append(record)
    return jsonify(records_list)

@app.route('/records/<string:id>',methods=['GET'])
def get_record_details(id):
    record_id = id.split(':')
    if len(record_id) == 1:
        if record_id[0] in records:
            return jsonify({record_id[0]: records[record_id[0]]})

@app.route('/records',methods=['GET'])
def return_all():
    return jsonify(records)

@app.route('/records/add',methods=['POST'])
def add_record():
    if not request.json or 'record_id' not in request.json:
            abort(400)
    record_id=request.json['record_id'].split(':')
    if len (record_id)==0 or len (record_id)>1: #żeby dane mialy odpowiedni poziom "drzewka"
        abort(400)
    if len (record_id)==1:
        if record_id[0] in records:
            abort(400)
        else:
            new_record={'Title':'','Year': 0,'Artist': '','Genre': '','NumberOfTracks': 0, 'Length': ''}
            records[record_id[0]]=new_record
            return jsonify({record_id[0]: new_record}), 201




@app.route('/records/<string:id>', methods=['PUT'])
def editOne(id):
    record_id = id.split(':')
    if len(record_id) == 1:
        if not request.json and 'Title' and 'Year' and 'Artist' and 'Genre' and 'NumberOfTracks' and 'Lenght' not in request.json:
            abort(400)
        if not record_id[0] in records:
            abort(400)
        data = request.get_json()
        records[record_id[0]] = data
        return jsonify({record_id[0]: data}), 201


@app.route('/records/<string:id>', methods=['DELETE'])
def deleteOne(id):
    record_id = id.split(':')
    if len(record_id) == 0 or len(record_id) > 1:
        abort(400)
    else:
        if not record_id[0] in records:
            abort(400)
        else:
            del records[record_id[0]]
            return jsonify({'result': True})


"""
        def question(id):
            set_id = id.split(':')
            if request.method == 'GET':
                if len(set_id) == 1:
                    if set_id[0] in lego_set_database:
                        return jsonify({set_id[0]: lego_set_database[set_id[0]]})
                    else:
                        abort(404)
            if request.method == 'DELETE':
                if len(set_id) == 0 or len(set_id) > 1:
                    abort(400)
                else:
                    if not set_id[0] in lego_set_database:
                        abort(400)
                    else:
                        del lego_set_database[set_id[0]]
                        return jsonify({'result': True})
            if request.method == 'PUT':
                if not request.json and 'name' and 'year' and 'bricks_number' and 'minifigs_number' and 'theme' not in request.json:
                    abort(400)
                if not set_id[0] in lego_set_database:
                    abort(400)
                data = request.get_json()
                lego_set_database[set_id[0]] = data
                return jsonify({set_id[0]: data}), 201
"""
"""
accounts = {
    'advertiser1': {
        'allocatedIn': 1800,
        'allocatedOut': 400,
        'type': 'budget',
        'subaccounts': {
            'campaign1': {
                'allocatedIn': 400,
                'allocatedOut': 200,
                'type': 'budget',
                'subaccounts': {
                    'baner1': {
                        'allocatedIn': 200,
                        'allocatedOut': 0,
                        'type': 'budget'
                    }
                }
            }
        }
    },
    'advertiser2': {
        'allocatedIn': 700,
        'allocatedOut': 500,
        'type': 'budget',
        'subaccounts': {
            'campaign1': {
                'allocatedIn': 200,
                'allocatedOut': 0,
                'type': 'budget',
                'subaccounts': {
                }
            },
            'campaign2': {
                'allocatedIn': 300,
                'allocatedOut': 0,
                'type': 'budget',
                'subaccounts': {
                }
            }
        }
    }
}


@app.route('/accounts', methods=['GET'])
def get_accounts():
    accountList = []
    for currentTopLevelAccount in accounts:
        accountList.append([currentTopLevelAccount])
        for currentSecondLevelAccount in accounts[currentTopLevelAccount]['subaccounts']:
            accountList.append([currentTopLevelAccount, currentSecondLevelAccount])
            for currentLastLevelAccount in accounts[currentTopLevelAccount]['subaccounts'][currentSecondLevelAccount][
                'subaccounts']:
                accountList.append([currentTopLevelAccount, currentSecondLevelAccount, currentLastLevelAccount])
    return jsonify({'Accounts': accountList})


@app.route('/accounts/<string:account_name>/summary', methods=['GET'])
def get_account(account_name):
    accountHierarchy = account_name.split(':')
    if len(accountHierarchy) == 0 or len(accountHierarchy) > 3:
        abort(400)
    if len(accountHierarchy) == 1:
        if accountHierarchy[0] in accounts:
            return jsonify({accountHierarchy[0]: accounts[accountHierarchy[0]]})
        else:
            abort(404)
    elif len(accountHierarchy) == 2:
        if accountHierarchy[0] in accounts:
            if accountHierarchy[1] in accounts[accountHierarchy[0]]['subaccounts']:
                return jsonify({account_name: accounts[accountHierarchy[0]]['subaccounts'][accountHierarchy[1]]})
            else:
                abort(404)
        else:
            abort(404)
    elif len(accountHierarchy) == 3:
        if accountHierarchy[0] in accounts:
            if accountHierarchy[1] in accounts[accountHierarchy[0]]['subaccounts']:
                if accountHierarchy[2] in accounts[accountHierarchy[0]]['subaccounts'][accountHierarchy[1]][
                    'subaccounts']:
                    return jsonify({account_name: accounts[accountHierarchy[0]]['subaccounts'][accountHierarchy[1]][
                        'subaccounts'][accountHierarchy[2]]})
                else:
                    abort(404)
            else:
                abort(404)
        else:
            abort(404)
    else:
        abort(400)


@app.route('/accounts', methods=['POST'])
def create_account():
    if not request.json or 'accountName' not in request.json:
        abort(400)
    account_name = request.json['accountName']
    accountHierarchy = account_name.split(':')
    if len(accountHierarchy) == 0 or len(accountHierarchy) > 3:
        abort(400)
    if len(accountHierarchy) == 1:
        if accountHierarchy[0] in accounts:
            # abort(400)
            return make_response((jsonify({'error': 'Already exists'})))
        else:
            newAccount = {'allocatedIn': 0, 'allocatedOut': 0, 'type': 'budget', 'subaccounts': {}}
            accounts[accountHierarchy[0]] = newAccount
            return jsonify({accountHierarchy[0]: accounts[accountHierarchy[0]]})
    elif len(accountHierarchy) == 2:
        if accountHierarchy[0] in accounts:
            if accountHierarchy[1] in accounts[accountHierarchy[0]]['subaccounts']:
                return make_response(jsonify({'error': 'Already exists'}))
            else:
                newAccount = {'allocatedIn': 0, 'allocatedOut': 0, 'type': 'budget', 'subaccounts': {}}
                accounts[accountHierarchy[0]]['subaccounts'][accountHierarchy[1]] = newAccount
                return jsonify({account_name: newAccount})
        else:
            abort(400)
    elif len(accountHierarchy) == 3:
        if accountHierarchy[0] in accounts:
            if accountHierarchy[1] in accounts[accountHierarchy[0]]['subaccounts']:
                if accountHierarchy[2] in accounts[accountHierarchy[0]]['subaccounts'][accountHierarchy[1]][
                    'subaccounts']:
                    return make_response(jsonify({'error': 'Already exists'}))
                else:
                    newAccount = {'allocatedIn': 0, 'allocatedOut': 0, 'type': 'budget'}
                    accounts[accountHierarchy[0]]['subaccounts'][accountHierarchy[1]]['subaccounts'][
                        accountHierarchy[2]] = newAccount
                    return jsonify({account_name: newAccount})
            else:
                abort(400)
        else:
            abort(400)
    else:
        abort(400)


@app.route('/accounts/<string:account_name>/budget', methods=['PUT'])
def update_budget(account_name):
    if not request.json or 'USD/1M' not in request.json:
        print("request.json", request.json)
        abort(400)
    accountHierarchy = account_name.split(':')
    budget = request.json['USD/1M']
    if len(accountHierarchy) == 0 or len(accountHierarchy) > 3:
        abort(400)
    if len(accountHierarchy) == 1:
        if accountHierarchy[0] in accounts:
            if type(budget) is not int:
                return make_response(jsonify({'error': 'Budget must be integer'}))
            else:
                if budget < accounts[accountHierarchy[0]]['allocatedOut']:
                    return make_response(jsonify({'error': 'Budget must be bigger than allocation already done'}))
                else:
                    accounts[accountHierarchy[0]]['allocatedIn'] = budget
                    return jsonify({accountHierarchy[0]: accounts[accountHierarchy[0]]})
        else:
            abort(404)
    else:
        return make_response(jsonify({'error': 'Budget can be added only to top-level account'}))


@app.route('/accounts/<string:account_name>/close', methods=['DELETE'])
def delete_account(account_name):
    accountHierarchy = account_name.split(':')
    if len(accountHierarchy) == 0 or len(accountHierarchy) > 3:
        abort(400)
    if len(accountHierarchy) == 1:
        if accountHierarchy[0] in accounts:
            del accounts[accountHierarchy[0]]
            return jsonify({'result': True})
        else:
            abort(404)
    elif len(accountHierarchy) == 2:
        if accountHierarchy[0] in accounts:
            if accountHierarchy[1] in accounts[accountHierarchy[0]]['subaccounts']:
                del accounts[accountHierarchy[0]]['subaccounts'][accountHierarchy[1]]
                return jsonify({'result': True})
            else:
                abort(404)
        else:
            abort(404)
    elif len(accountHierarchy) == 3:
        if accountHierarchy[0] in accounts:
            if accountHierarchy[1] in accounts[accountHierarchy[0]]['subaccounts']:
                if accountHierarchy[2] in accounts[accountHierarchy[0]]['subaccounts'][accountHierarchy[1]][
                    'subaccounts']:
                    del accounts[accountHierarchy[0]]['subaccounts'][accountHierarchy[1]]['subaccounts'][
                        accountHierarchy[2]]
                    return jsonify({'result': True})
                else:
                    abort(404)
            else:
                abort(404)
        else:
            abort(404)
    else:
        abort(400)


@app.route('/accounts/<string:account_name>/ballance', methods=['POST'])
def transfer_budget(account_name):
    if not request.json or 'USD/1M' not in request.json:
        print("request.json", request.json)
        abort(400)
    accountHierarchy = account_name.split(':')
    ballance = request.json['USD/1M']
    if len(accountHierarchy) == 0 or len(accountHierarchy) > 3:
        abort(400)
    if len(accountHierarchy) == 1:
        if accountHierarchy[0] in accounts:
            return make_response(jsonify({'error': 'This operation can be done only for subaccounts'}))
        else:
            abort(404)
    elif len(accountHierarchy) == 2:
        if accountHierarchy[0] in accounts:
            if accountHierarchy[1] in accounts[accountHierarchy[0]]['subaccounts']:
                if type(ballance) is not int:
                    return make_response(jsonify({'error': 'Budget must be integer'}))
                else:
                    if ballance > accounts[accountHierarchy[0]]['allocatedIn'] - accounts[accountHierarchy[0]][
                        'allocatedOut']:
                        return make_response(jsonify(
                            {'error': 'Ballance must be less than free budget available in the parent account'}))
                    else:
                        accounts[accountHierarchy[0]]['allocatedOut'] += ballance
                        accounts[accountHierarchy[0]]['subaccounts'][accountHierarchy[1]]['allocatedIn'] += ballance
                        return jsonify({accountHierarchy[0]: accounts[accountHierarchy[0]]})
            else:
                abort(404)
        else:
            abort(404)
    elif len(accountHierarchy) == 3:
        if accountHierarchy[0] in accounts:
            if accountHierarchy[1] in accounts[accountHierarchy[0]]['subaccounts']:
                if accountHierarchy[2] in accounts[accountHierarchy[0]]['subaccounts'][accountHierarchy[1]][
                    'subaccounts']:
                    if type(ballance) is not int:
                        return make_response(jsonify({'error': 'Budget must be integer'}))
                    else:
                        if ballance > accounts[accountHierarchy[0]]['subaccounts'][accountHierarchy[1]]['allocatedIn'] - \
                                accounts[accountHierarchy[0]]['subaccounts'][accountHierarchy[1]]['allocatedOut']:
                            return make_response(jsonify(
                                {'error': 'Ballance must be less than free budget available in the parent account'}))
                        else:
                            accounts[accountHierarchy[0]]['subaccounts'][accountHierarchy[1]][
                                'allocatedOut'] += ballance
                            accounts[accountHierarchy[0]]['subaccounts'][accountHierarchy[1]]['subaccounts'][
                                accountHierarchy[2]]['allocatedIn'] += ballance
                            return jsonify({accountHierarchy[1]: accounts[accountHierarchy[0]]['subaccounts'][
                                accountHierarchy[1]]})
                else:
                    abort(404)
            else:
                abort(404)
        else:
            abort(404)

    else:
        abort(404)
"""

if __name__ == '__main__':
    app.run(host)
