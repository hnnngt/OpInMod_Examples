"""
General description
-------------------
This example shows the functionalities of OpInMod.

The first example consists of one sink and four fossil fuel transformers and
the respective busses and sources:
* Hard Coal
* Natural Gas
* Lignite
* Oil

Data
----
* input_data.csv and tranformer specifications from oemof's `simple dispatch example <https://github.com/oemof/oemof-examples/tree/master/oemof_examples/oemof.solph/v0.4.x/simple_dispatch>`_
* emission factors per commodity from `ENTSO-E's 2018 TYNDP <https://www.entsoe.eu/Documents/TYNDP%5C%20documents/TYNDP2018/Scenarios%5C%20Data%5C%20Sets/Input%5C%20Data.xlsx>`_
* inertia constant per generation type from `Thiesen et al. <https://doi.org/10.3390/en14051255>`_

Installation requirements
-------------------------
You need a working Python 3 environment and OpInMod to run the examples.
Please check `'Installation' <https://github.com/hnnngt/OpInMod/README.rst>`_
section of the OpInMode documentation. Required packages to run each
example are listed in the respective section.

To visualise the results, the matplotlib library has to be installed.
"""


# package import
import os
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdt

import opinmod as oim


# model initialisation

# get current working directory
path = os.getcwd()

# import data
dataDf = pd.read_csv(
    path + '/example_1/input_data.csv'
)

load = dataDf['demand_el'].to_list()
wind = dataDf['wind'].to_list()
pv = dataDf['pv'].to_list()

# set up time series
timePeriods = len(load)
timeIdx = pd.date_range(
    start='20/8/2020',
    periods=timePeriods,
    freq='H'
)

# set up solver
solver = 'cbc'

# specify emission factors [t/MWh]
emFacHardCoal = 0.3384
emFacNatGas = 0.2052
emFacLignite = 0.2808
emFacOil = 0.3636

# build energy system
energysystem = oim.EnergySystem(
    timeindex=timeIdx,
    minimum_system_synchronous_inertia=1963.6,
    minimum_system_inertia=3963.3,
    emulated_inertia_constant=3.5
)

# resource buses
busHardCoal = oim.Bus(
    label="bus_hard_coal"
)
busNaturalGas = oim.Bus(
    label="bus_natural_gas"
)
busOil = oim.Bus(
    label="bus_oil"
)
busLignite = oim.Bus(
    label="bus_lignite"
)

# electricity
busElectricity = oim.Bus(
    label='bus_electricity'
)

# bus inertia
busInertia = oim.Bus(
    label='bus_inertia',
    balanced=False
)

energysystem.add(
    busHardCoal,
    busNaturalGas,
    busOil,
    busLignite,
    busElectricity,
    busInertia
)

# build sources
sourceHardCoal = oim.Source(
    label='source_hard_coal',
    outputs={
        busHardCoal:oim.Flow()
    }
)
sourceNaturalGas = oim.Source(
    label='source_natural_gas',
    outputs={
        busNaturalGas:oim.Flow()
    }
)
sourceOil = oim.Source(
    label='source_oil',
    outputs={
        busOil:oim.Flow()
    }
)
sourceLignite = oim.Source(
    label='source_lignite',
    outputs={
        busLignite:oim.Flow()
    }
)

energysystem.add(
    sourceHardCoal,
    sourceNaturalGas,
    sourceOil,
    sourceLignite
)

# create transformer
transformerHardCoal = oim.Transformer(
    label='transformer_hard_coal',
    inputs={
        busHardCoal: oim.Flow()
    },
    outputs={
        busElectricity: oim.Flow(
            nominal_value=20.2*10**6,
            variable_costs=25),
        busInertia: oim.Inertia(
            inertia_constant=4.25,
            inertia_costs=0,
            apparent_power=20.2*10**6,
            provision_type='synchronous_generator',
            minimum_stable_operation=0.3)
        },
    conversion_factors={
        busElectricity: 0.39
    }
)

