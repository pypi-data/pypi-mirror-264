
from .api_requests import post_request, get_request,  \
    get_object, get_mission_id_with_url, modify_object, delete_object, compute_mission_from_url, \
    get_mission_results_from_url, wait_and_get_mission_results_from_url
from .urls import PARAMETRIC_PROPULSION_SYSTEM_URL, PARAMETRIC_ORBIT_URL, PARAMETRIC_SPACECRAFT_URL, \
    REACTION_WHEELS_URL, PARAMETRIC_MAGNETIC_TORQUER_URL, PARAMETRIC_STUDY_URL, MISSION_RESULTS_URL


# Create #
def create_propulsion_system(body):
    post_request(PARAMETRIC_PROPULSION_SYSTEM_URL, body)


def create_orbit(body):
    post_request(PARAMETRIC_ORBIT_URL, body)


def create_spacecraft(body):
    post_request(PARAMETRIC_SPACECRAFT_URL, body)


def create_reaction_wheels(body):
    post_request(REACTION_WHEELS_URL, body)


def create_magnetic_torquer(body):
    post_request(PARAMETRIC_MAGNETIC_TORQUER_URL, body)


def create_mission(body):
    post_request(PARAMETRIC_STUDY_URL, body)


# Get Specific Mission/Object #
def get_propulsion_system(propulsion_system):
    return get_object(propulsion_system, PARAMETRIC_PROPULSION_SYSTEM_URL)


def get_orbit(orbit):
    return get_object(orbit, PARAMETRIC_ORBIT_URL)


def get_spacecraft(spacecraft):
    return get_object(spacecraft, PARAMETRIC_SPACECRAFT_URL)


def get_reaction_wheels(reaction_wheels):
    return get_object(reaction_wheels, REACTION_WHEELS_URL)


def get_magnetic_torquer(magnetic_torquer):
    return get_object(magnetic_torquer, PARAMETRIC_MAGNETIC_TORQUER_URL)


def get_mission(mission):
    return get_object(mission, PARAMETRIC_STUDY_URL)


def get_mission_id(mission):
    return get_mission_id_with_url(mission, PARAMETRIC_STUDY_URL)


# Modify Missions/Objects #
def modify_propulsion_system(propulsion_system, new_propulsion_system):
    modify_object(propulsion_system, new_propulsion_system, PARAMETRIC_PROPULSION_SYSTEM_URL)


def modify_orbit(orbit, new_orbit):
    modify_object(orbit, new_orbit, PARAMETRIC_ORBIT_URL)


def modify_spacecraft(spacecraft, new_spacecraft):
    modify_object(spacecraft, new_spacecraft, PARAMETRIC_SPACECRAFT_URL)


def modify_reaction_wheels(reaction_wheels, new_reaction_wheels):
    modify_object(reaction_wheels, new_reaction_wheels, REACTION_WHEELS_URL)


def modify_magnetic_torquer(magnetic_torquer, new_magnetic_torquer):
    modify_object(magnetic_torquer, new_magnetic_torquer, PARAMETRIC_MAGNETIC_TORQUER_URL)


def modify_mission(mission, new_mission):
    modify_object(mission, new_mission, PARAMETRIC_STUDY_URL)


# Delete Missions/Objects #
def delete_propulsion_system(propulsion_system):
    delete_object(propulsion_system, PARAMETRIC_PROPULSION_SYSTEM_URL)


def delete_orbit(orbit):
    delete_object(orbit, PARAMETRIC_ORBIT_URL)


def delete_spacecraft(spacecraft):
    delete_object(spacecraft, PARAMETRIC_SPACECRAFT_URL)


def delete_reaction_wheels(reaction_wheels):
    delete_object(reaction_wheels, REACTION_WHEELS_URL)


def delete_magnetic_torquer(magnetic_torquer):
    delete_object(magnetic_torquer, PARAMETRIC_MAGNETIC_TORQUER_URL)


def delete_mission(mission):
    delete_object(mission, PARAMETRIC_STUDY_URL)


# Get All Missions/Objects #
def get_all_propulsion_systems():
    return get_request(PARAMETRIC_PROPULSION_SYSTEM_URL)


def get_all_orbits():
    return get_request(PARAMETRIC_ORBIT_URL)


def get_all_spacecrafts():
    return get_request(PARAMETRIC_SPACECRAFT_URL)


def get_all_reaction_wheels():
    return get_request(REACTION_WHEELS_URL)


def get_all_magnetic_torquers():
    return get_request(PARAMETRIC_MAGNETIC_TORQUER_URL)


def get_all_missions():
    return get_request(PARAMETRIC_STUDY_URL)


# Computation #
def compute_mission(mission):
    compute_mission_from_url(mission, PARAMETRIC_STUDY_URL)


# Results #
def get_mission_results(mission):
    return get_mission_results_from_url(mission, PARAMETRIC_STUDY_URL, MISSION_RESULTS_URL)


def wait_and_get_mission_results(mission):
    return wait_and_get_mission_results_from_url(mission, PARAMETRIC_STUDY_URL, MISSION_RESULTS_URL)
