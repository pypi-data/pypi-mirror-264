
from .api_requests import post_request, \
    get_object, get_mission_id_with_url, modify_object, delete_object, compute_mission_from_url, \
    get_mission_results_from_url, wait_and_get_mission_results_from_url, get_request
from .urls import GROUND_STATION_URL, PAYLOAD_URL, EARTH_MESH_URL, SUB_CONSTELLATION_URL, CONSTELLATION_URL, \
    POINT_OF_INTEREST_URL, CONSTELLATION_PERFORMANCE_ANALYSIS_URL, CONSTELLATION_OPTIMIZATION_URL, \
    CONSTELLATION_GENERATION_URL, CONSTELLATION_SIMULATION_URL, MISSION_RESULTS_URL


# Create #
def create_ground_station(body):
    post_request(GROUND_STATION_URL, body)


def create_payload(body):
    post_request(PAYLOAD_URL, body)


def create_earth_mesh(body):
    post_request(EARTH_MESH_URL, body)


def create_sub_constellation(body):
    post_request(SUB_CONSTELLATION_URL, body)


def create_constellation(body):
    post_request(CONSTELLATION_URL, body)


def create_point_of_interest(body):
    post_request(POINT_OF_INTEREST_URL, body)


def create_performance_analysis_mission(body):
    post_request(CONSTELLATION_PERFORMANCE_ANALYSIS_URL, body)


def create_optimization_mission(body):
    post_request(CONSTELLATION_OPTIMIZATION_URL, body)


def create_generation_mission(body):
    post_request(CONSTELLATION_GENERATION_URL, body)


def create_simulation_mission(body):
    post_request(CONSTELLATION_SIMULATION_URL, body)


# Get Specific Mission/Object #
def get_ground_station(ground_station):
    return get_object(ground_station, GROUND_STATION_URL)


def get_payload(payload):
    return get_object(payload, PAYLOAD_URL)


def get_earth_mesh(earth_mesh):
    return get_object(earth_mesh, EARTH_MESH_URL)


def get_sub_constellation(sub_constellation):
    return get_object(sub_constellation, SUB_CONSTELLATION_URL)


def get_constellation(constellation):
    return get_object(constellation, CONSTELLATION_URL)


def get_point_of_interest(point_of_interest):
    return get_object(point_of_interest, POINT_OF_INTEREST_URL)


def get_performance_analysis_mission(performance_analysis_mission):
    return get_object(performance_analysis_mission, CONSTELLATION_PERFORMANCE_ANALYSIS_URL)


def get_optimization_mission(optimization_mission):
    return get_object(optimization_mission, CONSTELLATION_OPTIMIZATION_URL)


def get_generation_mission(generation_mission):
    return get_object(generation_mission, CONSTELLATION_GENERATION_URL)


def get_simulation_mission(simulation_mission):
    return get_object(simulation_mission, CONSTELLATION_SIMULATION_URL)


def get_performance_analysis_mission_id(performance_analysis_mission):
    return get_mission_id_with_url(performance_analysis_mission, CONSTELLATION_PERFORMANCE_ANALYSIS_URL)


def get_optimization_mission_id(optimization_mission):
    return get_mission_id_with_url(optimization_mission, CONSTELLATION_OPTIMIZATION_URL)


def get_generation_mission_id(generation_mission):
    return get_mission_id_with_url(generation_mission, CONSTELLATION_GENERATION_URL)


def get_simulation_mission_id(simulation_mission):
    return get_mission_id_with_url(simulation_mission, CONSTELLATION_SIMULATION_URL)


# Modify Missions/Objects #
def modify_ground_station(ground_station, new_ground_station):
    modify_object(ground_station, new_ground_station, GROUND_STATION_URL)


def modify_payload(payload, new_payload):
    modify_object(payload, new_payload, PAYLOAD_URL)


def modify_earth_mesh(earth_mesh, new_earth_mesh):
    modify_object(earth_mesh, new_earth_mesh, EARTH_MESH_URL)


def modify_sub_constellation(sub_constellation, new_sub_constellation):
    modify_object(sub_constellation, new_sub_constellation, SUB_CONSTELLATION_URL)


def modify_constellation(constellation, new_constellation):
    modify_object(constellation, new_constellation, CONSTELLATION_URL)


def modify_point_of_interest(point_of_interest, new_point_of_interest):
    modify_object(point_of_interest, new_point_of_interest, POINT_OF_INTEREST_URL)


def modify_performance_analysis_mission(performance_analysis_mission, new_performance_analysis_mission):
    modify_object(performance_analysis_mission, new_performance_analysis_mission,
                  CONSTELLATION_PERFORMANCE_ANALYSIS_URL)