transformerNaturalGas = oim.Transformer(
    label='transformer_natural_gas',
    inputs={
        busNaturalGas: oim.Flow()
    },
    outputs={
        busElectricity: oim.Flow(
            nominal_value=41*10**6,
            variable_costs=40
        ),
        busInertia: oim.Inertia(
            inertia_constant=3.5,
            inertia_costs=0,
            apparent_power=41*10**6,
            provision_type='synchronous_generator',
            minimum_stable_operation=0.3
        )
    },
    conversion_factors={
        busElectricity: 0.5
    }
)

transformerOil = oim.Transformer(
    label='transformer_oil',
    inputs={
        busOil: oim.Flow()
    },
    outputs={
        busElectricity: oim.Flow(
            nominal_value=5*10**6,
            variable_costs=50
        ),
        busInertia: oim.Inertia(
            inertia_constant=3.5,
            inertia_costs=0,
            apparent_power=5*10**6,
            provision_type='synchronous_generator',
            minimum_stable_operation=0.4
        )
    },
    conversion_factors={
        busElectricity: 0.28
    }
)

transformerLignite = oim.Transformer(
    label='transformer_lignite',
    inputs={
        busLignite: oim.Flow()
    },
    outputs={
        busElectricity: oim.Flow(
            nominal_value=11.8*10**6,
            variable_costs=19
        ),
        busInertia: oim.Inertia(
            inertia_constant=3.5,
            inertia_costs=0,
            apparent_power=11.8*10**6,
            provision_type='synchronous_generator',
            minimum_stable_operation=0.3
        )
    },
    conversion_factors={
        busElectricity: 0.41
    }
)

# add transfomers to energysystem
energysystem.add(
    transformerHardCoal,
    transformerNaturalGas,
    transformerOil,
    transformerLignite
)

# build sinks
sinkDemand = oim.Sink(
    label='sink_load',
    inputs={
        busElectricity: oim.Flow(
            nominal_value=85*10**6,
            fix=load
        )
    }
)

sinkExcess = oim.Sink(
    label='sink_excess',
    inputs={
        busElectricity: oim.Flow(
            variable_costs=1
        )
    }
)

# add sinks to energysystem
energysystem.add(
    sinkDemand,
    sinkExcess
)


# create an optimisation problem
om = oim.Model(
    energysystem
)

# solve the energy model using solver
om.solve(
    solver=solver,
    solve_kwargs={
        'tee': False
    }
)

# extract results
results = om.results()

# import additional package for easier result access
from oemof.solph.processing import convert_keys_to_strings

# convert result key to strings
results = convert_keys_to_strings(results)

# access flows
flowHardCoal = results[('source_hard_coal', 'bus_hard_coal')]['sequences']['flow'] * emFacHardCoal
flowNaturalGas = results[('source_natural_gas', 'bus_natural_gas')]['sequences']['flow'] * emFacNatGas
flowLignite = results[('source_lignite', 'bus_lignite')]['sequences']['flow'] * emFacLignite
flowOil = results[('source_oil', 'bus_oil')]['sequences']['flow'] * emFacOil

flowHardCoalEl = results[('transformer_hard_coal', 'bus_electricity')]['sequences']['flow']
flowNaturalGasEl = results[('transformer_natural_gas', 'bus_electricity')]['sequences']['flow']
flowLigniteEl = results[('transformer_lignite', 'bus_electricity')]['sequences']['flow']
flowOilEl = results[('transformer_oil', 'bus_electricity')]['sequences']['flow']

flowDemand = results[('bus_electricity', 'sink_load')]['sequences']['flow']
flowExcess = results[('bus_electricity', 'sink_excess')]['sequences']['flow']

# plot flow results
fig, ax = plt.subplots()
plt.stackplot(timeIdx, flowLigniteEl, flowHardCoalEl, flowNaturalGasEl, flowOilEl, labels=['Lignite', 'Hard Coal', 'Natural Gas', 'Oil'], alpha=0.4, colors=['#8B4513', '#000000', '#B0C4DE', '#191970'])
plt.plot(timeIdx, flowDemand, label='Load', color='#FF0000')
plt.plot(timeIdx, flowExcess, label='Excess', color='#FF00FF')
ax.legend(loc='lower left')
ax.set_xlabel('Time')
ax.set_ylabel('Power [MW]')
myFmt = mdt.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(myFmt)
ax.grid()
fig.set_size_inches(8, 4.5)
fig.tight_layout()
plt.savefig(path + '/example_1/flow_opinmod.pdf')
plt.close()

