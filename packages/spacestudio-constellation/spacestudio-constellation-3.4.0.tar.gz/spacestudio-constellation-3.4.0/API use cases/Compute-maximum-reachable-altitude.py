from dotenv import load_dotenv
load_dotenv()

import spacestudio
from use_cases_tools import *
# ---------------------------------------------------------------------------------------------------- purpose

# - Create a batch of simulations computing the maximum altitude reachable for different mission durations (7days, 14 days, 21 days)
# - Display results with matplotlib

# ---------------------------------------------------------------------------------------------------- connect API

base_url = spacestudio.log_base_url
mail = spacestudio.log_mail
password = spacestudio.log_password
spacestudio.connect(base_url, mail, password)


# ---------------------------------------------------------------------------------------------------- initialization

initialOrbitName = "SSO-600-km-DEMO"
finalOrbitName = "SSO-800-km-DEMO"
spacecraftName = "Spacecraft-DEMO"
missionName = "TRANSFER-DEMO"

# ---------------------------------------------------------------------------------------------------- computation

days = [7, 14, 21]
platformMass = [10, 50, 80]


totalAltitudes = []
for day in days:
    altitudes = []
    for mass in platformMass:

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
            platformPower=30,
            platformMass=mass,
            thrusterMass=5,
            propellantMass=10,
            nominalCapacity=560,
            dragModelDefined=True,
            attitudeModelDefined=True,
        )
        spacecraft = spacestudio.simulation.get_spacecraft(spacecraftName)

        updateSpacecraftOAP(spacecraft=spacecraft, orbit=initialOrbit)

        missionName = "ALTITUDE-MAX-DEMO"
        createTransferMission(
            name=missionName,
            targetDefinition="DELTA",
            spacecraft=spacecraft,
            initialOrbit=initialOrbit,
            deltaSemiMajorAxis=+5000e3,
            deltaInclination=0,
            durationUntilPause=day * 86400,
        )
        results = computeAndGetResults(missionName=missionName)
        altitudes.append(
        (
            results["results"]["finalOrbit"]["altitude"]
            - results["results"]["initialOrbit"]["altitude"]
        )
        / 1000
    )

    totalAltitudes.append(altitudes)

# ---------------------------------------------------------------------------------------------------- end

import matplotlib.pyplot as plt


fig, ax = plt.subplots()
(line1,) = ax.plot(totalAltitudes[0], platformMass, label="7 Days")
(line2,) = ax.plot(totalAltitudes[1], platformMass, label="14 Days")
(line3,) = ax.plot(totalAltitudes[2], platformMass, label="21 Days")

ax.set(
    xlabel="Altitude change (km)",
    ylabel="Payload mass (kg)",
    title="Altitude performance from SSO 600 km",
)
ax.grid()
ax.set(ylim=(min(platformMass), max(platformMass)))
ax.legend(handles=[line1, line2, line3])

plt.show()
