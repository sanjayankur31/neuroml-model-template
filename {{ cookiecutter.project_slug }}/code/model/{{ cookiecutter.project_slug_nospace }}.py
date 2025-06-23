#!/usr/bin/env python3
"""
{{ cookiecutter.short_description }}

Copyright 2025 {{ cookiecutter.author_name }}
Author: {{ cookiecutter.author_name }}<{{ cookiecutter.author_email }}>
"""


import typing
import logging
import neuroml
import typer
from neuroml.utils import component_factory
from pyneuroml.io import write_neuroml2_file
from pyneuroml.lems import generate_lems_file_for_neuroml
from pyneuroml.runners import run_lems_with


class {{ cookiecutter.project_slug_nospace }}(object):

    """{{ cookiecutter.project_name }} model in NeuroML"""
    network_name = "{{ cookiecutter.project_slug }}"
    nml_document = component_factory(neuroml.NeuroMLDocument, id=network_name)

    def __init__(self, neuroml_file: typing.Optional[str] = None, seed: typing.Optional[str] = None, lems_file: typing.Optional[str] = None):
        """Initialise the model from a parameter file.

        :param neuroml_file: name of NeuroML file to serialise model to
        :type neuroml_file: str
        :param seed: model/simulation seed
        :type seed: str
        :param lems_file: name of LEMS simulation file
        :type lems_file: str
        """
        with open("parameters/general.json") as f:
            general_params = json.load(f)

        self.seed = general_params.get("seed", seed if seed else "1234")
        self.neuroml_file = general_params.get("neuroml_file", neuroml_file if neuroml_file else f"{self.network_name}.net.nml")
        self.lems_file = general_params.get("lems_file", lems_file if lems_file else f"LEMS_test_Golgi_cells_{self.seed}.xml")

        if general_params.get("unused", None):
            logger.debug(f"Unused parameters in general.json: {general_params.get(unused)}")

        # set up a logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging_level if logging_level else logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging_level if logging_level else logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.propagate = False

        # set up cli
        self.app = typer.Typer()
        self.app.command()(self.create_model)
        self.app.command()(self.create_simulation)
        self.app.command()(self.simulate)


    def create(self):
        """Create the model"""
        self.logger.info("Creating model")
        # create and add more methods here as required
        self.create_network()

        # write model to file
        write_neuroml2_file(self.nml_document, self.neuroml_file)

    def create_network(self):
        """Create network"""
        self.network = self.nml_document.add(neuroml.Network, id="{{ cookiecutter.project_slug }}")

    def create_simulation(self, lems_file: typing.Optional[str]):
        """Create simulation
        :param lems_file: name of LEMS file to serialise simulation to
        :type lems_file: str
        """
        if lems_file:
            self.lems_file = lems_file
        else:
            # if not already set, use a default
            if not hasattr(self, "lems_file"):
                self.logger.error("No file name set for lems_file before, please pass a value")
                return

        quantities, sim = generate_lems_file_for_neuroml(
            sim_id="{{ cookiecutter.project_slug }}",
            neuroml_file=self.neuroml_file,
            target=self.network,
            duration="1500 ms",
            dt="0.01",
            lems_file_name=self.lems_file,
            target_dir=".",
        )

    def simulate(self, skip_run: bool = True, only_generate_scripts: bool = False):
        """Simulate the model

        :param skip_run: only parse file but do not generate scripts or run
        :type skip_run: bool
        :param only_generate_scripts: toggle whether only the runner script
            should be generated
        :type only_generate_scripts: bool
        """
        # https://pyneuroml.readthedocs.io/en/development/pyneuroml.runners.html#pyneuroml.runners.run_lems_with
        # you can also use `pynml ..` from the command line to do this
        {% if cookiecutter.simulation_engine|lower == "neuron" -%}
        run_lems_with(
            engine="jneuroml_neuron", lems_file_name=self.lems_file,
            skip_run=skip_run,
            only_generate_scripts=only_generate_scripts)
        {% elif cookiecutter.simulation_engine|lower == "netpyne" -%}
        run_lems_with(
            engine="jneuroml_netpyne", lems_file_name=self.lems_file,
            skip_run=skip_run,
            only_generate_scripts=only_generate_scripts)
        {% elif cookiecutter.simulation_engine|lower == "brian" -%}
        run_lems_with(
            engine="jneuroml_brian", lems_file_name=self.lems_file,
            skip_run=skip_run,
            only_generate_scripts=only_generate_scripts)
        {-% endif -%}


if __name__ == "__main__":
    model = {{ cookiecutter.project_slug_nospace }}()
    model.app()
