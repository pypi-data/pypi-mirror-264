from Crypto.Util.number import inverse, bytes_to_long, long_to_bytes

from belenios.config.config import AppConfig
from belenios.dataclass.dataclass import KeysPair, EncryptedText, EncryptedTextAndK
from belenios.utilities.Utility import Utility


class ElGamal:
    def discrete_logarithm(self, g_pow_v, g, q, max_dlp=None):
        if q.bit_length() > 64 and max_dlp is not None:
            m = max_dlp
        else:
            if max_dlp is None:
                m = int(q ** 0.5) + 1
            else:
                m = min(int(q ** 0.5) + 1, max_dlp)
        n = 10000
        start = 0
        giant_steps = {}
        giant = 1
        while start < m:
            end = min(start + n, m)
            # print((start, end))
            res, giant_step = self.discrete_logarithm_sub(g_pow_v, g, q, start, end, giant_steps, giant)
            if res is not None:
                return res
            start = end

        return None  # No logarithm found within the range

    def discrete_logarithm_sub(self, g_pow_v, g, p, m_min, m_max, giant_steps, giant):
        # Precompute giant steps
        for j in range(m_min, m_max):
            giant_steps[giant] = j
            giant = (giant * g) % p

        # Compute baby steps
        inv_g_m = pow(inverse(g, p), m_max, p)
        baby = g_pow_v
        for i in range(m_min, m_max):
            if baby in giant_steps:
                return i * m_max + giant_steps[baby], None
            baby = (baby * inv_g_m) % p

        return None, giant_steps  # No logarithm found within the range

    def split_into_chunks(self, number, p):
        """
        Split a large number into smaller chunks.

        Args:
            number (int): The input number to split.

        Returns:
            list: A list of smaller integers.
        """
        # Determine chunk size based on the size of p
        chunk_size = (p - 1).bit_length() - 1  # Using (p - 1) to ensure the chunks are smaller than p

        chunks = []
        first = True
        while number or first:
            # Extract the least significant chunk_size bits
            chunk = number % (1 << chunk_size)
            chunks.append(chunk)
            # Shift number to the right by chunk_size bits
            number >>= chunk_size
            first = False
        return chunks[::-1]

    def recover_number(self, chunks, p):
        """
        Recover the original number from smaller chunks.

        Args:
            chunks (list): List of smaller integers.
            chunk_size (int): The size of each chunk.

        Returns:
            int: The original number.
        """
        # Determine chunk size based on the size of p
        chunk_size = (p - 1).bit_length() - 1  # Using (p - 1) to ensure the chunks are smaller than p
        number = 0
        for chunk in chunks:
            if chunk is None:
                return None
            number = (number << chunk_size) + chunk
        return number

    # Asymmetric encryption
    def encrypt(self, msg, public_key, group, save_k=False):
        # Convert the plaintext to bytes and then to an integer
        converted_number = bytes_to_long(msg)
        return self.encrypt_from_int(converted_number,public_key, group, save_k)
    # Asymmetric encryption
    def encrypt_from_int(self, number, public_key, group, save_k=False, exponential=False):
        en_msg = []
        # Split the number into smaller chunks
        chunks = self.split_into_chunks(number, group.q)
        # print("Chunks:", chunks)
        for i in range(0, len(chunks)):
            k = Utility.generate_number_in_q(group)  # Random key
            k = 10
            u = pow(group.g, k, group.p)
            if exponential is True:
                v = (pow(public_key, k, group.p) * pow(group.g, number, group.p)) % group.p
                # v = (pow(public_key, k, group.p) * pow(group.g, number, group.p))
            else:
                v = (pow(public_key, k, group.p) * number) % group.p

            # print("g^k (u) used : ", u)
            # print("g^ak (v) used : ", v)
            if save_k:
                en_msg.append((u, v, k))
            else:
                en_msg.append((u, v))

        if save_k:
            return EncryptedTextAndK(en_msg)
        return EncryptedText(en_msg)

    def decrypt_from_int(self, encrypted_text, private_key, group, exponential=False, right=None,
                         no_dlp_searching=False, max_dlp=None):
        dr_msg = []
        for i in range(0, len(encrypted_text.chunk)):
            chunk = encrypted_text.chunk[i]
            u = chunk[0]
            v = chunk[1]
            if right is None:
                right = pow(u, -1 * private_key, group.p)
            if exponential is True:
                # print("exp")
                m_prime = (v * right) % group.p
                # m_prime = g^m . Find m for known m_prime and known g (DLP).
                # return bsgs( group.g,m_prime, group.q)
                if no_dlp_searching:
                    d = m_prime
                else:
                    d = self.discrete_logarithm(m_prime, group.g, group.p, max_dlp)
            else:
                d = (v * right) % group.p
            dr_msg.append(d)

        # print("dr_msg:", dr_msg)
        recovered_number = self.recover_number(dr_msg, group.q)
        # print("Recovered number:", recovered_number)
        return recovered_number

    def decrypt(self, encrypted_text, private_key, group, exponential=False):
        recovered_number = self.decrypt_from_int(encrypted_text, private_key, group, exponential)
        regenerated_string = long_to_bytes(recovered_number).decode()
        return regenerated_string


    # Driver code
    def main(self):
        # p = 11
        # g = 3
        # q = 5
        # group = AppConfig().el_gamal_groups.get("just-for-test")
        group = AppConfig().el_gamal_groups.get("BELENIOS-2048")
        # Bob key generation
        # Generate a private key
        # x = getRandomRange(1, group.q - 2)
        x = 5
        y = pow(group.g, x, group.p)
        keys_pair = KeysPair(y, x)
        # print("g used : ", group.g)
        # print("g^a (public_key) used : ", keys_pair.public_key)

        # Alice's encryption message with Bob public key
        # encrypted_text = self.encrypt(msg.encode(), keys_pair.public_key, group)
        # exponential = False
        exponential = True
        # exit(False)
        encrypted_text1 = self.encrypt_from_int(10, keys_pair.public_key, group, save_k=False, exponential=exponential)
        decrypted_text = self.decrypt_from_int(encrypted_text1, keys_pair.private_key, group, exponential=exponential,
                                               max_dlp=10 ** 2)
        print(decrypted_text)
        if decrypted_text != 10:
            exit(False)

        encrypted_text2 = self.encrypt_from_int(10, keys_pair.public_key, group, save_k=False, exponential=exponential)
        decrypted_text = self.decrypt_from_int(encrypted_text2, keys_pair.private_key, group, exponential=exponential,
                                               max_dlp=10 ** 2)
        print(decrypted_text)
        if decrypted_text != 10:
            exit(False)
        # exit()

        f = EncryptedText([((encrypted_text1.chunk[0][0] * encrypted_text2.chunk[0][0]) % group.p,
                            (encrypted_text1.chunk[0][1] * encrypted_text2.chunk[0][1]) % group.p)])
        # f = EncryptedText([(pow(encrypted_text1.chunk[0][0],2,group.p) , pow(encrypted_text1.chunk[0][1],2,group.p))])
        # print(f)
        # exit()
        decrypted_text = self.decrypt_from_int(f, keys_pair.private_key, group, exponential=exponential,
                                               max_dlp=10 ** 5)
        print(decrypted_text)
        if decrypted_text != 20:
            exit(False)

        encrypted_text1 = self.encrypt_from_int(10 ** 5, keys_pair.public_key, group, save_k=False,
                                                exponential=exponential)
        decrypted_text = self.decrypt_from_int(encrypted_text1, keys_pair.private_key, group, exponential=exponential,
                                               max_dlp=10 ** 6)
        print(decrypted_text)
        if decrypted_text != 10 ** 5:
            exit(False)

        encrypted_text2 = self.encrypt_from_int(10, keys_pair.public_key, group, save_k=False,
                                                exponential=exponential)
        decrypted_text = self.decrypt_from_int(encrypted_text2, keys_pair.private_key, group, exponential=exponential,
                                               max_dlp=10 ** 3)
        print(decrypted_text)
        if decrypted_text != 10:
            exit(False)
        # exit()

        f = EncryptedText([((encrypted_text1.chunk[0][0] * encrypted_text2.chunk[0][0]) % group.p,
                            (encrypted_text1.chunk[0][1] * encrypted_text2.chunk[0][1]) % group.p)])
        # f = EncryptedText([(pow(encrypted_text1.chunk[0][0],2,group.p) , pow(encrypted_text1.chunk[0][1],2,group.p))])
        # print(f)
        # exit()
        decrypted_text = self.decrypt_from_int(f, keys_pair.private_key, group, exponential=exponential,
                                               max_dlp=10 ** 9)
        print(decrypted_text)
        if decrypted_text != (10 ** 5) + (10):
            exit(False)
        exit(True)
        decrypted_text = self.decrypt_from_int(f, keys_pair.private_key, group, exponential=True, max_dlp=10 ** 5)
        print("Decrypted Message :", decrypted_text)
        exit()
        if decrypted_text == 50000 + 604321:
            print("is homomorphic by sum")
        decrypted_text = self.decrypt_from_int(f, keys_pair.private_key, group, exponential=True, max_dlp=10 ** 5)
        print("Decrypted Message :", decrypted_text)
        exit()
        encrypted_text1 = self.encrypt_from_int(10, keys_pair.public_key, group, save_k=False, exponential=False)
        # print(encrypted_text1)
        encrypted_text2 = self.encrypt_from_int(10, keys_pair.public_key, group, save_k=False, exponential=False)
        # print(encrypted_text2)

        f = EncryptedText([(encrypted_text1.chunk[0][0] * encrypted_text2.chunk[0][0],
                            encrypted_text1.chunk[0][1] * encrypted_text2.chunk[0][1])])
        decrypted_text = self.decrypt_from_int(f, keys_pair.private_key, group, exponential=False)

        if decrypted_text == 10 * 10:
            print("is homomorphic by mul")
        print("Decrypted Message :", decrypted_text)
        # print("Is Message correct :", msg == decrypted_text)

        # a = EncryptedTextAndK(chunk=[(4668496126002962658882380217764192095482229044353957117271293358702925124310,
        #                               30397351926047547824654525111658362281056689471750309174167068820938261670430,
        #                               49164449440762570282379174637271973724871893072529699739403694160311175459599)])
        # pk = 46848588746177681989295036151738831494583428455369152762249665817922661702588
        # pub = 66003342716164202112599502859642890596263702302645409972366290560489068378251
        # pub2 = pow(group.g, pk, group.q)
        # print("pub", pub == pub2, pub2)
        # right = 1842561303388720141086967684726446539599603118724140243523399057502308417786670020647042626062945533525282363258206419086505960146180970575368136477223948706063675097215028411798029050315690578296129426861953639126723525644368988519151481189078378712844441981296086127497349204213478543795633586046613583090647511436030387362640850775912085133649344927468703990258714127783000273033922947006372940887198361548874714524620270794156832114456759242638903314506860253621014015049420318494360289857435405025449163951034744450081017573083116399442458111588827827127402104349888893533522797993830704967457983704703915756214
        # # a = ElGamal().encrypt_from_int(1, pub, group, save_k=True, exponential=True)
        # print("dsf", self.decrypt_from_int(a, pk, group, exponential=True, right=right))

if __name__ == '__main__':
    ElGamal().main()
