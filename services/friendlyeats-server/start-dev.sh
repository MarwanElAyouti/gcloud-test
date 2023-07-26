#!/bin/bash

uvicorn friendlyeats.app:app --host 0.0.0.0 --port 80 --reload --log-level debug