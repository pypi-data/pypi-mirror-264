
from .api_requests import post_request, get_request, \
    get_object, get_mission_id_with_url, modify_object, delete_object, \
    delete_intermediate_objects_from_mission_and_url, \
    compute_mission_from_url, compute_mission_until_duration_from_url, create_mission_from_paused_results_and_url, \
    get_mission_results_from_url, wait_and_get_mission_results_from_url, get_paused_mission_results_merged_with_url
from .urls import ANTENNA_URL, BATTERY_URL, ZONE_OF_INTEREST_URL, ORBIT_URL, SPACECRAFT_URL, SPACECRAFT_GEOMETRY_URL, \
    PROPULSION_SYSTEM_URL, SIMULATION_URL, MISSION_RESULTS_URL


# Create #
def create_antenna(body):
    post_request(ANTENNA_URL, body)


def create_battery(body):
    post_request(BATTERY_URL, body)


def create_zone_of_interest(body):
    post_request(ZONE_OF_INTEREST_URL, body)


def create_orbit(body):
    post_request(ORBIT_URL, body)


def create_spacecraft(body):
    post_request(SPACECRAFT_URL, body)


def create_spacecraft_geometry(body):
    post_request(SPACECRAFT_GEOMETRY_URL, body)


def create_propulsion_system(body):
    post_request(PROPULSION_SYSTEM_URL, body)


def create_mission(body):
    post_request(SIMULATION_URL, body)


def create_mission_from_paused_results(mission, new_mission_name):
    create_mission_from_paused_results_and_url(mission, new_mission_name, SIMULATION_URL, MISSION_RESULTS_URL)


# Get Specific Mission/Object #
def get_antenna(antenna):
    return get_object(antenna, ANTENNA_URL)


def get_battery(battery):
    return get_object(battery, BATTERY_URL)


def get_zone_of_interest(interest_zone):
    return get_object(interest_zone, ZONE_OF_INTEREST_URL)


def get_orbit(orbit):
    return get_object(orbit, ORBIT_URL)


def get_spacecraft(spacecraft):
    return get_object(spacecraft, SPACECRAFT_URL)


def get_spacecraft_geometry(spacecraft_geometry):
    return get_object(spacecraft_geometry, SPACECRAFT_GEOMETRY_URL)


def get_propulsion_system(propulsion_system):
    return get_object(propulsion_system, PROPULSION_SYSTEM_URL)


def get_mission(mission):
    return get_object(mission, SIMULATION_URL)


def get_mission_id(mission):
    return get_mission_id_with_url(mission, SIMULATION_URL)


# Modify Mission/Objects #
def modify_antenna(antenna, new_antenna):
    modify_object(antenna, new_antenna, ANTENNA_URL)


def modify_battery(battery, new_battery):
    modify_object(battery, new_battery, BATTERY_URL)


def modify_zone_of_interest(interest_zone, new_interest_zone):
    modify_object(interest_zone, new_interest_zone, ZONE_OF_INTEREST_URL)


def modify_orbit(orbit, new_orbit):
    modify_object(orbit, new_orbit, ORBIT_URL)


def modify_spacecraft(spacecraft, new_spacecraft):
    modify_object(spacecraft, new_spacecraft, SPACECRAFT_URL)


def modify_spacecraft_geometry(spacecraft_geometry, new_spacecraft_geometry):
    modify_object(spacecraft_geometry, new_spacecraft_geometry, SPACECRAFT_GEOMETRY_URL)


def modify_propulsion_system(propulsion_system, new_propulsion_system):
    modify_object(propulsion_system, new_propulsion_system, PROPULSION_SYSTEM_URL)


def modify_mission(mission, new_mission):
    modify_object(mission, new_mission, SIMULATION_URL)


# Delete Mission/Objects #
def delete_antenna(antenna):
    delete_object(antenna, SIMULATION_URL)


def delete_battery(battery):
    delete_object(battery, BATTERY_URL)


def delete_zone_of_interest(interest_zone):
    delete_object(interest_zone, ZONE_OF_INTEREST_URL)


def delete_orbit(orbit):
    delete_object(orbit, ORBIT_URL)


def delete_spacecraft(spacecraft):
    delete_object(spacecraft, SPACECRAFT_URL)


def delete_spacecraft_geometry(spacecraft_geometry):
    delete_object(spacecraft_geometry, SPACECRAFT_GEOMETRY_URL)


def delete_propulsion_system(propulsion_system):
    delete_object(propulsion_system, PROPULSION_SYSTEM_URL)


def delete_mission(mission):
    delete_object(mission, SIMULATION_URL)


def delete_intermediate_objects_from_mission(original_mission_name):
    delete_intermediate_objects_from_mission_and_url(original_mission_name,
                                                     [ANTENNA_URL, BATTERY_URL, ZONE_OF_INTEREST_URL, ORBIT_URL,
                                                      SPACECRAFT_URL, SPACECRAFT_GEOMETRY_URL, PROPULSION_SYSTEM_URL],
                                                     [SIMULATION_URL, MISSION_RESULTS_URL])


# Get All Missions/Objects #
def get_all_antennas():
    return get_request(ANTENNA_URL)


def get_all_batteries():
    return get_request(BATTERY_URL)


def get_all_zones_of_interest():
    return get_request(ZONE_OF_INTEREST_URL)


def get_all_orbits():
    return get_request(ORBIT_URL)


def get_all_spacecrafts():
    return get_request(SPACECRAFT_URL)


def get_all_spacecraft_geometries():
    return get_request(SPACECRAFT_GEOMETRY_URL)


def get_all_propulsion_systems():
    return get_request(PROPULSION_SYSTEM_URL)


def get_all_missions():
    return get_request(SIMULATION_URL)


# Computation #
def compute_mission(mission):
    compute_mission_from_url(mission, SIMULATION_URL)


def compute_mission_until_duration(mission, duration):
    compute_mission_until_duration_from_url(mission, SIMULATION_URL, duration)


# Results #
def get_mission_results(mission):
    return get_mission_results_from_url(mission, SIMULATION_URL, MISSION_RESULTS_URL)


def wait_and_get_mission_results(mission):
    return wait_and_get_mission_results_from_url(mission, SIMULATION_URL, MISSION_RESULTS_URL)


def get_paused_mission_results_merged(mission):
    return get_paused_mission_results_merged_with_url(mission, SIMULATION_URL)
