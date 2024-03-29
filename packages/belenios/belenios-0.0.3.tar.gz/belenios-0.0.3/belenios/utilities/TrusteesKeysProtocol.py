import json

from Crypto.Util.number import getRandomRange

from belenios.dataclass.dataclass import KeysPair
from belenios.models.belenios.CertKeysModel import CertKeysModel
from belenios.models.belenios.PolynomialModel import PolynomialModel
from belenios.models.belenios.ProofModel import ProofModel
from belenios.models.belenios.SignedStringModel import SignedStringModel
from belenios.models.belenios.TrusteePublicKeyModel import TrusteePublicKeyModel
from belenios.models.belenios.VInputModel import VInputModel
from belenios.models.belenios.VOutputModel import VOutputModel
from belenios.utilities.ProofOfKnowledge import ProofOfKnowledge
from belenios.utilities.Utility import Utility
from belenios.utilities.command_line.DbSession import DbSession


class TrusteesKeysProtocol:

    # https://www.belenios.org/specification.pdf#subsection.4.5
    def generate_single_trustee_key(self, election):
        keys_pair = Utility.gen_key_el_gamal(election.group)
        return TrusteesKeysProtocol().generate_trustee_public_key(election, keys_pair)

    def generate_trustee_public_key(self, election, keys_pair):
        # we generate A = g^w using a key pair, where private_key = A and public_key = w
        tmp = Utility.gen_key_el_gamal(election.group)
        w = tmp.private_key
        A = tmp.public_key

        challenge = ProofOfKnowledge.Hpok(election.group, keys_pair.public_key, A) % election.group.q
        response = (w - challenge * keys_pair.private_key)
        trusteePublicKeyModel = TrusteePublicKeyModel()
        trusteePublicKeyModel.public_key = keys_pair.public_key
        trusteePublicKeyModel.pok = ProofModel()
        trusteePublicKeyModel.pok.challenge = challenge
        trusteePublicKeyModel.pok.response = response
        return trusteePublicKeyModel, keys_pair

    # https://www.belenios.org/specification.pdf#subsection.4.5
    def check_proof_trustee_public_key(self, election, trusteePublicKeyModel):
        left = pow(election.group.g, trusteePublicKeyModel.pok.response, election.group.p)
        right = pow(trusteePublicKeyModel.public_key, trusteePublicKeyModel.pok.challenge, election.group.p)
        A = (left * right) % election.group.p
        challenge = ProofOfKnowledge.Hpok(election.group, trusteePublicKeyModel.public_key, A) % election.group.q
        return trusteePublicKeyModel.pok.challenge == challenge

    def derivate_private_seed(self, seed, group):
        sk = int.from_bytes(Utility.hash_sha256_as_bytes(("sk|" + seed).encode()), byteorder='big')
        dk = int.from_bytes(Utility.hash_sha256_as_bytes(("vk|" + seed).encode()), byteorder='big')
        vk = pow(group.g, sk, group.p)
        ek = pow(group.g, dk, group.p)
        return sk, dk, vk, ek

    # https://www.belenios.org/specification.pdf#subsection.4.6
    def generate_perdersen_trustee_keys(self, election):
        seed = Utility.generate_base58_string(22)
        signing_key, decryption_key, verification_key, encryption_key = self.derivate_private_seed(seed, election.group)

        cert_keys = CertKeysModel()
        cert_keys.verification = verification_key
        cert_keys.encryption = encryption_key

        signed_msg = Utility.generate_signed_msg(cert_keys, signing_key, election)
        return signed_msg, seed

    # https://www.belenios.org/specification.pdf#subsubsection.4.6.4
    def generate_perdersen_trustee_polynomial(self, election_bundle, threshold, seed, trustee_id):
        election = election_bundle.election
        signing_key, _, _, encryption_key = self.derivate_private_seed(seed, election.group)
        a_i = [getRandomRange(1, election.group.q - 2) for _ in range(threshold + 1)]
        a_i = [1,2]
        A_i = [pow(election.group.g, a_ij, election.group.p) for a_ij in a_i]
        pedersen_trustee = None
        for pedersen_trustee_iter in election_bundle.trustee_kinds:
            if pedersen_trustee_iter.trustee_kind_type == "PedersenTrusteeModel":
                pedersen_trustee = pedersen_trustee_iter
                break
        if pedersen_trustee is None:
            print("Invalid trustee id")
            return None
        s_ij = [Utility.evaluate_polynomial(a_i, j, election.group.q) for j in range(len(pedersen_trustee.certs) + 1)]
        print("a_i",   a_i)
        print("A_i", A_i)
        print("s_i", s_ij)
        polynomial = PolynomialModel()
        polynomial.trustee_id = trustee_id
        # check A_i or filled with ai0, . . . , ait
        polynomial.polynomial = Utility.generate_channel_msg(json.dumps(a_i), signing_key, encryption_key, election)
        # print("d", Utility.decrypt_channel_msg(polynomial.polynomial, verification_key, decryption_key, election))
        for j, cur_s_ij in enumerate(s_ij[1:]):
            # TODO handle random order adding
            ek_j = pedersen_trustee.certs[j].signed_object.encryption
            polynomial.secrets.append(Utility.generate_channel_msg(str(cur_s_ij), signing_key, ek_j, election))
        signed_string = SignedStringModel()
        signed_string.value = json.dumps(A_i)
        polynomial.coefexps = Utility.generate_signed_msg(signed_string, signing_key, election)

        election_bundle.polynomials.append(polynomial)
        DbSession().session.commit()
        return polynomial

    # https://www.belenios.org/specification.pdf#subsubsection.4.6.5
    def generate_perdersen_trustee_vinput(self, election_bundle, seed, trustee_id):
        election = election_bundle.election
        signing_key, _, _, encryption_key = self.derivate_private_seed(seed, election.group)

        polynomial = None
        for p in election_bundle.polynomials:
            if p.polynomial.recipient == encryption_key and p.trustee_id == trustee_id:
                polynomial = p

        if polynomial is None:
            print("Polynomial not found")
            return None
        v_input = VInputModel()
        v_input.polynomial = polynomial.polynomial
        for p_i in election_bundle.polynomials:
            v_input.secrets.append(p_i.secrets[trustee_id - 1])
            v_input.coefexps.append(p_i.coefexps)

            # for p in p_i.polynomials:
            #     # print(p.trustee_id, p.secrets)
            #     if p.trustee_id == trustee_id:
            #         pass
            #         break

        return v_input

    def check_perdersen_trustee_vinput(self, election_bundle, seed, trustee_id, v_input):
        election = election_bundle.election
        signing_key, decryption_key, verification_key, encryption_key = self.derivate_private_seed(seed, election.group)

        pedersen_trustee = None
        for pedersen_trustee_iter in election_bundle.trustee_kinds:
            if pedersen_trustee_iter.trustee_kind_type == "PedersenTrusteeModel":
                pedersen_trustee = pedersen_trustee_iter
                break
        if pedersen_trustee is None:
            print("Invalid trustee id")
            return False

        for i, coef in enumerate(v_input.coefexps):
            prod = 1
            A_i = json.loads(coef.signed_object.value)
            for k in range(pedersen_trustee.threshold):
                jk = pow(trustee_id, k)
                A_ik = A_i[k]
                # print(jk, A_ik)
                prod *= pow(A_ik, jk, election_bundle.election.group.p)
                prod = prod % election_bundle.election.group.p
            vk_j = pedersen_trustee.certs[i].signed_object.verification
            s_ij = int(Utility.decrypt_channel_msg(v_input.secrets[i], vk_j, decryption_key,
                                               election).signed_object.value)

            g_s_ij = pow(election_bundle.election.group.g, s_ij, election_bundle.election.group.p)
            # print(g_s_ij, prod)
            if g_s_ij != prod:
                print("Incorrect product", i, k, g_s_ij, prod)
                return False
        return True

    # https://www.belenios.org/specification.pdf#subsubsection.4.6.6
    def generate_perdersen_trustee_voutput(self, election_bundle, seed, trustee_id, v_input):
        election = election_bundle.election
        signing_key, decryption_key, verification_key, encryption_key = self.derivate_private_seed(seed, election.group)

        pedersen_trustee = None
        for pedersen_trustee_iter in election_bundle.trustee_kinds:
            if pedersen_trustee_iter.trustee_kind_type == "PedersenTrusteeModel":
                pedersen_trustee = pedersen_trustee_iter
                break
        if pedersen_trustee is None:
            print("Invalid trustee id")
            return None

        private_key = 0
        for i, s_i in enumerate(v_input.secrets):
            # check sign with verification key
            vk_i = pedersen_trustee.certs[i].signed_object.verification
            decrypted = Utility.decrypt_channel_msg(s_i, vk_i, decryption_key, election)
            # print("d", decrypted)
            # print("d", decrypted.signed_object.value)

            private_key += int(decrypted.signed_object.value)
            # private_key = private_key % election.group.q
        keys_pair = KeysPair(pow(election.group.g, private_key, election.group.p), private_key)
        v_output = VOutputModel()
        v_output.private_key = Utility.generate_channel_msg(str(private_key), signing_key, encryption_key,
                                                            election)
        v_output.trustee_public_key, _ = TrusteesKeysProtocol().generate_trustee_public_key(election, keys_pair)
        return v_output, private_key
    def compute_election_public_key(self,election_bundle):
        result = 1
        for trustee_kind in election_bundle.trustee_kinds:
            if trustee_kind.trustee_kind_type == "SingleTrusteeModel":
                result = (result * trustee_kind.trustee_public_key.public_key) % election_bundle.election.group.p
            else:
                for coefexps in trustee_kind.coefexps:
                    A_i = json.loads(coefexps.signed_object.value)
                    result = (result * A_i[0]) % election_bundle.election.group.p
        #           TODO: Check modulo
        return result
