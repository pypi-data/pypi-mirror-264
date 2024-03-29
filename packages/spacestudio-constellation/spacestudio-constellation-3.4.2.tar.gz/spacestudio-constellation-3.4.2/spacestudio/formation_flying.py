from .api_requests import post_request, get_request, \
    get_object, get_mission_id_with_url, modify_object, delete_object, \
    compute_mission_from_url, get_mission_results_from_url, wait_and_get_mission_results_from_url
from .urls import FF_SIMULATION_URL, MISSION_RESULTS_URL


# Create #
def create_mission(body):
    post_request(FF_SIMULATION_URL, body)


# Get Specific Mission/Object #
def get_mission(mission):
    return get_object(mission, FF_SIMULATION_URL)


def get_mission_id(mission):
    return get_mission_id_with_url(mission, FF_SIMULATION_URL)


# Modify Missions/Objects #
def modify_mission(mission, new_mission):
    modify_object(mission, new_mission, FF_SIMULATION_URL)


# Delete Missions/Objects #
def delete_mission(mission):
    delete_object(mission, FF_SIMULATION_URL)


# Get All Missions/Objects #
def get_all_missions():
    return get_request(FF_SIMULATION_URL)


# Computation #
def compute_mission(mission):
    compute_mission_from_url(mission, FF_SIMULATION_URL)


# Results #
def get_mission_results(mission):
    return get_mission_results_from_url(mission, FF_SIMULATION_URL, MISSION_RESULTS_URL)


def wait_and_get_mission_results(mission):
    return wait_and_get_mission_results_from_url(mission, FF_SIMULATION_URL, MISSION_RESULTS_URL)
