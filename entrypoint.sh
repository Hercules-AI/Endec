#!/bin/bash

# exit immediately on failing commands
set -euo pipefail

alembic upgrade head

exec python -m app.main
