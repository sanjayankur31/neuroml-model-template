# NeuroML model template

[![GitHub CI](https://github.com/sanjayankur31/neuroml-model-template/actions/workflows/ci.yml/badge.svg)](https://github.com/sanjayankur31/neuroml-model-template/actions/workflows/ci.yml)
[![GitHub](https://img.shields.io/github/license/sanjayankur31/neuroml-model-template)](https://github.com/sanjayankur31/neuroml-model-template/blob/master/LICENSE.lesser)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/sanjayankur31/neuroml-model-template)](https://github.com/sanjayankur31/neuroml-model-template/pulls)
[![GitHub issues](https://img.shields.io/github/issues/sanjayankur31/neuroml-model-template)](https://github.com/sanjayankur31/neuroml-model-template/issues)
[![GitHub Org's stars](https://img.shields.io/github/stars/NeuroML?style=social)](https://github.com/NeuroML)
[![Twitter Follow](https://img.shields.io/twitter/follow/NeuroML?style=social)](https://twitter.com/NeuroML)
[![Gitter](https://badges.gitter.im/NeuroML/community.svg)](https://gitter.im/NeuroML/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

[Cookiecutter](https://cookiecutter.readthedocs.io/en/stable/) template repository for NeuroML modelling projects.

https://docs.neuroml.org

This interactively creates a new NeuroML model project that:

- creates a directory structure
- adds a license
- adds basic [OMV](https://github.com/OpenSourceBrain/osb-model-validation) tests and sets up GitHub Actions
- adds a simple starter python project for building a NeuroML model and simulation
- sets up requirements.txt files to support different simulation backends
- initialises Git (optional)
- initialises Git-annex for data (optional)

## Usage

You can use cookiecutter to directly pull this template from GitHub:

```
$ cookiecutter gh:sanjayankur31/neuroml-model-template
```

You can also download it and run cookiecutter.
More information on cookiecutter is in its documentation [here](https://cookiecutter.readthedocs.io/en/stable/usage.html).
