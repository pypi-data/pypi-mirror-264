from dotenv import load_dotenv
load_dotenv()

import spacestudio
from use_cases_tools import *


# ---------------------------------------------------------------------------------------------------- connect API

base_url = spacestudio.log_base_url
mail = spacestudio.log_mail
password = spacestudio.log_password
spacestudio.connect(base_url, mail, password)

# ---------------------------------------------------------------------------------------------------- purpose

# Simple RAAN Mission n°1 :
# - define an orbit, a spacecraft, and a 2 degrees RAAN phasing mission
# - compute the mission
# - display the maneuver report and the orbit properties in the python console
# - write results in .xlsx file
# - plot ephemerides (Relative RAAN) and save figure as .png, using matplotlib


# ---------------------------------------------------------------------------------------------------- initialization

initialOrbitName = "SSO-600-km-DEMO"
spacecraftName = "Spacecraft-DEMO"
missionName = "RAAN-DEMO"

# ---------------------------------------------------------------------------------------------------- computation

createOrbit(
    name=initialOrbitName,
    type="Circular",
    sunSynchronousOrbit=True,
    altitude=700e3,
    ltan=6 * 3600,
)
initialOrbit = spacestudio.simulation.get_orbit(initialOrbitName)

createSpacecraft(
    name=spacecraftName,
    thrust=14e-3,
    thrusterPower=200,
    isp=850,
    solarArrayPower=260,
    platformPower=30,
    platformMass=80,
    thrusterMass=5,
    propellantMass=10,
    nominalCapacity=560,
    dragModelDefined=True,
    attitudeModelDefined=True,
)
spacecraft = spacestudio.simulation.get_spacecraft(spacecraftName)

createRaanMission(
    name=missionName,
    spacecraft=spacecraft,
    initialOrbit=initialOrbit,
    optimizationType="ΔT",
    targetDeltaRaan=2 * (pi / 180),
    targetDeltaVmax=getMaxDeltaV(spacecraft=spacecraft) - 1,
)
results = computeAndGetResults(missionName=missionName)


# ---------------------------------------------------------------------------------------------------- print results in .xlsx
export2csv = False
if (export2csv):
    export_mission_results_in_xlsx(missionName)

# ---------------------------------------------------------------------------------------------------- Display ephemerides with matplotlib

import matplotlib.pyplot as plt

ephemerides = results["results"]["ephemerides"]
simulationDuration = []
relativeRaan = []

for ephemeride in ephemerides:
    simulationDuration.append(ephemeride[0] / 86400)
    relativeRaan.append(ephemeride[56] * (180 / pi))

fig, ax = plt.subplots()
ax.plot(simulationDuration, relativeRaan)

ax.set(
    xlabel="Simulation Duration (days)",
    ylabel="Relative RAAN (deg)",
    title="Relative RAAN over time",
)
ax.grid()
plt.show()
