#!/usr/bin/env python3

__version__ = '1.4 2023-06-14'
__author__ = '${naam} ${achternaam} ${studnr}'

import os, sys
import getopt
import json
import base64
import textwrap
import traceback

from cryptography import exceptions
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import ciphers
from cryptography.hazmat.primitives.ciphers import algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sympadding
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.backends import default_backend

import pprint

def readMesg(fname: str) ->str:
    """ The message is a unicode-string """
    if fname:
        with open(fname, 'r') as fp:
            mesg = fp.read()
    else:
        mesg = input('Mesg? ')
    return mesg

def writeMesg(fname: str, mesg: str) -> None:
    """ The message is a unicode-string """
    if fname:
        with open(fname, 'w') as fp:
            fp.write(mesg)
    else:
        print(mesg)

class HvaCryptoMail:
    """ Class to encrypt/decrypt, hash/verifyHash and sign/verifySign messages.
        We this class to store all relevant parameters used in this process.
    """ 
    _mark = '--- HvA Crypto Mail ---'

    def __init__(self) -> None:
        """ Initilalise the used variables """
        self.version = '1.1'    # Version number
        self.modes   = []       # Specifies the used algorithms
        self.snds    = {}       # keys: names of senders, values: relevant data
        self.rcvs    = {}       # keys: names of receivers, values: relevant data
        self.sesIv   = None     # (optional) session Iv (bytes)
        self.sesKey  = None     # (optional) session key (bytes)
        self.prvs    = {}       # keys: names of user, values: prvKey-object
        self.pubs    = {}       # keys: names of user, values: pubKey-object
        self.code    = None     # (optional) the encrypted message  (bytes)
        self.mesg    = None     # (optional) the uncoded message    (bytes)
        self.dgst    = None     # (optional) the hash the message   (bytes)


    def dump(self, cmFname:str , vbs: bool=False) -> None:
        """ Export internal state to a guarded 'HvaCryptoMail'
            cmFname: string; Name of the file to save to.
        """
        print('version ->' ,self.version , ' modes -> ',self.modes , ' msg -> ',self.mesg
              ," code -> ",self.code )
        if gDbg: print(f"DEBUG: HvaCryptoMail:save cmFname={cmFname}")
        jdct = {}
        if self.version: jdct['vers'] = self.version
        if self.modes:   jdct['mods'] = self.modes
        if self.mesg:    jdct['mesg'] = self.mesg.decode('utf-8')
        if self.code:    jdct['code'] = self.code.hex()
        if self.dgst:    jdct['dgst'] = self.dgst.hex()
        if self.sesKey:  jdct['sKey'] = self.sesKey.hex()
        if self.sesIv:   jdct['sIv']  = self.sesIv.hex()
        if self.rcvs:    jdct['rcvs'] = { user: data.hex() \
                for user, data in self.rcvs.items() if data }
        if self.snds:    jdct['snds'] = { user: data.hex() \
                for user, data in self.snds.items() if data }
        if self.prvs: jdct['prvs'] = {
                name: str(prvKey.private_bytes(
                                               encoding=serialization.Encoding.PEM,
                                               format=serialization.PrivateFormat.TraditionalOpenSSL,
                                               encryption_algorithm=serialization.NoEncryption()),
                          encoding='ascii') \
                for name, prvKey in self.prvs.items() }
        if self.pubs:    jdct['pubs'] = {
                name: str(pubKey.public_bytes(
                                                    encoding=serialization.Encoding.PEM,
                                                    format=serialization.PublicFormat.SubjectPublicKeyInfo),
                          encoding='ascii')
                for name, pubKey in self.pubs.items() }
    


        if vbs: print(json.dumps(jdct, indent=4, sort_keys=True))
        payload = base64.b64encode(bytes(json.dumps(jdct), encoding='utf-8'))
        data = self._mark + '\n' + \
               '\n'.join(textwrap.wrap(str(payload, encoding='ascii'))) + '\n' + \
               self._mark + '\n'
        if cmFname:
            with open(cmFname, 'w') as fp:
                fp.write(data)
        return


    def load(self, cmFname:str, vbs:bool=False) -> None:
        """ Import internal state from a guarded 'HvaCryptoMail'
            cmFname: string; Name of the file to load from.
        """
        if gDbg: print(f"DEBUG: HvaCryptoMail:load cmFname={cmFname}")
        with open(cmFname, 'r') as fp:
            data = fp.read()
        data = data.strip()

        if not (data.startswith(self._mark) and data.endswith(self._mark)):
            raise Exception('Invalid HvaCryptoMail')

        payload = data[len(self._mark):-len(self._mark)]

        jdct = json.loads(base64.b64decode(payload))
        if vbs: print(json.dumps(jdct, indent=4, sort_keys=True))

        self.version = jdct.get('vers', '')
        self.modes   = jdct.get('mods', [])
        self.mesg    = jdct.get('mesg').encode('utf-8') if 'mesg' in jdct else None
        self.code    = bytes.fromhex(jdct['code']) if 'code' in jdct else None
        self.dgst    = bytes.fromhex(jdct['dgst']) if 'dgst' in jdct else None
        self.sesKey  = bytes.fromhex(jdct['sKey']) if 'sKey' in jdct else None
        self.sesIv   = bytes.fromhex(jdct['sIv'])  if 'sIv'  in jdct else None
        self.rcvs    = { user: bytes.fromhex(data)  \
                for user, data in jdct.get('rcvs', {}).items() }
        self.snds    = { user: bytes.fromhex(data)  \
                for user, data in jdct.get('snds', {}).items() }
        self.prvs    = { user: serialization.load_pem_private_key(data.encode('ascii'), password=None, backend=default_backend()) \
                for user, data in jdct.get('prvs', {}).items() }
        self.pubs    = { user: serialization.load_pem_public_key(data.encode('ascii'), backend=default_backend()) \
                for user, data in jdct.get('pubs', {}).items() }
        return

    def addMode(self, mode: str) -> None:
        """ Add the use mode to the mode-list
            Only one type crypted and Only one type of signed """
        if mode not in [
                'crypted:aes256-cfb:pkcs7:rsa-oaep-mgf1-sha256',
                'signed:rsa-pss-mgf1-sha384',
                'hashed:sha384' ]:
            # crypted:aes256-cfb:pkcs7:rsa-oaep-mgf1-sha256
            #   Message padded with pkcs7
            #   Message Encrypted with AES-128 met CFB
            #   Key protected with RSA with OAEP, MGF1 and SHA256
            # signed:rsa-pss-mgf1-sha384
            #   Message Signed with with RSA with PSS, MGF1 and SHA384
            # hashed:sha384
            #   Message Hash with SHA384
            # Andere modes hoeven niet geimplementeerd te worden.
            Exception('Unexptected mode:{}'.format(mode))
        if gDbg: print(f"DEDUG: HvaCryptoMail::addMode: mode={mode}, self.modes={self.modes}")
        self.modes.append(mode)


    def hasMode(self, mode: str) -> bool:
        """ Check whether a mode is supported this HvaCryptoMessage """
        for _mode in self.modes:
            if _mode.startswith(mode): return True
        return False


    def loadPrvKey(self, name: str) -> None:
        """ Load a Private key for user `name` """
        prvKey = self.prvs.get(name)

        fname = name+'.prv'
        # Load the prv-key from file `fname` into prvKey
        if prvKey is None and os.path.exists(fname):
            with open(fname, 'rb') as fp:
                data = fp.read()
                prvKey = serialization.load_pem_private_key(data, password=None, backend=default_backend())

        if prvKey is not None: self.prvs[name] = prvKey
        return


    def loadPubKey(self, name: str) -> None:
        """ Load a public key for user `name`,
            either from certificate-file or public key-file """
        pubKey = self.pubs.get(name)

        fname = name+'.crt'
        # Load the pub-key from certificate `fname` into pubKey
        if pubKey is None and os.path.exists(fname):
            data = open(fname, 'rb').read()
            crt = x509.load_pem_x509_certificate(data,
                    backend=default_backend())
            pubKey = crt.public_key()

        fname = name +'.pub'
        # Load the pub-key from public key-file `fname` into pubKey
        if pubKey is None and os.path.exists(fname):
            with open(fname, 'rb') as fp:
                data = fp.read()
                pubKey = serialization.load_pem_public_key(data, backend=default_backend())

        if pubKey: self.pubs[name] = pubKey
        return


    def genSesKey(self, n: int) -> None:
        """ Generate a (secure) session key for symmetric encryption. """
        # set self.sesKey with an usable key
        sesKey = b'' # Initialize variable
        sesKey = os.urandom(n)
        self.sesKey = sesKey
        return


    def genSesIv(self, n: int) -> None:
        """ Generate a (secure) intial-vector key for symmetric encryption. """
        # set self.sesIv with an usable intial vector
        sesIv = b'' # Initialize variable
        sesIv = os.urandom(n)
        self.sesIv = sesIv
        return


    def encryptSesKey(self, user: str) -> bool:
        """ Encrypt the session-key for `user` in `self.rcvs` """
        # Implememt encryption using RSA with OAEP, MGF1 and SHA256
        assert 'crypted:aes256-cfb:pkcs7:rsa-oaep-mgf1-sha256' in self.modes, \
                f"Unknown mode={self.modes}"

        encKey = None # Initialise variable
        cipher = ciphers(algorithms.AES(self.sesKey), modes.CFB(self.sesIv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(self.mesg) + encryptor.finalize()
        encKey = base64.b64encode(encrypted_data)
        if encKey: self.rcvs[user] = encKey
        return encKey is not None


    def decryptSesKey(self, user: str) -> bool:
        """ Decrypt the session-key saved in `self.rcvs` for `user` """
        # Implememt decryption using RSA with OAEP, MGF1 and SHA256
        assert 'crypted:aes256-cfb:pkcs7:rsa-oaep-mgf1-sha256' in self.modes, \
                f"Unknown mode={self.modes}"
        sesKey = None # Initialise variable
        cipher = ciphers(algorithms.AES(self.sesKey), modes.CFB(self.sesIv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(base64.b64decode(self.code)) + decryptor.finalize()
        sesKey = decrypted_data
        if sesKey: self.sesKey = sesKey
        return sesKey is not None


    def encryptMesg(self) -> bool:
        """ Encrypt the message (self.mesg) result in self.code"""
        assert 'crypted:aes256-cfb:pkcs7:rsa-oaep-mgf1-sha256' in self.modes, \
                f"Unknown mode={self.modes}"
        code = None # Initialize variable
        cipher = ciphers(algorithms.AES(self.sesKey), modes.CFB(self.sesIv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(self.mesg) + encryptor.finalize()
        code = base64.b64encode(encrypted_data)
        if code is not None: self.code = code
        return code is not None

    def decryptMesg(self) -> bool:
        """ Decrypt the message """
        assert 'crypted:aes256-cfb:pkcs7:rsa-oaep-mgf1-sha256' in self.modes, \
                f"Unknown mode={self.modes}"

        mesg = None # Initalise variable
        cipher = ciphers(algorithms.AES(self.sesKey), modes.CFB(self.sesIv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(base64.b64decode(self.code)) + decryptor.finalize()
        mesg = decrypted_data
        if mesg is not None: self.mesg = mesg
        return mesg is not None


    def signMesg(self, user: str) -> bool:
        """ Sign the message """
        # Implement signing using RSA with PSS, MGF1 and SHA384
        assert 'signed:rsa:pss-mgf1:sha384' in self.modes, \
                f"Unknown mode={self.modes}"
        signature = None # Initialize variable
        prvKey = self.prvs.get(user)

        if prvKey is not None:
            hasher = hashes.Hash(hashes.SHA384(), backend=default_backend())
            hasher.update(self.mesg)
            digest = hasher.finalize()
            signature = prvKey.sign(
                digest,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA384()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA384()
            )

            self.snds[user] = signature

        if signature: self.snds[user] = signature
        return signature is not None

    def verifyMesg(self, user: str) -> bool:
        """ Verify the message Return
            None is signature is incorrect, return True if correct """
        # Implement verification using RSA with PSS, MGF1 and SHA384
        assert 'signed:rsa:pss-mgf1:sha384' in self.modes, \
                f"Unknown mode={self.modes}"
        verified = None # Initialize variable
        pubKey = self.pubs.get(user)

        if pubKey is not None and user in self.snds:
            signature = self.snds[user]
            verifier = pubKey.verifier(
                signature,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA384()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA384()
            )
            verifier.update(self.mesg)
            try:
                verifier.verify()
                verified = True
            except:
                verified = False
 
        return verified

    def calcHash(self) -> None:
        """ Calculate the hash-digest of the message (`self.mesg`)
            Assign the digest to `self.dgst` """
        # Implememt hash using SHA384
        assert 'hashed:sha384' in self.modes, \
                f"Unknown mode={self.modes}"
        dgst = b''
        # Calculate hash (SHA384) of self.mesg
        hasher = hashes.Hash(hashes.SHA384(), backend=default_backend())
        hasher.update(self.mesg)
        dgst = hasher.finalize()

        self.dgst = dgst

    def chckHash(self) -> bool:
        """ Calculate the hash of the message (`self.mesg`)
            Check is is corresponds to `self.dgst` """
        # Implememt hash using SHA384
        assert 'hashed:sha384' in self.modes, \
                f"Unknown mode={self.modes}"
        res = None  # Initialized variable
        hasher = hashes.Hash(hashes.SHA384(), backend=default_backend())
        hasher.update(self.mesg)
        res = hasher.finalize()
        return res

# end of class HvaCryptoMail


def encode(cmFname: str, mesg: str, senders: list, receivers: list) -> tuple:
    """ Encode (encrypt and/or sign) the message (`mesg`)
        for the `receivers` and `senders`.
        The receivers and senders list containe names of users.
        The coded message-structur (CryptoMail) is written to the file `cmFname`
    """

# Implemented modes:
#   cm.addMode('hashed:sha384')
#   cm.addMode('crypted:aes256-cfb:pkcs7:rsa-oaep-mgf1-sha256')
#   cm.addMode('signed:rsa:pss-mgf1:sha384')

# Initialisation
    sendersState = {}
    receiversState = {}

    # Init cm
    cm = HvaCryptoMail()
    # Set cm.mesg
# Student work {{
# Student work }} Set

    # Calc Hash (don't forget addMode)
# Student work {{
# Student work }} Hash

    # Sign (don't forget addMode)
# Student work {{
# Student work }} Sign

    # Encrypt (don't forget addMode)
# Student work {{
# Student work }} Encrypt

    # Remove secrets
    # Secrets should not be a part of the saved CryptoMail structure
# Student work {{
# Student work }} Secrets


    # Save & Return
    cm.dump(cmFname)
    return receiversState, sendersState


def decode(cmFname: str, receivers: list=None, senders: list=None) -> tuple:
    """ Decode (decrypt and/or verify) found in de file named `cmFname`
        for the `receivers` en `senders`.
        The receivers and senders list containe names of users.
        Returns a tuple (msg, sendersState, receiversState).
    """

# Initialisation
    cm = HvaCryptoMail()
    cm.load(cmFname, gVbs)

    if receivers is None: receivers = cm.rcvs.keys()
    if senders is None: senders = cm.snds.keys()
    if gDbg: print(f"DEBUG: rcvs={receivers} snds={senders}")
    
    mesg = None
    sendersState = {}
    receiversState = {}
    hashState = None
    secretState = None

# Set secretState to True as no secrets are reveiled otherwise False
# Student work {{
# Student work }} CheckSecrets

    if cm.hasMode('crypted'):
        if gVbs: print('Verbose: crypted')
        # Decrypt the message for receivers or senders
        # and update sendersState of receiversState
# Student work {{
# Student work }} Decrypt

    if cm.hasMode('hashed'):
        if gVbs: print('Verbose: hashed')
# Student work {{
# Student work }} Hash

    if cm.hasMode('signed'):
        if gVbs: print('Verbose: signed')
        # Verify the message for receivers or senders
        # and update sendersState of receiversState
# Student work {{
# Student work }} Verify

# Convert bytes to str
    mesg = cm.mesg.decode('utf-8') if cm.mesg else None
    return mesg, receiversState, sendersState, hashState, secretState


def prState(state) -> str:
    return { None: 'no-info', True: 'success', False: 'failure' }.get(state, '???')

gVbs = False
gDbg = False
gSil = False

def main():
    global gVbs, gDbg, gSil
    autoLoad = True
    cmFname = ''
    mesgFname = ''
    receivers = None
    senders = None
    res = 0
    opts, args = getopt.getopt(sys.argv[1:], 'hVDSf:m:r:s:', [])
    for opt, arg in opts:
        if opt == '-h':
            print(f"Usage: {sys.argv[0]} -[HVDS] \\")
            print(f"\t\t[-f <cmFname>] \\   # {cmFname}")
            print(f"\t\t[-m <mesgFname>] \\ # {mesgFname}")
            print(f"\t\t[-r <receivers>] \\ # {receivers}")
            print(f"\t\t[-s <senders>] \\   # {senders}")
            print(f"\t\t encode|decode")
            sys.exit()
        if opt == '-V': gVbs = True
        if opt == '-D': gDbg = True
        if opt == '-S': gSil = True

        if opt == '-f': cmFname = arg
        if opt == '-m': mesgFname = arg
        if opt == '-r': receivers = arg.split(',') if arg else []
        if opt == '-s': senders = arg.split(',') if arg else []

    if gDbg: print(f"DEBUG: version={__version__}")

    if cmFname == '':
        print('Error: no <fname>.cm')
        sys.exit(2)

    cm = HvaCryptoMail()

    for cmd in args:

        if cmd == 'info':
            if autoLoad: cm.load(cmFname) 
            cm.dump(None, True)

        if cmd == 'encode':
            plainStr = readMesg(mesgFname)
            receiversState, sendersState = encode(cmFname, plainStr, senders, receivers)
            if True:
                sendersStr = ','.join([ name+'='+prState(state) for name, state in sendersState.items() ])
                receiversStr = ','.join([ name+'='+prState(state) for name, state in receiversState.items() ])
                print(f"Encoded:file:      {cmFname}")
                print(f"Encoded:receivers: {receiversStr}")
                print(f"Encoded:senders:   {sendersStr}")
                print(f"Encoded:mesg:      {plainStr}")
            else:
                print(f"Unable to encode {cmFname}")
                res = 1

        if cmd == 'decode':
            plainStr, receiversState, sendersState, hashState, secretState = \
                    decode(cmFname, receivers, senders)
            if plainStr:
                sendersStr = ','.join([ name+'='+prState(state) for name, state in sendersState.items() ])
                receiversStr = ','.join([ name+'='+prState(state) for name, state in receiversState.items() ])
                print(f"Decoded:file:      {cmFname}")
                print(f"Decoded:receivers: {receiversStr}")
                print(f"Decoded:senders:   {sendersStr}")
                print(f"Decoded:hash:      {prState(hashState)}")
                print(f"Decoded:secrets:   {prState(secretState)}")
                print(f"Decoded:mesg:      {plainStr}")
                if mesgFname: writeMesg(mesgFname, plainStr)
            else:
                print(f"Unable to decode {cmFname}")
                res = 1

    sys.exit(res)

if __name__ == '__main__':
    main()

# End of Program
