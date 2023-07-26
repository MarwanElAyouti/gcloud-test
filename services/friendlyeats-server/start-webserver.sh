#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

uvicorn friendlyeats.app:app --host 0.0.0.0 --port 80 --no-access-log --forwarded-allow-ips '*' --proxy-headers
