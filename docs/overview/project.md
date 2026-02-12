# Project Overview

InventoryK12 is a single-product monorepo focused initially on Texas school
districts, with a compliance model designed to expand to other states.

InventoryK12 add-ons and supporting services are intended to be housed within
the InventoryK12 monorepo and integrated through InventoryK12 APIs/events.

## Data and Environments

- Development uses a remote Postgres database for parity with production.
- Developers can run Postgres locally and connect via `host.docker.internal` from Docker.
