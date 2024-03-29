
from .api_requests import post_request, \
    get_object, get_mission_id_with_url, modify_object, delete_object, compute_mission_from_url, \
    get_mission_results_from_url, wait_and_get_mission_results_from_url, get_request
from .urls import LAUNCH_URL, DEPLOYMENT_MISSION_URL, MISSION_RESULTS_URL


# Create #
def create_launch(body):
    post_request(LAUNCH_URL, body)


def create_mission(body):
    post_request(DEPLOYMENT_MISSION_URL, body)


# Get Specific Mission/Object #
def get_launch(launch):
    return get_object(launch, LAUNCH_URL)


def get_mission(mission):
    return get_object(mission, DEPLOYMENT_MISSION_URL)


def get_mission_id(mission):
    return get_mission_id_with_url(mission, DEPLOYMENT_MISSION_URL)


# Modify Missions/Objects #
def modify_launch(launch, new_launch):
    modify_object(launch, new_launch, LAUNCH_URL)


def modify_mission(mission, new_mission):
    modify_object(mission, new_mission, DEPLOYMENT_MISSION_URL)


# Delete Missions/Objects #
def delete_launch(launch):
    delete_object(launch, LAUNCH_URL)


def delete_mission(mission):
    delete_object(mission, DEPLOYMENT_MISSION_URL)


# Get All Missions/Objects #
def get_all_launches():
    return get_request(LAUNCH_URL)


def get_all_missions():
    return get_request(DEPLOYMENT_MISSION_URL)


# Computation #
def compute_mission(mission):
    compute_mission_from_url(mission, DEPLOYMENT_MISSION_URL)


# Results #
def get_mission_results(mission):
    return get_mission_results_from_url(mission, DEPLOYMENT_MISSION_URL, MISSION_RESULTS_URL)


def wait_and_get_mission_results(mission):
    return wait_and_get_mission_results_from_url(mission, DEPLOYMENT_MISSION_URL, MISSION_RESULTS_URL)
