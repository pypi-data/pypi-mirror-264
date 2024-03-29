from dotenv import load_dotenv

load_dotenv()

import spacestudio
import numpy as np
from math import radians, degrees
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------------------------------- Connect API


base_url = spacestudio.log_base_url
mail = spacestudio.log_mail
password = spacestudio.log_password
spacestudio.connect(base_url, mail, password)

# ---------------------------------------------------------------------------------------------------- Objects definition

earthMesh = {  
	'name' : 'basic rectangular earth mesh', 
	'southernmostLatitude' : radians(40), 
	'northernmostLatitude' : radians(55), 
	'westernmostLongitude' : radians(-5), 
	'easternmostLongitude' : radians(10), 
	'rangeType' : 'NUMBER', 
	'numberOfLatitudes' : 30, 
	'numberOfLongitudes' : 30, 
}

spacestudio.constellation.delete_earth_mesh(earthMesh["name"])
spacestudio.constellation.create_earth_mesh(earthMesh)



angles = [10, 15, 20, 30]

# ---------------------------------------------------------------------------------------------------- Computation

results = []

for angle in angles:

    # Vary semi-view angle of the payload
    payload = {
    "name": "basic payload",
    "fieldOfViewType": "TYPE_CIRCULAR",
    "circularFOVDefinitionType": "ALTITUDE_AND_SEMI_VIEW_ANGLE",
    "constantParameterType": "SEMI_VIEW_ANGLE",
    "semiViewAngleCircularDefinition": radians(angle),
    "payloadPower": 10,
    "constantParameterChoice": "SAME",
    "telecomType": "NONE"
    }

    spacestudio.constellation.delete_payload(payload["name"])
    spacestudio.constellation.create_payload(payload)

    constellationGeometry = {
        "name": "basic constellation geometry",
        "constellationType": "CUSTOM",
        "planeDefinitionType": "ALTITUDE_AND_SUN_SYNCHRONOUS",
        "definitionType": "DELTA_RAAN",
        'altitude' : 600000, 
        "numberOfSpacecraftsPerPlane": 6,
        "numberOfPlanes": 4,
        "deltaRaan": radians(45),
        "minInitialRaan": radians(0),
        "firstPlaneInitialRaan": radians(0),
        "firstSpacecraftInitialInOrbitPosition" : radians(0),
        "payload": spacestudio.constellation.get_payload(payload["name"]),
        "interPlanePhasing": radians(60),
    }

    spacestudio.constellation.delete_sub_constellation(constellationGeometry["name"])
    spacestudio.constellation.create_sub_constellation(constellationGeometry)

    constellation = {
        "name": "basic constellation",
        "homogeneousConstellationGeometries": [spacestudio.constellation.get_sub_constellation(constellationGeometry["name"])]
    }

    spacestudio.constellation.delete_constellation(constellation["name"])
    spacestudio.constellation.create_constellation(constellation)

    
    performance_analysis_mission = {
    "name": "Batched performance analysis mission",
    "constellation": spacestudio.constellation.get_constellation(constellation["name"]),
    "earthMeshes": [spacestudio.constellation.get_earth_mesh(earthMesh["name"])],
    "simulationDate": "2022-01-01T12:00:00.000Z",
    "simulationDuration": 7*86400,
    "computeRevisit": True,
    "threshold": 1,
}

    spacestudio.constellation.delete_performance_analysis_mission(performance_analysis_mission["name"])
    spacestudio.constellation.create_performance_analysis_mission(performance_analysis_mission)

    # Compute and get results
    spacestudio.constellation.compute_performance_analysis_mission(performance_analysis_mission["name"])
    missionResults = (spacestudio.constellation.wait_and_get_performance_analysis_mission_results(performance_analysis_mission["name"]))

    # convert seconds in minutes
    meshPerformances = missionResults["results"]["meshPerformances"]
    pointRevisitTimeAverage = []
    for perf in meshPerformances:
        pointRevisitTimeAverage.append([point["metrics"]["statisticalMetrics"]["REVISIT_TIME"]["average"] / 60 for point in perf["points"]])

    results.append(pointRevisitTimeAverage)

# ---------------------------------------------------------------------------------------------------- Post-treatment

# Define x, y axis based on studied earth Mesh
earthMesh = spacestudio.constellation.get_earth_mesh(earthMesh["name"])
x = np.linspace(
    degrees(earthMesh["westernmostLongitude"]),
    degrees(earthMesh["easternmostLongitude"]),
    earthMesh["numberOfLongitudes"],
)
y = np.linspace(
    degrees(earthMesh["southernmostLatitude"]),
    degrees(earthMesh["northernmostLatitude"]),
    earthMesh["numberOfLatitudes"],
)
X, Y = np.meshgrid(x, y)

# Define figure subplots
fig, axs = plt.subplots(2, 2, constrained_layout=False)
fig.tight_layout(pad=4.0)
fig.suptitle("Revisit time average Vs. Semi-view angle", fontsize="x-large")

ax1 = axs[0, 0]
ax2 = axs[0, 1]
ax3 = axs[1, 0]
ax4 = axs[1, 1]
subplots = [ax1, ax2, ax3, ax4]

# Apply results to subplots
for i in range(len(subplots)):
    Z = np.reshape(results[i], (len(x), len(y)))
    ax = subplots[i]
    pc = ax.pcolormesh(X, Y, Z, cmap="jet", shading="gouraud")
    fig.colorbar(pc, ax=ax, format="%s min")
    ax.set_title("FOR " + str(angles[i]) + "°")
    ax.set_xlabel("Longitude (deg)")
    ax.set_ylabel("Latitude (deg)")

plt.subplots_adjust(wspace=0.8, hspace=0.8)
plt.show()
