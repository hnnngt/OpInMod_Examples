This repository contains basic examples on how to use `Open Inertia Modelling (OpInMod) <https://github.com/hnnngt/OpInMod>`_.
The example can be used to learn and understand the functionalities of OpInMod.

.. contents::
    :depth: 1
    :local:
    :backlinks: top

Installation
================

Download the repository using the green download button. 

You need a working Python 3 environment and OpInMod to run the examples. Please check `'Installation' <https://github.com/hnnngt/OpInMod/README.rst>`_ 
section of the OpInMod documentation. Required packages to run each example are listed in the respective section.

Contributing
================

Everybody is welcome to contribute by adding their own example, fix documentation, bugs and typos in existing examples, etc 
via a `pull request <https://github.com/hnnngt/opinmod_examples/pulls>`_.

Examples
=========

The following examples are based on oemof's `simple dispatch example <https://github.com/oemof/oemof-examples/tree/master/oemof_examples/oemof.solph/v0.4.x/simple_dispatch>`_.
The demand and feed-in time series are extracted from the simple dispatch example. 
The functionalities of OpInMod are explained stepwise and extended with each example. 

Example 1
---------

This example shows the functionalities of OpInMod.

The first example consists of one sink and four fossil fuel transformers and
the respective busses and sources:

* Hard Coal
* Natural Gas
* Lignite
* Oil

Apart from the oemof simple dispatch example, the following data sources are used

* input_data.csv and tranformer specifications from oemof's `simple dispatch example <https://github.com/oemof/oemof-examples/tree/master/oemof_examples/oemof.solph/v0.4.x/simple_dispatch>`_
* emission factors per commodity from `ENTSO-E's 2018 TYNDP <https://www.entsoe.eu/Documents/TYNDP%20documents/TYNDP2018/Scenarios%20Data%20Sets/Input%20Data.xlsx>`_
* inertia constant per generation type from `Thiesen et al. <https://doi.org/10.3390/en14051255>`_

Example 2
---------

The second example consists of one sink and four fossil fuel transformers and
the respective busses and sources:

* Hard Coal
* Natural Gas
* Lignite
* Oil

Added to the second example are two renewable sources:

* Solar PV
* Wind turbine

The wind turbine is able to provide synthetic inertia

Data
----
* Normalized power vs. normalized rotational speed characteristic of the `NREL 5MW wind turbine <https://doi.org/10.2172/947422>`_

Example 3
---------

The third example consists of one sink and four fossil fuel transformers and
the respective busses and sources as well as two renewable sources:

* Hard Coal
* Natural Gas
* Lignite
* Oil

* Solar PV
* Wind turbine

The wind turbine is able to provide synthetic inertia

Added to the third example is a synchronously connected storage unit; in this case
a synchronous condenser.

Example 4
---------

The fourth example consists of one sink and four fossil fuel transformers and
the respective busses and sources as well as two renewable sources and a
synchronously connected storage unit:

* Hard Coal
* Natural Gas
* Lignite
* Oil

* Solar PV
* Wind turbine

* Synchronous condenser

The wind turbine is able to provide synthetic inertia

Added to the fourth example is a battery storage unit providing
synthetic inertia

License
=======

Copyright (c) 2021 Henning Thiesen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

