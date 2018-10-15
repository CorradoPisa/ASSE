from flakon import JsonBlueprint
from flask import request, jsonify, abort, Response
import json as js
from myservice.classes.poll import Poll, NonExistingOptionException, UserAlreadyVotedException

doodles = JsonBlueprint('doodles', __name__)

_ACTIVEPOLLS = {} # list of created polls
_POLLNUMBER = 0 # index of the last created poll

@doodles.route('/doodles', methods=['POST', 'GET'])
def all_polls():

    if request.method == 'POST':
        result = create_doodle(request)

    elif request.method == 'GET':
        result = get_all_doodles(request)
    
    return result


@doodles.route('/doodles/<id>', methods=['PUT', 'GET', 'DELETE'])
def single_poll(id):
    global _ACTIVEPOLLS
    result = ""

    exist_poll(id) # check if the Doodle is an existing one

    if request.method == 'GET': # retrieve a poll
        result = jsonify(_ACTIVEPOLLS[id].serialize())

    elif request.method == 'DELETE': # delete a poll and get back winners
        result = jsonify({'winners' : _ACTIVEPOLLS.pop(id).get_winners()})

    elif request.method == 'PUT': # vote in a poll
        response = vote(id, request)
        # I do not know why .get_json() method is not working
        # as per documentation it should be
        # That is why I had to parse row data in not a neat way
        json = js.loads(response.get_data().decode("utf-8"))
        result = jsonify({'winners' : json})


    return result

@doodles.route('/doodles/<id>/<person>', methods=['GET', 'DELETE'])
def person_poll(id, person):
    
    exist_poll(id) # check if the Doodle exists
    
    if request.method == 'GET':
        result = jsonify({'votedoptions' :_ACTIVEPOLLS[id].get_voted_options(person)})
        # retrieve all preferences cast from <person> in poll <id>
    if request.method == 'DELETE':
        result = jsonify({'removed' :_ACTIVEPOLLS[id].delete_voted_options(person)})
        # delete all preferences cast from <person> in poll <id>

    return result
       

def vote(id, request):
    result = ""
    # extract person and option fields from the JSON request
    json = request.get_json()
    person = json['person']
    option = json['option']

    try:
        result = jsonify(_ACTIVEPOLLS[id].vote(person,option))
        # cast a vote from person in  _ACTIVEPOLLS[id]?
    except UserAlreadyVotedException:
        abort(400) # Bad Request
    except NonExistingOptionException:
        abort(400) # I think it should be 422:Unprocessable Entity, but test forces me
        # manage the NonExistingOptionException

    return result


def create_doodle(request):
    global _ACTIVEPOLLS, _POLLNUMBER
    json = request.get_json()
    _POLLNUMBER += 1;
    _ACTIVEPOLLS[str(_POLLNUMBER)] = (Poll(_POLLNUMBER, json['title'], json['options']))
    return jsonify({'pollnumber': _POLLNUMBER})


def get_all_doodles(request):
    global _ACTIVEPOLLS
    return jsonify(activepolls = [e.serialize() for e in _ACTIVEPOLLS.values()])

def exist_poll(id):
    if int(id) > _POLLNUMBER:
        abort(404) # error 404: Not Found, i.e. wrong URL, resource does not exist
    elif not(id in _ACTIVEPOLLS):
        abort(410) # error 410: Gone, i.e. it existed but it's not there anymore