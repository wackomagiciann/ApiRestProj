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




if __name__ == '__main__':
    app.run(host)
