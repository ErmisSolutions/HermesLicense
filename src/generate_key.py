import argparse, os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def gen_keys(priv_path, pub_path, bits):

    os.makedirs(os.path.dirname(os.path.abspath(priv_path)), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(pub_path)), exist_ok=True)

    priv = rsa.generate_private_key(public_exponent=65537, key_size=bits)
    with open(priv_path, 'wb') as f:
        f.write(priv.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()))

    pub = priv.public_key()
    with open(pub_path, 'wb') as f:
        f.write(pub.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))

    os.chmod(priv_path, 0o600)
    print(f"Wrote Key Pair > {priv_path} | {pub_path}") 

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--out-priv', default='keys/priv.pem')
    p.add_argument('--out-pub', default='keys/pub.pem')
    p.add_argument('--bits', type=int, default=4096)

    args = p.parse_args()
    gen_keys(priv_path=args.out_priv, pub_path=args.out_pub, bits=args.bits)