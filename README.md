# HermesLicense

Offline RSA-signed license system for on-prem deployments.

This repo contains:
- `generate_keys.py` — generate RSA keypair (run once on a secure machine)
- `make_license.py` — sign licenses using the private key (offline)
- `verifier.py` — license validator (de-obfuscated, intended to be compiled into a single executable)
- `machine_id.py` — machine id helpers (Linux-first fallbacks)
- `install.sh` & `hermes_verifier.service` — example installer + systemd unit
- `examples/` — sample license and packaging script

## Overview
1. Generate keypair on an offline/secure machine:
   ```bash
   pip install -r requirements.txt
   python generate_keys.py --bits 4096 --out-priv ./priv.pem --out-pub ./pub.pem
