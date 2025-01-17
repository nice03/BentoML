#!/usr/bin/env bash

GIT_ROOT=$(git rev-parse --show-toplevel)

cd "$GIT_ROOT" || exit 1

source ./scripts/ci/helpers.sh

INFO "(pylint) Linting bentoml..."

pylint --rcfile="./pyproject.toml" bentoml

INFO "(pylint) Linting tests and docker..."

pylint --rcfile="./pyproject.toml" --disable=E0401,F0010 tests docker
