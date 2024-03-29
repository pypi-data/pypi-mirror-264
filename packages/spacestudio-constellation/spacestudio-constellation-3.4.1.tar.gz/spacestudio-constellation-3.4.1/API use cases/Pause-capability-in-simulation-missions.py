from dotenv import load_dotenv
load_dotenv()

import numpy as np
import spacestudio
from use_cases_tools import *

# ---------------------------------------------------------------------------------------------------- connect API

base_url = spacestudio.log_base_url
mail = spacestudio.log_mail
password = spacestudio.log_password
spacestudio.connect(base_url, mail, password)

# ---------------------------------------------------------------------------------------------------- purpose

# API Pause capability for simulation missions
# - define an orbital transfer between SSO 600km and SSO 800km
# - compute the mission in two different ways :
# - 1st way: update spacecraft OAP before the mission (fixed duty cycle)
# - 2nd way: update spacecraft OAP every five days with the durationUntilPause feature (dynamic duty cycle)
# - write results in .xlsx files
# - compare results using matplotlib

# ---------------------------------------------------------------------------------------------------- initialization

initialOrbitName = "SSO-600-km-DEMO"
finalOrbitName = "SSO-800-km-DEMO"
spacecraftName = "Spacecraft-DEMO"
missionName = "TRANSFER-DEMO"
durationUntilPause = 5 * 86400

# ---------------------------------------------------------------------------------------------------- computation

maneuvers = []

for updateOAP in [0, 1]:

    createOrbit(
        name=initialOrbitName,
        type="Circular",
        sunSynchronousOrbit=True,
        altitude=600e3,
        ltan=12 * 3600,
    )
    initialOrbit = spacestudio.simulation.get_orbit(initialOrbitName)

    createOrbit(
        name=finalOrbitName,
        type="Circular",
        sunSynchronousOrbit=True,
        altitude=800e3,
        ltan=12 * 3600,
    )
    finalOrbit = spacestudio.simulation.get_orbit(finalOrbitName)

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

    createTransferMission(
        name=missionName,
        spacecraft=spacecraft,
        targetDefinition="TARGET_ORBIT",
        initialOrbit=initialOrbit,
        targetOrbit=finalOrbit,
    )

    if updateOAP == 0:

        fixedOAP = updateSpacecraftOAP(spacecraft=spacecraft, orbit=initialOrbit)
        results = computeAndGetResults(missionName=missionName)

    elif updateOAP == 1:

        oaps = computeAndUpdateOAP(
            missionName=missionName, durationUntilPause=durationUntilPause
        )

        spacestudio.simulation.get_paused_mission_results_merged(missionName)
        missionName = missionName + " - merged"
        results = spacestudio.simulation.get_mission_results(missionName)

    maneuvers.append(results)
    export_mission_results_in_xlsx(missionName)

# ---------------------------------------------------------------------------------------------------- Display ephemerides with matplotlib
import matplotlib.pyplot as plt

# fixed duty cycle
thrusterPower = spacecraft["thruster"]["power"]
fixedDC = (fixedOAP / thrusterPower) * 100
x1 = list(
    np.linspace(
        0,
        maneuvers[0]["results"]["maneuverReport"]["simulationDuration"] / 86400,
        num=10,
    )
)
y1 = [fixedDC] * 10

# dynamic duty cycle
end = maneuvers[1]["results"]["maneuverReport"]["simulationDuration"]
x2 = list(np.arange(0, end / 86400, durationUntilPause/86400))
x2.append(end / 86400)
y2 = []
for oap in oaps:
    y2.append((oap / thrusterPower) * 100)
y2.insert(0, y2[0])


fig1, ax = plt.subplots()
(line1,) = ax.plot(x1, y1, label="Fixed Duty Cycle")
(line2,) = ax.plot(x2, y2, drawstyle="steps", label="Dynamic Duty Cycle")
ax.plot(x2, y2, "o--", color="grey", alpha=0.3)


ax.set(
    xlabel="Simulation duration (Days)",
    ylabel="Duty Cycle (%)",
    title="Duty Cycle comparison",
)
ax.grid()
ax.legend(handles=[line1, line2])


simulationDuration = []
totalConsumption = []
totalNumberOfBurns = []

for maneuver in maneuvers:
    report = maneuver["results"]["maneuverReport"]
    simulationDuration.append(round(report["simulationDuration"] / 86400, 2))
    totalConsumption.append(round(report["totalConsumption"], 2))
    totalNumberOfBurns.append(report["totalNumberOfBurns"])

names = ["Fixed", "Dynamic"]

fig2, axs = plt.subplots(1, 3, figsize=(8, 4), sharey=False)
bar0 = axs[0].bar(names, simulationDuration, color=["b", "g"], alpha=0.5)
axs[0].bar_label(bar0)
axs[0].set_ylabel("Simulation duration (Days)")
bar1 = axs[1].bar(names, totalConsumption, color=["b", "g"], alpha=0.5)
axs[1].bar_label(bar1)
axs[1].set_ylabel("Total consumption (Kg)")
bar2 = axs[2].bar(names, totalNumberOfBurns, color=["b", "g"], alpha=0.5)
axs[2].bar_label(bar2)
axs[2].set_ylabel("Total number of burns")
fig2.suptitle("Manoeuvring performance")
fig2.tight_layout()

plt.show()
