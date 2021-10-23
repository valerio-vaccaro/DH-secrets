import pytest
import os
import json
import glob
from dhsecrets import DHSecrets


class TestDHSecrets:

    def test(self):
        files = glob.glob(os.path.join('./test','*'))
        for file in files:
            os.remove(file)

        dhs1 = DHSecrets('./test')
        name1 = dhs1.create_priv('pluto')

        dhs1b = DHSecrets('./test')
        dhs1b.import_priv(name1+'.priv')

        assert (dhs1.priv, dhs1.pub) == (dhs1b.priv, dhs1b.pub)

        dhs2 = DHSecrets('./test')
        name2 = dhs2.create_priv('pippo', encoding='BASE64')

        print('Files:')

        dhs3 = DHSecrets('./test')
        pubs = dhs3.list_pubs()
        print(json.dumps(pubs, indent=4))

        privs = dhs3.list_privs()
        print(json.dumps(privs, indent=4))

        filename = dhs3.encode(dhs1, dhs2, 'pippo')
        print(filename)


        message = dhs3.decode(dhs2, dhs1, filename+'.enc')
        print(message)

        assert False == True
