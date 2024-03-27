# Quick Start

The following blockchain explorers are supported in this plugin:

- [Base](https://base.blockscout.com/) for Base networks.
- [Ethereum](https://eth.blockscout.com/) for Ethereum networks.
- [Gnosis](https://gnosis.blockscout.com/) for Gnosis networks.
- [Optimism](https://optimism.blockscout.com/) for Optimism networks.
- [Polygon](https://polygon.blockscout.com/) for Polygon POS networks.

## Dependencies

- [python3](https://www.python.org/downloads) version 3.8 up to 3.11.

## Installation

### via `pip`

You can install the latest release via [`pip`](https://pypi.org/project/pip/):

```bash
pip install ape-blockscout
```

### via `setuptools`

You can clone the repository and use [`setuptools`](https://github.com/pypa/setuptools) for the most up-to-date version:

```bash
git clone https://github.com/ApeWorX/ape-blockscout.git
cd ape-blockscout
python3 setup.py install
```

## Quick Usage

## Set up the environment

Specify API keys as environment variables. You could put them in your shell's config like `~/.profile`
or use a tool like [direnv](https://direnv.net/) and store them locally in `.envrc`.

You can also specify multiple comma-separated keys, a random key will be chosen for each request.
This could be useful if you hit API rate limits.

You can obtain an API key by registering with Blockscout and visiting [this page](https://docs.blockscout.com/for-users/my-account/api-keys).

```bash
export BASE_BLOCKSCOUT_API_KEY=SAMPLE_KEY
export ETH_BLOCKSCOUT_API_KEY=SAMPLE_KEY
export GNOSIS_BLOCKSCOUT_API_KEY=SAMPLE_KEY
export OPTIMISM_BLOCKSCOUT_API_KEY=SAMPLE_KEY
export POLYGON_BLOCKSCOUT_API_KEY=SAMPLE_KEY
```

## Development

Please see the [contributing guide](CONTRIBUTING.md) to learn more how to contribute to this project.
Comments, questions, criticisms and pull requests are welcomed.
