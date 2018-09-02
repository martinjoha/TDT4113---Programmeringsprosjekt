from Ciphers import *

class Person:

    def __init__(self, cipher, key):
        self.cipher = cipher
        self.key = key


    def get_key(self):
        return self.cipher.get_key()

    def set_key(self, new_key):
         self.key = new_key

    def operate_cipher(self, text):
        return


class Sender(Person):

    # Hvis cipher er av typen RSA, må sender hente den offentlige nøkkelen til mottaker for å
    # få riktig nøkkel til encode-metoden
    def operate_cipher(self, text, receiver):
        if isinstance(self. cipher, RSA):
            return self.cipher.encode(text, receiver)
        return self.cipher.encode(text, self.key)

    def send_cipher(self, receiver, text):
        new_text = self.operate_cipher(text, receiver)
        return receiver.receive_cipher(new_text)

    def get_encoded_text(self, text):
        return self.cipher.encode(text, self.key)

    def get_cipher(self):
        return self.cipher


class Receiver(Person):

    # Dersom
    def __init__(self, cipher, key):
        self.cipher = cipher
        self.key = key
        if isinstance(cipher, RSA):
            self.generate_key()

    # dersom cipheret er RSA må man decode med en annen type nøkkel som er en tuppel, men ikke et heltall
    def operate_cipher(self, text):
        if isinstance(self.cipher, RSA):
            return self.cipher.decode(text, self.private_key)
        return self.cipher.decode(text, self.key)

    # Brukes for å få riktige tall dersom cipheret er av typen RSA
    # Da må mottakeren ha ekstra nøkler som gis til senderen og til cipheret for å decode
    def generate_key(self):
        p = generate_random_prime(8)
        q = generate_random_prime(8)
        while p == q:
            q = generate_random_prime(8)
        phi = (p - 1) * (q - 1)
        e = rn(3, phi - 1)
        while extended_gcd(e, phi) != 1:
            e = rn(3, phi - 1)
        n = p * q
        d = modular_inverse(e, phi)
        self.public_key = (n, e)
        self.private_key = (n, d)


    #denne gjelder kun i det tilfellet som er RSA
    def get_public_key(self):
        return self.public_key

    def receive_cipher(self, text):
        return self.operate_cipher(text)




class Hacker(Person):


    # Lager en liste som representerer hver mulige nøkkel til hvert enkelt cipher
    # Gjør at jeg lett kan iterere gjennom hver av tilfellene i en decodemetode

    def __init__(self, cipher):
        self.words = [line.rstrip('\n') for line in open('english_words','r')]
        if isinstance(cipher, Caesar) or isinstance(cipher, Multiplicative):
            self.keys = [a for a in range(95)]
            self.cipher = cipher
        elif isinstance(cipher, Affine):
            self.keys = [(x, y) for x in range(95) for y in range(95)]
            self.cipher = cipher
        else:
            self.cipher = cipher
            self.keys = self.words

    # Itererer gjennom alle mulige nøkler, og så decoder inputstringen og ser hvordan den ser ut.
    # Har tolket det som lettest å sammenligne ordene ved å gjøre til liste.
    # Sjekker hvor mange ord som matcher med ordlisten, og den listen som har best resultat blir returnert
    def decode(self, text):
        a = [0]*len(self.keys)
        for i in range(len(self.keys)):
            new_text = self.cipher.decode(text, self.keys[i])
            x = new_text.split()
            for j in range(len(x)):
                if x[j] in self.words:
                    a[i] += 1
        return self.cipher.decode(text, self.keys[a.index(max(a))])


a = Affine()
b = Sender(a, (4, 3))
c = Receiver(a, (4, 3))
d = Hacker(a)

#print(b.send_cipher(c, "coding is good"))
x = b.operate_cipher("code", d)
print('\n' +d.decode(x))

