#!/usr/bin/env python3
"""
{{ cookiecutter.short_description }}

Copyright 2025 {{ cookiecutter.author_name }}
Author: {{ cookiecutter.author_name }}<{{ cookiecutter.author_email }}>
"""


import neuroml
from neuroml.utils import component_factory


class {{ cookiecutter.project_slug_nospace }}(object):

    """{{ cookiecutter.project_name }} model in NeuroML"""
    nml_document = component_factory(neuroml.NeuroMLDocument, id="{{ cookiecutter.project_slug }}")

    # set up a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.propagate = False

    def __init__(self, neuroml_file: typing.Optional[str] = None):
        """Init

        :param neuroml_file: name of NeuroML file to serialise model to
        :type neuroml_file: str
        """
        if neuroml_file:
            self.neuroml_file = neuroml_file
        else:
            self.neuroml_file = "some sane default"

    def create(self):
        """Create the model"""
        self.logger.info("Creating model")
        # create and add more methods here as required
        self.create_network()

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
            self.lems_file = "some sane default"

        quantities, sim = generate_lems_file_for_neuroml(
            sim_id="{{ cookiecutter.project_slug }}",
            neuroml_file=self.neuroml_file,
            target=self.network,
            duration="1500 ms",
            dt="0.01",
            lems_file="LEMS_{{ cookiecutter.project_slug }}.xml",
            target_dir=".",
        )

    def simulate(self):
        """Simulate the model"""
        write_neuroml2_file(self.newdoc, self.neuroml_file)


if __name__ == "__main__":
    model = {{ cookiecutter.project_slug_nospace }}()
    model.create()
    model.simulate()
