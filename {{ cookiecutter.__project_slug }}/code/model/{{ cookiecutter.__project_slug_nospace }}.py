#!/usr/bin/env python3
"""
{{ cookiecutter.short_description }}

Copyright {% now 'local', '%Y' %} {{ cookiecutter.author_name }}
Author: {{ cookiecutter.author_name }}<{{ cookiecutter.author_email }}>
"""


import typing
import logging
import neuroml
import typer
from datetime import datetime
from neuroml.utils import component_factory
from pyneuroml.io import write_neuroml2_file
from pyneuroml.lems import generate_lems_file_for_neuroml
from pyneuroml.runners import run_lems_with
from pyneuroml.annotations import create_annotation


class {{ cookiecutter.__project_slug_nospace }}(object):

    """{{ cookiecutter.project_name }} model in NeuroML"""
    network_name = "{{ cookiecutter.__project_slug }}"
    nml_document = component_factory(neuroml.NeuroMLDocument, id=network_name)

    # https://docs.neuroml.org/Userdocs/Provenance.html
    # https://pyneuroml.readthedocs.io/en/development/pyneuroml.annotations.html#pyneuroml.annotations.create_annotation
    annotation = create_annotation(
        subject="{{ cookiecutter.__project_slug }}",
        abstract="{{ cookiecutter.short_description }}",
        title="{{ cookiecutter.project_name }}",
        annotation_style="miriam",
        xml_header=False,
        keywords=["keyword 1", "keyword 2"],
        creation_date="{% now 'local', '%Y-%m-%d' %}",
        authors={
            "{{ cookiecutter.author_name }}": {
                "{{ cookiecutter.author_email }}": "email",
                "https://orcid.org/###": "orcid"
            }
        },
        contributors={
            "A contributor": {
                "email@address.com": "email",
            }
        },
        sources={"https://github.com/<username>/<project>": "GitHub"},
        citations={"https://doi.org/...": "{{ cookiecutter.author_name }} et al"},
        references={"https://doi.org/...": "{{ cookiecutter.author_name }} et al"}
    )
    nml_document.annotation = neuroml.Annotation([annotation])
    network = nml_document.add(neuroml.Network, id="{{ cookiecutter.__project_slug }}", validate=False)

    def __init__(self):
        """Initialise the model from a parameter file."""

        # set up cli
        self.app = typer.Typer(help="{{ cookiecutter.project_name }} model in NeuroML")
        self.app.command()(self.create_model)
        self.app.command()(self.create_simulation)
        self.app.command()(self.create_model_simulation)
        self.app.command()(self.simulate)
        self.app.callback()(self.configure)
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    def configure(
        self,
        code_config_file: str = "parameters/general.json",
        model_parameters_file: str = "parameters/model.json",
        neuroml_file: typing.Optional[str] = None,
        seed: typing.Optional[int] = None,
        label: typing.Optional[str] = None,
        model_variant: typing.Optional[str] = None,
        lems_file: typing.Optional[str] = None,
        logging_level: typing.Optional[str] = None,

    ):
        """Configure model

        :param neuroml_file: name of NeuroML file to serialise model to
        :type neuroml_file: str
        :param seed: model/simulation seed
        :type seed: str
        :param lems_file: name of LEMS simulation file
        :type lems_file: str

        """
        self.code_config_file = code_config_file
        self.model_parameters_file = model_parameters_file
        with open(self.code_config_file) as f:
            self.general_params = json.load(f)

        if seed:
            self.seed = seed
        else:
            self.seed = self.general_params.get("seed", "1234")

        if label:
            provided_label = label
        else:
            provided_label = self.general_params.get("label")
        self.label = f"_{provided_label.replace(' ', '_')}" if provided_label else ""

        if model_variant:
            provided_model_variant = model_variant
        else:
            provided_model_variant = self.model_params.get("label")
        self.model_variant = (
            f"{provided_model_variant.replace(' ', '_')}"
            if provided_model_variant
            else ""
        )

        if neuroml_file:
            self.neuroml_file = neuroml.file
        else:
            self.neuroml_file = self.general_params.get(
                "neuroml_file",
                f"{self.network_name}{self.label}_{self.model_variant}_{self.seed}_{self.timestamp}.net.nml",
            )

        if lems_file:
            self.lems_file = lems_file
        else:
            self.lems_file = self.general_params.get(
                "lems_file",
                f"LEMS_{self.network_name}{self.label}_{self.model_variant}_{self.seed}_{self.timestamp}.xml",
            )

        if logging_level:
            self.logging_level = logging_level
        else:
            self.logging_level = self.general_params.get(
                "logging_level",
                "DEBUG",
            )

        # set up a logger
        self.logger = logging.getLogger(self.network_name)
        self.logger.setLevel(getattr(logging, self.logging_level))
        ch = logging.StreamHandler()
        ch.setLevel(getattr(logging, self.logging_level))
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.propagate = False

    def create_model(self):
        """Create the model"""
        self.logger.info("Creating model")

        # load model parameters
        with open(self.model_parameters_file) as f:
            self.model_params = json.load(f)

        # create and add more methods here as required
        self.__create_network()

        # write model to file
        write_neuroml2_file(self.nml_document, self.neuroml_file)

    def __create_network(self):
        """Create network"""
        # details of creating the network and populations

    def create_simulation(self, lems_file: typing.Optional[str] = None,
                          model_file: typing.Optional[str] = None):
        """Create simulation

        :param lems_file: name of LEMS file to serialise simulation to
        :type lems_file: str
        """
        if lems_file:
            self.logger.info(f"LEMS file name provided. Using it: {lems_file}")
            self.lems_file = lems_file
        else:
            # if not already set, use a default
            if not hasattr(self, "lems_file"):
                self.logger.error(
                    "No file name set for lems_file before, please pass a value"
                )
                return

        if model_file:
            self.logger.info(f"Model file name provided. Using it: {model_file}")
            self.neuroml_file = model_file
            self.timestamp = model_file.split(".")[0].split("_")[-1]
            self.lems_file = f"LEMS_{self.network_name}{self.label}_{self.model_variant}_{self.seed}_{self.timestamp}.xml"

        self.logger.info(f"Saving LEMS simulation file {self.lems_file}")
        quantities, sim = generate_lems_file_for_neuroml(
            sim_id=f"{{ cookiecutter.__project_slug }}_{self.timestamp}",
            neuroml_file=self.neuroml_file,
            target=self.network.id,
            duration="1500 ms",
            dt="0.01",
            lems_file_name=self.lems_file,
            target_dir=".",
            gen_plots_for_all_v=True,
            gen_saves_for_all_v=True,
            simulation_seed=self.seed,
        )

        validate_neuroml2_lems_file(self.lems_file)

    def create_model_simulation(self):
        """Create both the model and simulation

        Note, that this does not accept any parameters. So, it respects the
        default parameters only.

        """
        self.create_model()
        self.create_simulation()

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

        {%- endif %}


if __name__ == "__main__":
    model = {{ cookiecutter.__project_slug_nospace }}()
    model.app()
