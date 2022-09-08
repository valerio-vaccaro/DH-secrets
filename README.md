# DH-secrets
Diffie-Hellman based secret secure exchange.

## Installation
Install lib and cli using the following command.

```
$ pip install dhsecrets
```

##  Usage
The package will install a shell utility called `dhs-cli`

```
$ dhs-cli -h

usage: dhs-cli [-h] [-p PATH] {list,generate,encode,decode} ...

Diffie-Hellman secrets.

positional arguments:
  {list,generate,encode,decode}

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Key path
```

### Create keys 
We are Alice and we want share a secret with Bob, first step is create a key pair and share the public key with Bob.

```
$ dhs-cli generate priv -n alice

Created alice-3cf5.pub and alice-3cf5.priv
```

Bob on his side do the following.

```
$ dhs-cli generate priv -n bob

Created bob-d740.pub and bob-d740.priv.
```

### List keys
After Alice copy the Bob Public Keyon the key folder she can list the known keys.

```
$ dhs-cli list priv

[
    {
        "file": "./alice-3cf5.priv",
        "name": "alice",
        "pub": "0319c6697fb8e0d65f0f4d4e93a7fe52ce41e51dfb340a8a2207830158f85e3cf5",
        "encodig": "HEX",
        "timestamp": "Thursday, 08 September 2022 10:43AM"
    }
]
```

Alice known only 1 private key and 2 publik keys, she can check using the following command.

```
$ dhs-cli list pub

[
    {
        "file": "./bob-d740.pub",
        "name": "bob",
        "pub": "031bf3ecc3458bec4f34f8d47d2db8d46d7679562e3efa5d71edd10d8f35ccd740",
        "encodig": "HEX",
        "timestamp": "Thursday, 08 September 2022 10:43AM"
    },
    {
        "file": "./alice-3cf5.pub",
        "name": "alice",
        "pub": "0319c6697fb8e0d65f0f4d4e93a7fe52ce41e51dfb340a8a2207830158f85e3cf5",
        "encodig": "HEX",
        "timestamp": "Thursday, 08 September 2022 10:43AM"
    }
]

```

### Encode
Alice can  encode the string message using the encode command.

```
$ dhs-cli encode --priv alice-3cf5.priv --pub bob-d740.pub -P "supersecret"

Created alice-bob-d60c.enc


$ cat alice-bob-d60c.enc

E7irYBYdMxBOZGtu221RZSJc3VSQ8yAVt33NmH2eW959Y6lYyMJoCTAG7Q3kxHLBhbIhGYUPLzraUDwvZeHyaDLQHqnq/7K2XNMvtGOy7wWVtlRuYIBGdNXNslGvugke/kr71xkWEfjgG7sUDYyYXJqxUa2Ol24KPoxPDr+5jJYrzSCzGgRZYhEo/2/rsrANBHN5Z698w/bVB4eC8+KyzIJ51A2HaDz0CCHi73bCsJv6sJPLf6U2HYHdK/xig1XADQYb7eWAVv4C51mTi1iv9LqGKoLgMnUD7GEzXVgbCmhol9CG3ZnsDrrLZy/ntEOj9Q+qMhPdhPzKCoxmJkQf+6xLLRSEmkTi7fg4XlKIoERh4IgJ+blZ3MOngmHz/cJs97WlKnTlK4djr3EHdA2N0WO+YVvJ/lXpXCe1dE1RIJrUc04oJtasXMjlZIB8wDXYIBKzAbR8+khgw9/Oapm/BZBBmHpM36yIGgz0zmmnCybYJOagXT93LkatOWK/olqc

```

### Decode
Bob can decode the message using the decode command.

```
$ dhs-cli decode --priv bob-d740.priv --pub alice-3cf5.pub -F alice-bob-d60c.enc | jq

{
  "from": "0319c6697fb8e0d65f0f4d4e93a7fe52ce41e51dfb340a8a2207830158f85e3cf5",
  "to": "031bf3ecc3458bec4f34f8d47d2db8d46d7679562e3efa5d71edd10d8f35ccd740",
  "type": "string",
  "payload": "supersecret",
  "payload_signature": "maYEEc7yhP/iP/8ZtoiuomVtLtXp2FHfrJz0IZvCpR5NDOUpCpBG4WbU3LWGk6Lf0e/ORhNFBXFhXCXyzUw84w==",
  "local_timestamp": "Thursday, 08 September 2022 01:23PM"
}
```