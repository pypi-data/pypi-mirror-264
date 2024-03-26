#############################################################
stereoid
#############################################################

Stereoid packages together a set of software tools that are used in the design
and analysis of the Harmony satellite mission.

=======================================================
Setting up your development environment to run stereoid
=======================================================
To be able to run the Jupyter Notebooks and use the modules defined in the
library you will need to install a few dependencies. Setting up a virtual
environment and running "``pip install .``" should automatically fetch and install
the necessary packages. Detailed instructions on how to do so follow:

You will need a recent version of Python installed on your system. We suggest
3.9 or later but 3.8 is also know to work. Once you have Python, you can create
a virtual environment so that you can install packages in isolation. You can do
this by running the following command on Unix/macOS:

``python3 -m venv drama-env``

or on Windows:

``py -m venv drama-env``

This will create a folder called "``drama-env``" in the folder where the previous
command was ran. All packages will be installed in this folder. Now to activate
this environment run this on Unix/macOS:

``source drama-env/bin/activate``

or on Windows:

``.\drama-env\Scripts\activate``

Now change to the directory where you have downloaded the stereoid
package to and execute:
git switch develop
pip install -e .

The first command switches to the develop branch and the second installs the
package. Make sure that "``pip install -e .``" is ran from the root level of the git
repository, ie from the directory where the ``setup.py`` and ``README.rst`` files
are.

After this you can install Jupyter Lab (if you don't already have it)
and start running the Jupyter Notebooks.

========================================
Running the Harmony scientific workbench
========================================
The package provides a cli program that sets up a simulation scenario, reads the
wave spectra from the SWAN model and runs the ocean scientific workbench for the
Harmony mission. To run, execute:
``harmulator_fwd [--debug] /path/to/params_scientific_workbench.py``
The --debug flag provides additional information in the console log. A sample
``params_scientific_workbench.py`` is provided in the ``PAR`` directory of this
repository.
