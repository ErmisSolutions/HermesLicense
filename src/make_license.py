"""
Create RSA-signed license JSON using priv.pem (offline).
License format:
{
  "id": "CLIENT-001",
  "exp": 1710000000,
  "meta": "Acme Inc
  "machine_id": "host-hash-if-used",
  "sig": "base64-signature"
}
"""

import json, argparse, time, base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def canonical_json(payload):
    return json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')

def sign_payload(priv_pem, payload) -> str:
    with open(priv_pem, 'rb') as f:
        priv = serialization.load_pem_private_key(f.read(), password=None)
    data = canonical_json(payload)
    sig = priv.sign(data, padding.PKCS1v15(), hashes.SHA256())
    return base64.b64encode(sig).decode('ascii')

def make_lic(out_path, priv_pem, id=None, days=365, meta=None, machine_id=None):
    payload = {}

    if id is not None:
        payload['id'] = str(id)

    if days > 0:
        payload['exp'] = int(time.time() + int(days) * 24 * 3600)
    else:
        payload['exp'] = None

    if meta is not None:
        payload['meta'] = str(meta)

    if machine_id is not None:
        payload['machine_id'] = str(machine_id)
    sig = sign_payload(priv_pem, payload)

    payload['sig'] = sig

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
    
    print(f"Wrote license -> {out_path}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Create a RSA Signed License")
    p.add_argument('out', help="output License JSON Path")
    p.add_argument('--priv', default='priv.pem', help='private key path')
    p.add_argument('--id', help='license id')
    p.add_argument('--days', type=int, default=365, help='Valid for N Days')
    p.add_argument('--meta', help='metadata string (client name)')
    p.add_argument('--machine-id', help='Optional machine binding value')

    args = p.parse_args()
    
    make_lic(args.out, args.priv, args.id, args.days, args.meta, args.machine_id)