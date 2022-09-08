import argparse
import pathlib
import json
from dhsecrets.dhsecrets import DHSecrets


def main():
    parser = argparse.ArgumentParser(description='Diffie-Hellman secrets.')
    parser.add_argument('-p', '--path', help='Key path',
                        type=pathlib.Path, default='.')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    list_parser = subparsers.add_parser('list')
    listsubparsers = list_parser.add_subparsers(dest='keytype')
    listsubparsers.required = True
    pub_list_parser = listsubparsers.add_parser('pub')
    priv_list_parser = listsubparsers.add_parser('priv')

    generate_parser = subparsers.add_parser('generate')
    generatesubparsers = generate_parser.add_subparsers(dest='keytype')
    generatesubparsers.required = True
    priv_generate_parser = generatesubparsers.add_parser('priv')
    priv_generate_parser.add_argument(
        '-e', '--encoding', help='Encoding of the privkey (HEX, BASE64)', default='HEX')
    priv_generate_parser.add_argument(
        '-n', '--name', help='Keyname', required=True)

    encode_parser = subparsers.add_parser('encode')
    encode_parser.add_argument(
        '--priv', help='Privkey', type=open, required=True)
    encode_parser.add_argument(
        '--pub', help='Pubkey', type=open, required=True)
    encode_parser.add_argument(
        '-P', '--payload', help='Payload', required=True)

    decode_parser = subparsers.add_parser('decode')
    decode_parser.add_argument(
        '--priv', help='Privkey', type=open, required=True)
    decode_parser.add_argument(
        '--pub', help='Pubkey', type=open, required=True)
    decode_parser.add_argument(
        '-F', '--filename', help='filename', type=open, required=True)

    args = parser.parse_args()

    # check encoding
    # check name not null

    if args.command == 'list':
        dhs = DHSecrets(args.path)
        if args.keytype == 'pub':
            pubs = dhs.list_pubs()
            print(json.dumps(pubs, indent=4))
        elif args.keytype == 'priv':
            privs = dhs.list_privs()
            print(json.dumps(privs, indent=4))

    elif args.command == 'generate':
        if args.keytype == 'priv':
            dhs = DHSecrets(args.path)
            filename = dhs.create_priv(args.name, encoding=args.encoding)
            print(f'Created {filename}.pub and {filename}.priv.')

    elif args.command == 'encode':
        dhs = DHSecrets(args.path)
        dhs_priv = DHSecrets(args.path)
        dhs_priv.import_priv(args.priv.name)
        dhs_pub = DHSecrets(args.path)
        dhs_pub.import_pub(args.pub.name)
        filename = dhs.encode(dhs_priv, dhs_pub, args.payload)
        print(f'Created {filename}.enc')

    elif args.command == 'decode':
        dhs = DHSecrets(args.path)
        dhs_priv = DHSecrets(args.path)
        dhs_priv.import_priv(args.priv.name)
        dhs_pub = DHSecrets(args.path)
        dhs_pub.import_pub(args.pub.name)
        message = dhs.decode(dhs_priv, dhs_pub, args.filename.name)
        print(message)
    else:
        exit(1)


if __name__ == "__main__":
    main()
