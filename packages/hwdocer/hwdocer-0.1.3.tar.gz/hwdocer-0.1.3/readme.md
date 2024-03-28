# HWDOCER

The [HardWare DOCumentation buildER][home_link] is a utility that help generating graphical documentations using [drawio][drawio_link] and [wireviz][wireviz_link]

## Install

### Via PyPI

> TODO

### As a Git submodule

1. Add the submodule  
   simply open a **terminal** in the host repo and execute this:

   ```bash
   git submodule add https://gitlab.com/real-ee/public/hwdocer.git dep/hwdocer
   ```

2. Venv install
   Then you need to [install](https://laurencedv.org/computing/python) the venv, by having [poetry][poetry_link] and [pyenv][pyenv_link].  
   Open a **terminal** then execute this:

   ```bash
   poetry install
   ```

## Usage

Typically you should add the git repo as a git module so you have a copy locally in your project then simply run it on your doc folder

```bash
poetry run python -m hwdocer -vvvv -i "./doc" -o "./doc/build"
```

> NOTE: Currently all `*.yml` file in the _input search_ will match for **harness** drawing and all `*.drawio` files will match for **diagram** drawing

### Drawio

To create diagram and drawing that will be then automatically drawn by this tool, you need to install [drawio][drawio_link] local executable by downloading the installer for your OS (only linux tested)

### Wireviz

To create wire harness, install [wireviz][wireviz_link], which is a project based on [graphviz][graphviz_link] but aimed to specifically draw wire harnesses.

## Contrib

See the [contribution guideline][contrib_file]

## Changelog

See the [release][release_file] file and [roadmap file][roadmap_file]

## License

This software is released under [GPL3][license_file]

<!-- links -->

[home_link]: https://gitlab.com/realee-laurencedv/hwdocbuilder
[poetry_link]: https://python-poetry.org/docs/
[pyenv_link]: https://github.com/pyenv/pyenv
[drawio_link]: https://github.com/jgraph/drawio-desktop/releases/
[wireviz_link]: https://github.com/wireviz/WireViz
[graphviz_link]: https://graphviz.org/

<!-- files -->

[release_file]: doc/release.md
[roadmap_file]: doc/roadmap.md
[contrib_file]: doc/contrib.md
[license_file]: license