def modify_optimization_mission(optimization_mission, new_optimization_mission):
    modify_object(optimization_mission, new_optimization_mission, CONSTELLATION_OPTIMIZATION_URL)


def modify_generation_mission(generation_mission, new_generation_mission):
    modify_object(generation_mission, new_generation_mission, CONSTELLATION_GENERATION_URL)


def modify_simulation_mission(simulation_mission, new_simulation_mission):
    modify_object(simulation_mission, new_simulation_mission, CONSTELLATION_SIMULATION_URL)


# Delete Missions/Objects #
def delete_ground_station(ground_station):
    delete_object(ground_station, GROUND_STATION_URL)


def delete_payload(payload):
    delete_object(payload, PAYLOAD_URL)


def delete_earth_mesh(earth_mesh):
    delete_object(earth_mesh, EARTH_MESH_URL)


def delete_sub_constellation(sub_constellation):
    delete_object(sub_constellation, SUB_CONSTELLATION_URL)


def delete_constellation(constellation):
    delete_object(constellation, CONSTELLATION_URL)


def delete_point_of_interest(point_of_interest):
    delete_object(point_of_interest, POINT_OF_INTEREST_URL)


def delete_performance_analysis_mission(performance_analysis_mission):
    delete_object(performance_analysis_mission, CONSTELLATION_PERFORMANCE_ANALYSIS_URL)


def delete_optimization_mission(optimization_mission):
    delete_object(optimization_mission, CONSTELLATION_OPTIMIZATION_URL)


def delete_generation_mission(generation_mission):
    delete_object(generation_mission, CONSTELLATION_GENERATION_URL)


def delete_simulation_mission(simulation_mission):
    delete_object(simulation_mission, CONSTELLATION_SIMULATION_URL)


# Get All Missions/Objects #
def get_all_ground_stations():
    return get_request(GROUND_STATION_URL)


def get_all_payloads():
    return get_request(PAYLOAD_URL)


def get_all_earth_meshes():
    return get_request(EARTH_MESH_URL)


def get_all_sub_constellations():
    return get_request(SUB_CONSTELLATION_URL)


def get_all_constellations():
    return get_request(CONSTELLATION_URL)


def get_all_points_of_interests():
    return get_request(POINT_OF_INTEREST_URL)


def get_all_performance_analysis_missions():
    return get_request(CONSTELLATION_PERFORMANCE_ANALYSIS_URL)


def get_all_optimization_missions():
    return get_request(CONSTELLATION_OPTIMIZATION_URL)


def get_all_generation_missions():
    return get_request(CONSTELLATION_GENERATION_URL)


def get_all_simulation_missions():
    return get_request(CONSTELLATION_SIMULATION_URL)


# Computation #
def compute_performance_analysis_mission(mission):
    compute_mission_from_url(mission, CONSTELLATION_PERFORMANCE_ANALYSIS_URL)


def compute_optimization_mission(mission):
    compute_mission_from_url(mission, CONSTELLATION_OPTIMIZATION_URL)


def compute_generation_mission(mission):
    compute_mission_from_url(mission, CONSTELLATION_GENERATION_URL)


def compute_simulation_mission(mission):
    compute_mission_from_url(mission, CONSTELLATION_SIMULATION_URL)


# Results #
def get_performance_analysis_mission_results(mission):
    return get_mission_results_from_url(mission, CONSTELLATION_PERFORMANCE_ANALYSIS_URL, MISSION_RESULTS_URL)


def get_optimization_mission_results(mission):
    return get_mission_results_from_url(mission, CONSTELLATION_OPTIMIZATION_URL, MISSION_RESULTS_URL)


def get_generation_mission_results(mission):
    return get_mission_results_from_url(mission, CONSTELLATION_GENERATION_URL, MISSION_RESULTS_URL)


def get_simulation_mission_results(mission):
    return get_mission_results_from_url(mission, CONSTELLATION_SIMULATION_URL, MISSION_RESULTS_URL)


def wait_and_get_performance_analysis_mission_results(mission):
    return wait_and_get_mission_results_from_url(mission, CONSTELLATION_PERFORMANCE_ANALYSIS_URL, MISSION_RESULTS_URL)


def wait_and_get_optimization_mission_results(mission):
    return wait_and_get_mission_results_from_url(mission, CONSTELLATION_OPTIMIZATION_URL, MISSION_RESULTS_URL)


def wait_and_get_generation_mission_results(mission):
    return wait_and_get_mission_results_from_url(mission, CONSTELLATION_GENERATION_URL, MISSION_RESULTS_URL)


def wait_and_get_simulation_mission_results(mission):
    return wait_and_get_mission_results_from_url(mission, CONSTELLATION_SIMULATION_URL, MISSION_RESULTS_URL)