# access overall apparent power
totalAppPower = results[('transformer_hard_coal', 'bus_inertia')]['sequences']['apparent_power'] * results[('transformer_hard_coal', 'bus_inertia')]['sequences']['source_inertia'] + results[('transformer_lignite', 'bus_inertia')]['sequences']['apparent_power'] * results[('transformer_lignite', 'bus_inertia')]['sequences']['source_inertia'] + results[('transformer_oil', 'bus_inertia')]['sequences']['apparent_power'] * results[('transformer_oil', 'bus_inertia')]['sequences']['source_inertia'] + results[('transformer_natural_gas', 'bus_inertia')]['sequences']['apparent_power'] * results[('transformer_natural_gas', 'bus_inertia')]['sequences']['source_inertia']

kinEnergyHardCoal = results[('transformer_hard_coal', 'bus_inertia')]['sequences']['apparent_power'] * results[('transformer_hard_coal', 'bus_inertia')]['sequences']['source_inertia'] * results[('transformer_hard_coal', 'bus_inertia')]['sequences']['inertia_constant']

kinEnergyNatGas = results[('transformer_natural_gas', 'bus_inertia')]['sequences']['apparent_power'] * results[('transformer_natural_gas', 'bus_inertia')]['sequences']['source_inertia'] * results[('transformer_natural_gas', 'bus_inertia')]['sequences']['inertia_constant']

kinEnergyLignite = results[('transformer_lignite', 'bus_inertia')]['sequences']['apparent_power'] * results[('transformer_lignite', 'bus_inertia')]['sequences']['source_inertia'] * results[('transformer_lignite', 'bus_inertia')]['sequences']['inertia_constant']

kinEnergyOil = results[('transformer_oil', 'bus_inertia')]['sequences']['apparent_power'] * results[('transformer_oil', 'bus_inertia')]['sequences']['source_inertia'] * results[('transformer_oil', 'bus_inertia')]['sequences']['inertia_constant']

inertiaHardCoal = kinEnergyHardCoal/totalAppPower
inertiaNaturalGas = kinEnergyNatGas/totalAppPower
inertiaLignite = kinEnergyLignite/totalAppPower
inertiaOil = kinEnergyOil/totalAppPower

inertiaSync = inertiaHardCoal + inertiaNaturalGas + inertiaLignite + inertiaOil

minSyncInertia = (0.5*om.es.minimum_system_synchronous_inertia*4*math.pi**2*50**2)/(totalAppPower)
minSysInertia = (0.5*om.es.minimum_system_inertia*4*math.pi**2*50**2)/(totalAppPower)

# plot inertia results
fig, ax = plt.subplots()
plt.stackplot(timeIdx, inertiaLignite, inertiaHardCoal, inertiaNaturalGas, inertiaOil, labels=['Lignite', 'Hard Coal', 'Natural Gas', 'Oil'], alpha=0.4, colors=['#8B4513', '#000000', '#B0C4DE', '#191970'])
plt.plot(timeIdx, minSyncInertia, label='Min Sync. Inertia', color='black')
plt.plot(timeIdx, minSysInertia, label='Min Inertia', color='black', linestyle='-.')
ax.legend(loc='lower left')
ax.set_xlabel('Time')
ax.set_ylabel('Power System Inertia [s]')
myFmt = mdt.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(myFmt)
ax.grid()
fig.set_size_inches(8, 4.5)
fig.tight_layout()
plt.savefig(path + '/example_1/inertia_opinmod.pdf')
plt.close()

# print results
print('Electricity Hard Coal: ' + str(sum(flowHardCoalEl)))
print('Electricity Natural Gas: ' + str(sum(flowNaturalGasEl)))
print('Electricity Lignite: ' + str(sum(flowLigniteEl)))
print('Electricity Oil: ' + str(sum(flowOilEl)))
print('Excess: ' + str(sum(flowExcess)))
print('CO2 Emissions: ' + str(sum(flowHardCoal + flowNaturalGas + flowLignite + flowOil)))
