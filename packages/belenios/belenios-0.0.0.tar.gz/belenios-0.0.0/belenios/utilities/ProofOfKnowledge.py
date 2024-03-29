from belenios.utilities.Utility import Utility


# https://gitlab.inria.fr/belenios/belenios/-/blob/master/src/lib/v1/trustees.ml
class ProofOfKnowledge:
    @staticmethod
    def Hpok(group, public_key, A):
        zkp = ("pok|" + str(group.description) + "|" + str(public_key) + "|" + str(A)).encode()
        res = int.from_bytes(Utility.hash_sha256_as_bytes(zkp), byteorder='big')
        return res

    @staticmethod
    def Hraweg(S0, election, answer, A):
        zkp = ("raweg|" + str(S0) + "|" + str(election.public_key) + "|" + str(answer.choices.alpha) + "|" + str(
            answer.choices.beta) + "|" + str(A)).encode()
        res = int.from_bytes(Utility.hash_sha256_as_bytes(zkp), byteorder='big')
        return res

    @staticmethod
    def Hsignature(H, A):
        zkp = ("sig|" + str(H) + "|" + str(A)).encode()
        res = int.from_bytes(Utility.hash_sha256_as_bytes(zkp), byteorder='big')
        return res

    @staticmethod
    def Hsignmsg(M, A):
        zkp = ("sigmsg|" + str(M) + "|" + str(A)).encode()
        res = int.from_bytes(Utility.hash_sha256_as_bytes(zkp), byteorder='big')
        return res

    @staticmethod
    def Hiprove(S, ciphertext, As, Bs):
        As_Bs_part = ""
        for A, B in zip(As, Bs):
            As_Bs_part += str(A) + ","
            As_Bs_part += str(B) + ","
        As_Bs_part = As_Bs_part[:-1]
        zkp = ("prove|" + str(S) + "|" + str(ciphertext.alpha) + "|" + str(
            ciphertext.beta) + "|" + As_Bs_part).encode()
        res = int.from_bytes(Utility.hash_sha256_as_bytes(zkp), byteorder='big')
        return res
