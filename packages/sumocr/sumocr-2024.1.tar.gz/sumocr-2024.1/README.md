# SUMO - CommonRoad Interface

This package implements the interface between the framework for motion planning of automated vehicles [commonroad-io](https://pypi.org/project/commonroad-io/)
and the traffic simulator [SUMO](https://sumo.dlr.de).
The interface is presented in detail in our [paper](https://mediatum.ub.tum.de/doc/1486856/344641.pdf) [1].

## Documentation

Please refer to the [documentation](https://cps.pages.gitlab.lrz.de/sumo-interface/) and [tutorials](https://commonroad.in.tum.de/tools/sumo-interface).
To run interactive scenarios, denoted by the suffix ```I```, from the CommonRoad database,
please use the script from the corresponding repository [gitlab.lrz.de/tum-cps/commonroad-interactive-scenarios](https://gitlab.lrz.de/tum-cps/commonroad-interactive-scenarios).


[1] _Moritz Klischat, Octav Dragoi, Mostafa Eissa, and Matthias Althoff, Coupling SUMO with a Motion Planning Framework for Automated Vehicles, SUMO 2019: Simulating Connected Urban Mobility_

## Development

### Dependencies

You can easily install all dependencies with poetry:

```sh
$ poetry install --with tests --with dev
```

### Tests

To run the tests you can use:

```sh
$ export SUMO_HOME=$(whereis sumo)
$ poetry run pytest tests/ --ignore=./tests/sumocr/sumo_docker
```

### pre-commit

pre-commit is used to run a variety of checks on the code (e.g. formatting with `black`).
You can install the hooks with:

```sh
$ pre-commit install
```

Those hooks will be run everytime you run `git commit`.

### Documentation

The documentation is built with sphinx. Before building make sure to install the required dependencies:

```sh
$ poetry install --with docs
```

Than you can build the documentation with:

```sh
$ cd docs/source
$ poetry run sphinx-build -b html . ../../public
```

After the built finished successfully you can view in you browser by opening `public/index.html` from the root of the project.
If you perfomed API changes, you might need to recreate the API doc:

```sh
$ cd docs
$ poetry run sphinx-apidoc -o ./source/api ../sumocr
```
