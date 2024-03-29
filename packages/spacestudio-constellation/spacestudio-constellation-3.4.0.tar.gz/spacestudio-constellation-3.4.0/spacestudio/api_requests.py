import json
import jwt
import os
import requests
import time

from dotenv import load_dotenv
from urllib3.exceptions import InsecureRequestWarning
from urllib import parse

from .__init__ import load_modules

log_base_url = os.getenv("LOG_BASE_URL")
log_mail = os.getenv("LOG_MAIL")
log_password = os.getenv("LOG_PASSWORD")
client_id = os.getenv("CLIENT_ID")

global session
global spacestudio_user_url
global headers
global auth_type
global jwt_token
global userId
global guardian_url
session = requests.Session()


def build_user_url(user_url, user_id):
    global spacestudio_user_url
    spacestudio_user_url = user_url + '/exoops/users/' + user_id


def build_headers(token):
    global headers
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}


def format_base_url(user_url):
    if user_url[-1] == '/':
        return user_url[:-1]
    else:
        return user_url


def connect(user_url, mail, password):
    global auth_type
    global jwt_token
    global userId
    global keycloak_url
    global headers

    formated_user_url = format_base_url(user_url)
    keycloak_url = 'https://auth.exotrail.space'
    keycloak_realm = 'spacestudio-users'

    body = "client_id=" + client_id + "&grant_type=password&username="+ parse.quote(mail) + "&password=" + parse.quote(password)
    r= requests.post(keycloak_url + "/realms/" + keycloak_realm + "/protocol/openid-connect/token", data=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    if (r.status_code != 200):
        print("Error: ", r.json())
        exit()
    
    jwt_token = r.json()['access_token']
    build_headers(jwt_token)
    
    scripting_option_activated = r.status_code == 200
    
    r= requests.get(log_base_url + "/exoops/users/infos", headers={"Authorization": "Bearer " + jwt_token})
    
    if (r.status_code != 200):
        print("SCRIPTING NOT ACTIVATED, CONTACT THE SUPPORT TEAM'")
        exit()
    
    userId = r.json()['id']
    
    build_user_url(formated_user_url, userId)
    build_headers(jwt_token)
    load_modules(scripting_option_activated)


def get_user_id():
    return userId


def get_jwt_token():
    return jwt_token


def get_headers():
    return headers


# Requests #
def post_request(url, body):
    req = session.post(url, headers=headers, data=json.dumps(body))
    return handle_response(req)


def get_request(url, stream=False):
    req = session.get(url, headers=headers, stream=stream)
    return handle_response(req, stream)


def get_status(url):
    try:
        req = session.get(url, headers=headers)
        return handle_response(req)
    except BaseException:
        return 0


def put_request(url, object_id, body):
    url = url + '/' + object_id
    req = session.put(url, headers=headers, data=json.dumps(body))
    return handle_response(req)


def delete_request(url, object_id):
    url = url + '/' + object_id
    session.delete(url, headers=headers)


# Handling Response #
def handle_response(request, stream=False):
    res = request

    if res.status_code == 409:
        print('Error 409 - Conflict issue - You may have already created an object or mission with the same name.')
    elif res.status_code == 400 or res.status_code == 404 or res.status_code == 500 or res.status_code == 403:
        print(res)
        print(res.json())
    else:
        if stream:
            return res
        else:
            return res.json()


def loop_through_object(param, response):
    if not response:
        return None
    for value in response:
        if value['displayedName'] == param:
            return value


# Get Object #
def get_object(element, url):
    response = get_request(url)
    asked_object = loop_through_object(element, response)
    return asked_object


def get_mission_id_with_url(mission, url):
    response = get_request(url)
    mission = loop_through_object(mission, response)
    if not mission:
        return None
    else:
        return mission['id']


def create_mission_from_paused_results_and_url(mission, new_mission_name, url, result_url):
    mission_id = get_mission_id_with_url(mission, url)
    simulationResult = get_mission_results_from_url(mission, url, result_url)['results']
    url = url + '/create_from_results/' + mission_id + '/' + new_mission_name
    post_request(url, simulationResult)


# Modify Objects #
def modify_object(old_object, new_object, url):
    object_to_modify = get_object(old_object['name'], url)
    object_to_modify_id = object_to_modify['id']
    put_request(url, object_to_modify_id, new_object)


# Delete Objects #


def delete_object(element, url):
    object_to_delete = get_object(element, url)
    if object_to_delete is not None:
        object_to_delete_id = object_to_delete['id']
        delete_request(url, object_to_delete_id)


def delete_intermediate_objects_from_mission_and_url(original_mission_name, object_url, mission_url):
    original_mission_id = get_mission_id_with_url(original_mission_name, mission_url)
    for url in [object_url, mission_url]:
        try:
            all_objects = get_request(url)
            for element in all_objects:
                if original_mission_id == element['pausedParentMissionId']:
                    delete_request(url, element['id'])
            print('Done with', url)
        except requests.exceptions.JSONDecodeError:
            print('Decoding error in', url)


# Computation #
def compute_mission_from_url(mission, url):
    mission_id = get_mission_id_with_url(mission, url)
    if mission_id:
        computation_url = url + '/compute/' + mission_id
        get_request(computation_url)


def compute_mission_until_duration_from_url(mission, url, duration):
    mission_id = get_mission_id_with_url(mission, url)
    url = url + '/compute_until_duration/' + mission_id
    post_request(url, duration)


# Results #
def get_mission_results_from_url(mission, url, result_url):
    mission_json = get_object(mission, url)
    if mission_json is None:
        print('Mission', mission, 'not found.')
        return None
    mission_computation_id = mission_json['computationLogId']
    mission_result_url = result_url + mission_computation_id
    results = get_request(mission_result_url)
    if 'errors' in results:
        for error in results['errors']:
            print('\nError: ', error['message'])
    return results


def wait_and_get_mission_results_from_url(mission, url, result_url):
    mission_json = get_object(mission, url)
    if mission_json is None:
        print('Mission', mission, 'not found.')
        return None
    mission_id = mission_json['id']
    status_url = url + '/status/' + mission_id
    status = get_status(status_url)
    if status == 0:
        print('Process pending')
    while status != -1:
        time.sleep(1)
        status = get_status(status_url)
        if status != 0:
            print('Computation status: ', status)
    return get_mission_results_from_url(mission, url, result_url)


def get_paused_mission_results_merged_with_url(mission, url):
    mission_id = get_mission_id_with_url(mission, url)
    url = url + '/create_merged_results/' + mission_id
    merged_results = get_request(url)
    if 'errors' in merged_results:
        for error in merged_results['errors']:
            print('\nError: ', error['message'])
    return merged_results
