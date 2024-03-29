import ast

import base58
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Random import random
from Crypto.Util.number import inverse
from sqlalchemy.orm import joinedload

from belenios.dataclass.dataclass import KeysPair
from belenios.models.belenios.ChannelMsgModel import ChannelMsgModel
from belenios.models.belenios.EncryptedDataModel import EncryptedDataModel
from belenios.models.belenios.SignedStringModel import SignedStringModel


class Utility:
    # Generating large random numbers in [1, p]
    @staticmethod
    def generate_number_in_q(group):
        return random.randint(1, group.q)

    @staticmethod
    def gen_key_el_gamal(group):
        private_key = random.randint(1, group.q)
        public_key = pow(group.g, private_key, group.p)
        return KeysPair(public_key, private_key)
    @staticmethod
    def generate_base58_string(length):
        # Determine the minimum length required for 14 characters
        min_length = max(length, 14)

        # Generate random bytes
        random_bytes = get_random_bytes(min_length)

        # Encode random bytes to Base58
        base58_string = base58.b58encode(random_bytes)

        # If the length of the resulting Base58 string is less than 14, generate more random bytes and concatenate
        while len(base58_string) < 14:
            additional_bytes = get_random_bytes(min_length)
            base58_string += base58.b58encode(additional_bytes)

        # Truncate the string to the desired length
        return base58_string[:length].decode()
    @staticmethod
    def hash_sha256_as_bytes(data):
        """
        Compute the SHA-256 hash of the input data.

        Args:
            data (bytes): The input data to hash.

        Returns:
            bytes: The SHA-256 hash value.
        """
        hash_object = SHA256.new()
        hash_object.update(data)
        return hash_object.digest()

    @staticmethod
    def hash_sha256_as_hex(data):
        """
        Compute the SHA-256 hash of the input data.

        Args:
            data (bytes): The input data to hash.

        Returns:
            str(hex): The SHA-256 hash value.
        """
        hash_object = SHA256.new()
        hash_object.update(data)
        return hash_object.hexdigest()

    @staticmethod
    def derive_secret_exponent(prefix, salt_model, election):
        # Concatenate the uuid of the election and salt
        salt = election.uuid + salt_model.salt_value
        # Derive the secret exponent x using PBKDF2
        iterations = 100000
        key_length = 64  # 512 bits = 64 bytes
        x = PBKDF2(prefix.encode(), salt.encode(), dkLen=key_length, count=iterations, hmac_hash_module=SHA256)

        # Convert the derived key to an integer in big endian
        x_int = int.from_bytes(x, byteorder='big')

        # Reduce modulo p to form x
        x_mod_p = x_int % election.group.q

        return x_mod_p
    @staticmethod
    def send_mail(app, sender_email, receiver_email, message):
        print('Sending Email :\n\n\t Sender: %s\n\t Receiver: %s\n\t Message: %s\n' % (
        sender_email, receiver_email, message))

    @staticmethod
    def get_election_bundle_from_uuid(election_uuid):
        from belenios.models.belenios.ElectionBundleModel import ElectionBundleModel
        from belenios.models.belenios.ElectionModel import ElectionModel
        from belenios.utilities.command_line.DbSession import DbSession
        return DbSession().session.query(ElectionBundleModel) \
            .join(ElectionModel) \
            .filter(ElectionModel.uuid == election_uuid) \
            .options(joinedload(ElectionBundleModel.election)) \
            .first()

    @staticmethod
    def get_prefix_index_from_credential(private_credential):
        if len(private_credential) != 22:
            return None, None
        prefix = private_credential[:17].replace("-", "")  # XXX-XXXX-XXX-XXXX-NNNN
        index = private_credential[17:].replace("-", "")  # XXX-XXXX-XXX-XXXX-NNNN
        return prefix, int(index)

    @staticmethod
    def put_new_event(election_bundle):
        from belenios.models.belenios.EventModel import EventModel
        event = EventModel()
        # TODO: get last event
        event.height = 0

        election_bundle.events.append(event)
        return event

    @staticmethod
    def generate_signed_msg(signed_object, sk, election):
        from belenios.utilities.ProofOfKnowledge import ProofOfKnowledge
        from belenios.models.belenios.ProofModel import ProofModel
        from belenios.models.belenios.SignedMsgModel import SignedMsgModel
        signed_msg = SignedMsgModel()
        signed_msg.signed_object = signed_object

        # we generate A = g^w using a key pair, where private_key = A and public_key = w
        tmp = Utility.gen_key_el_gamal(election.group)
        w = tmp.private_key
        A = tmp.public_key

        challenge = ProofOfKnowledge.Hsignmsg(str(signed_object), A) % election.group.q
        response = (w - challenge * sk)
        signed_msg.signature = ProofModel()
        signed_msg.signature.challenge = challenge
        signed_msg.signature.response = response
        return signed_msg

    @staticmethod
    def check_signed_msg(signed_msg, vk, election):
        from belenios.utilities.ProofOfKnowledge import ProofOfKnowledge
        left = pow(election.group.g, signed_msg.signature.response, election.group.p)
        right = pow(vk, signed_msg.signature.challenge, election.group.p)
        A = (left * right) % election.group.p
        challenge = ProofOfKnowledge.Hsignmsg(str(signed_msg.signed_object), A) % election.group.q
        return signed_msg.signature.challenge == challenge

    @staticmethod
    def aes_ccm_encrypt(plaintext, key, iv):
        cipher = AES.new(key, AES.MODE_CCM, nonce=iv)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        return ciphertext, tag

    @staticmethod
    def aes_ccm_decrypt(ciphertext, tag, key, iv):
        cipher = AES.new(key, AES.MODE_CCM, nonce=iv)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext

    @staticmethod
    def generate_encrypted_msg(plaintext, ek, election):
        from belenios.models.belenios.EncryptedMsgModel import EncryptedMsgModel
        encrypted_msg = EncryptedMsgModel()
        # TODO: use ElGamal() if possible
        # we generate g^r using a key pair, where private_key = r and public_key = alpha
        tmp = Utility.gen_key_el_gamal(election.group)
        r = tmp.private_key
        encrypted_msg.alpha = tmp.public_key

        # we generate g^s using a key pair, where private_key = s and public_key = teta
        tmp = Utility.gen_key_el_gamal(election.group)
        s = tmp.private_key
        teta = tmp.public_key

        encrypted_msg.beta = pow(ek, r, election.group.p) * teta

        key = SHA256.new(("key|" + str(teta)).encode()).digest()
        # print("teta", teta)
        # print("ek", ek)
        # print("key", key)
        iv = SHA256.new(("iv|" + str(encrypted_msg.alpha)).encode()).digest() [:13]
        ciphertext, tag = Utility.aes_ccm_encrypt(plaintext, key, iv)
        # print("fir", Utility.aes_ccm_decrypt(ciphertext,
        #                         tag, key, iv))
        # print("Ciphertext:", ciphertext.hex(), ciphertext == bytes.fromhex(ciphertext.hex()))
        # print("Tag:", tag.hex())

        encrypted_msg.data = EncryptedDataModel()
        encrypted_msg.data.ciphertext = ciphertext.hex()
        encrypted_msg.data.tag = tag.hex()
        encrypted_msg.data.iv = iv.hex()

        return encrypted_msg

    @staticmethod
    def decrypt_encrypted_msg(encrypted_msg, dk, election):
        teta = (encrypted_msg.beta * inverse(pow(encrypted_msg.alpha, dk, election.group.p),
                                             election.group.p)) % election.group.p
        # print("teta", teta)
        key = SHA256.new(("key|" + str(teta)).encode()).digest()
        # print("dk", dk)
        # print("key", key)
        iv = SHA256.new(("iv|" + str(encrypted_msg.alpha)).encode()).digest()[:13]
        if bytes.fromhex(encrypted_msg.data.iv) != iv:
            print("Invalid IV")
            return None
        # print("Ciphertext:", encrypted_msg.data.ciphertext)

        plaintext = Utility.aes_ccm_decrypt(bytes.fromhex(encrypted_msg.data.ciphertext),
                                            bytes.fromhex(encrypted_msg.data.tag), key, iv)
        # print("plaintext:", plaintext)
        return plaintext

    @staticmethod
    def generate_channel_msg(plaintext, sk, ek, election):
        channel_msg = ChannelMsgModel()
        channel_msg.recipient = ek
        signed_string = SignedStringModel()
        signed_string.value = plaintext
        sign = str(Utility.generate_signed_msg(signed_string, sk, election).to_dict()).encode()
        channel_msg.message = Utility.generate_encrypted_msg(sign, ek, election)
        return channel_msg

    @staticmethod
    def decrypt_channel_msg(channel_msg, vk, dk, election):
        from belenios.models.belenios.SignedMsgModel import SignedMsgModel

        decrypted = Utility.decrypt_encrypted_msg(channel_msg.message, dk, election)
        # print("decrypted", decrypted)
        # Convert byte string to string
        byte_string_decoded = decrypted.decode()

        # Use ast.literal_eval() to convert string to dictionary
        result_dict = ast.literal_eval(byte_string_decoded)
        signed_msg = SignedMsgModel.load_from_json(result_dict)
        # print("decrypted fe",result_dict)
        # print("decrypted", signed_msg)
        if not Utility.check_signed_msg(signed_msg, vk, election):
            print("invalid signature")
            return None
        return signed_msg
        #
        # channel_msg = ChannelMsgModel()
        # channel_msg.recipient = ek
        # signed_string = SignedStringModel()
        # signed_string.value = plaintext
        # sign = str(Utility.generate_signed_msg(signed_string, sk, election).to_json()).encode()
        # channel_msg.message = Utility.generate_encrypted_msg(sign, ek, election)
        # return channel_msg



    @staticmethod
    def get_trustee_kind_from_id(id, election_bundle):
        for trustee_kind in election_bundle.trustee_kinds:
            if trustee_kind.trustee_kind_type == "SingleTrusteeModel":
                if trustee_kind.trustee_id == id:
                    return trustee_kind
            else:
                for trustee_id in trustee_kind.trustee_ids:
                    if trustee_id == id:
                        return trustee_kind
        return None

    @staticmethod
    def evaluate_polynomial(a, x, modulus):
        result = 0
        for i, coef in enumerate(a):
            result += coef * pow(x, i)
        return result % modulus
