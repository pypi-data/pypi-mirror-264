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

# Perform lifetime simulation mission:
# Modify some parameters between the maneuvers : propellantMass
# Display mass evolution and orbital elements evolution.

# ---------------------------------------------------------------------------------------------------- initialization

initialOrbitName = "SSO-600-km-DEMO"
spacecraftName = "Spacecraft-DEMO"
platformMass=150
thrusterMass=5.0


# ---------------------------------------------------------------------------------------------------- computation

createOrbit(
    name=initialOrbitName,
    type="Circular",
    sunSynchronousOrbit=True,
    altitude=600e3,
    ltan=12 * 3600,
)
initialOrbit = spacestudio.simulation.get_orbit(initialOrbitName)

createSpacecraft(
    name=spacecraftName,
    thrust=14e-3,
    thrusterPower=200,
    isp=850,
    solarArrayPower=260,
    platformPower=300,
    platformMass=80,
    thrusterMass=5,
    propellantMass=10,
    nominalCapacity=560,
    dragModelDefined=True,
    attitudeModelDefined=True,
)

spacecraft = spacestudio.simulation.get_spacecraft(spacecraftName)

# ---------------------------------------------------------------------------------------------------- maneuver n°1: leop transfer

missionName = "LEOP transfer"
createTransferMission(
    name=missionName,
    spacecraft=spacecraft,
    initialOrbit=initialOrbit,
    targetDefinition = 'DELTA',
    deltaSemiMajorAxis=-100e3,
    deltaInclination=0,
)
print(missionName, "running...")
maneuver1 = computeAndGetResults(missionName=missionName)

# ---------------------------------------------------------------------------------------------------- update parameters between maneuvers

## UPDATE PROPELLANT MASS
modifyPropellantMass(
    spacecraft=spacecraft,
    mass=maneuver1["results"]["maneuverReport"]["totalConsumption"],
)
spacecraft = spacestudio.simulation.get_spacecraft(spacecraftName)


## CREATE A NEW INITIAL ORBIT FROM PREVIOUS RESULTS
currentOrbitName = "intermediate orbit"
createOrbitFromResults(results=maneuver1, newOrbitName=currentOrbitName)
currentOrbit = spacestudio.simulation.get_orbit(currentOrbitName)

# ---------------------------------------------------------------------------------------------------- maneuver n°2: station keeping

missionName = "STATION KEEPING"
missionDuration = 50 * 86400
smaTopMargin = 100
smaBottomMargin = 100
createStationKeepingMission(missionName,
    spacecraft,
    currentOrbit, 
   smaTopMargin,
   smaBottomMargin,
   missionDuration,
   ephemeridesStepInSeconds=3600
)

print(missionName, "running...")
maneuver2 = computeAndGetResults(missionName=missionName)

# ---------------------------------------------------------------------------------------------------- update parameters between maneuvers

## UPDATE PROPELLANT MASS
modifyPropellantMass(
    spacecraft=spacecraft,
    mass=maneuver2["results"]["maneuverReport"]["totalConsumption"],
)

spacecraft = spacestudio.simulation.get_spacecraft(spacecraftName)

## CREATE A NEW INITIAL ORBIT FROM PREVIOUS RESULTS
currentOrbitName = "intermediate orbit"
createOrbitFromResults(results=maneuver2, newOrbitName=currentOrbitName)
currentOrbit = spacestudio.simulation.get_orbit(currentOrbitName)

# ---------------------------------------------------------------------------------------------------- maneuver n°3: deorbitation

missionName = "DEORBITATION"
createTransferMission(
    name=missionName,
    spacecraft=spacecraft,
    initialOrbit=currentOrbit,
    targetDefinition= 'DELTA',
    deltaSemiMajorAxis=-100e3,
    deltaInclination=0,
)
print(missionName, "running...")
maneuver3 = computeAndGetResults(missionName=missionName)

# ---------------------------------------------------------------------------------------------------- Display ephemerides with matplotlib



import matplotlib.pyplot as plt

maneuvers = [maneuver1, maneuver2, maneuver3]
current_spacecraft_mass = []
keplerianSma = []
angles = []
simulationDuration = []
lastValue = 0

for maneuver in maneuvers:

    ephemerides = maneuver["results"]["ephemerides"]
    duration = []


    for ephemeris in ephemerides:
        duration.append((ephemeris[0] / 86400) + lastValue)
        current_spacecraft_mass.append(ephemeris[41])
        keplerianSma.append(ephemeris[24] / 1000)

    lastValue = duration[-1]
    simulationDuration.extend(duration)


fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(simulationDuration, current_spacecraft_mass )
ax2.plot(simulationDuration, keplerianSma)

ax1.set(
    xlabel="Simulation Duration (days)",
    ylabel=" mass (kg)",
    title="Total spacecraft mass over time",
)

ax2.set(
    xlabel="Simulation Duration (days)",
    ylabel="sma (km)",
    title="Semi major axis over time",
)

ax1.grid()
ax2.grid()

fig.tight_layout()
plt.show()
print("")
