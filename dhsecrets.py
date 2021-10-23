import os
import glob
import json
import datetime
import base64
import wallycore as wally

class DHSecrets:
    def __init__(self, path='.'):
        self.path = path
        self.name = None
        self.priv = None
        self.pub = None

    def list_pubs(self):
        files = glob.glob(os.path.join(self.path, '*.pub'))
        results = []
        for file in files:
            with open(file) as json_file:
                payload = json.load(json_file)
                results.append({'file': file, 'name': payload['name'], 'pub': payload['pub'], 'encodig': payload['encoding'], 'timestamp': payload['local_timestamp']})
        return results

    def import_pub(self, file):
        with open(os.path.join(self.path, file)) as json_file:
            payload = json.load(json_file)
            encoding = payload['encoding']
            if encoding == 'HEX':
                pubkey = wally.hex_to_bytes(payload['pub'])
            elif encoding == 'BASE64':
                pubkey = base64.b64decode(payload['pub']).decode()

            self.pub = bytearray(pubkey)
            self.name = payload['name']


    def list_privs(self):
        files = glob.glob(os.path.join(self.path, '*.priv'))
        results = []
        for file in files:
            with open(file) as json_file:
                payload = json.load(json_file)
                results.append({'file': file, 'name': payload['name'], 'pub': payload['pub'], 'encodig': payload['encoding'], 'timestamp': payload['local_timestamp']})
        return results

    def create_priv(self, name, encoding='HEX'):
        while True: # Iterate until valid
            try:
                priv = bytes(os.urandom(32))
                pub = wally.ec_public_key_from_private_key(priv)
                break
            except ValueError:
                pass
        # create file
        if encoding == 'HEX':
            enpriv = wally.hex_from_bytes(priv)
            enpub = wally.hex_from_bytes(pub)
        elif encoding == 'BASE64':
            enpriv = base64.b64encode(priv).decode()
            enpub = base64.b64encode(pub).decode()
        else:
            enpriv = ''
            enpub = ''
        self.priv = priv
        self.pub = bytearray(pub)
        self.name = name
        payload = {
            'pub': enpub,
            'name': name,
            'encoding': encoding,
            'local_timestamp': datetime.datetime.now().strftime("%A, %d %B %Y %I:%M%p"),
        }

        filename = name + '-' + wally.hex_from_bytes(pub[-2:])

        f = open(str(self.path) + '/' + filename + '.pub', "w")
        f.write(json.dumps(payload, indent=4, sort_keys=True))
        f.close()

        payload['priv'] = enpriv
        f = open(str(self.path) + '/' + filename + '.priv', "w")
        f.write(json.dumps(payload, indent=4, sort_keys=True))
        f.close()
        return filename


    def import_priv(self, file):
        with open(os.path.join(self.path, file)) as json_file:
            payload = json.load(json_file)
            encoding = payload['encoding']
            if encoding == 'HEX':
                privkey = wally.hex_to_bytes(payload['priv'])
                pubkey = wally.hex_to_bytes(payload['pub'])
            elif encoding == 'BASE64':
                privkey = base64.b64decode(payload['priv']).decode()
                pubkey = base64.b64decode(payload['pub']).decode()

            self.priv = bytearray(privkey)
            pub = wally.ec_public_key_from_private_key(privkey)
            assert pub == pubkey
            self.pub = bytearray(pubkey)
            self.name = payload['name']

    def encode(self, priv, pub, payload):
        secret = wally.ecdh(pub.pub, priv.priv)
        iv = bytes(wally.sha256(secret)[:wally.AES_BLOCK_LEN])
        wally_BITCOIN_MESSAGE_HASH_FLAG = 1
        formatted = wally.format_bitcoin_message(payload.encode('utf-8'), wally_BITCOIN_MESSAGE_HASH_FLAG)
        signature = wally.ec_sig_from_bytes(priv.priv, formatted, wally.EC_FLAG_ECDSA)
        signature = base64.b64encode(signature).decode('ascii')
        message = {
                    'from': wally.hex_from_bytes(priv.pub),
                    'to': wally.hex_from_bytes(pub.pub),
                    'type': 'string',
                    'payload': payload,
                    'payload_signature': signature,
                    'local_timestamp': datetime.datetime.now().strftime("%A, %d %B %Y %I:%M%p"),
                  }
        text = bytes(json.dumps(message).encode('utf-8'))
        encrypted = bytearray()
        written_e = wally.aes_cbc(secret, iv, text, wally.AES_FLAG_ENCRYPT, encrypted)
        encrypted = bytearray(written_e)
        written_e = wally.aes_cbc(secret, iv, text, wally.AES_FLAG_ENCRYPT, encrypted)

        s = wally.sha256(text)
        filename = f'{priv.name}-{pub.name}-{wally.hex_from_bytes(s)[:4]}'
        f = open(str(self.path) + '/' + filename + '.enc', "w")
        f.write(base64.b64encode(encrypted).decode())
        f.close()

        return filename

    def decode(self, priv, pub, filename):
        secret = wally.ecdh(pub.pub, priv.priv)
        iv = bytes(wally.sha256(secret)[:wally.AES_BLOCK_LEN])
        with open(os.path.join(self.path, filename)) as json_file:
            payload = json_file.read()
            encrypted = base64.b64decode(payload.encode('utf-8'))#.decode('utf-8')
            decrypted = bytearray()
            written_d = wally.aes_cbc(secret, iv, encrypted, wally.AES_FLAG_DECRYPT, decrypted)
            decrypted = bytearray(written_d)
            written_d = wally.aes_cbc(secret, iv, encrypted, wally.AES_FLAG_DECRYPT, decrypted)
            message = decrypted.decode()

            return message
