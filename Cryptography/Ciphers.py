from crypto_utils import *
from random import randint as rn
""" All the symbols available
[' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', 
'2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D',
'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']
"""


class Cipher:
    #characters = [chr(i) for i in range(65, 91)]

    def __init__(self):
        self.characters = [chr(i) for i in range(32, 127)]

    def generate_key(self, new_key):
        return

    def encode(self, text, key):
        return

    def decode(self, text, key):
        return

    def verify(self, text):
        code = self.encode(text)
        return self.decode(code) == text

    def get_index(self, letter):
        return self.characters.index(letter)


class Caesar(Cipher):

    # Plusser hvert element med nøkkelens verdi og endrer verdien
    def encode(self, text, key):
        new_text = list(text)
        for i in range(len(text)):
            index_letter = self.characters.index(new_text[i])
            new_text[i] = self.characters[(index_letter + key + 95) % 95]
        return "".join(new_text)

    # Trekker nøkkelens verdi fra hvert element og endrer verdien
    def decode(self, text, key):
        new_text = list(text)
        for i in range(len(text)):
            index_letter = self.characters.index(new_text[i])
            new_text[i] = self.characters[(index_letter - key + 95) % 95]
        return "".join(new_text)


class Multiplicative(Cipher):


    #Ganger indeksverdien til hvert element med nøkkelen, for så å bruke modulo for ikke å komme utenfor indeks
    def encode(self, text, key):
        new_text = list(text)
        for i in range(len(new_text)):
            index_letter = self.characters.index(new_text[i])
            new_text[i] = self.characters[(index_letter * key) % 95]
        return "".join(new_text)

    # Finner modulo invers til nøkkelen, slik at den vil gå tilbake til der den var
    def decode(self, text, key):
        new_key = modular_inverse(key, 95)
        return self.encode(text, new_key)


class Affine(Cipher):

    def __init__(self):
        self.caesar = Caesar()
        self.mult = Multiplicative()

    # Encoder ved å først encode gjennom en Multiplicative, og så en Caesar
    def encode(self, text, key):
        new_word = self.mult.encode(text, key[0])
        return self.caesar.encode(new_word, key[1])

    # Decoder ved å først decode gjennom Caesar og så en Multiplicative
    def decode(self, text, key):
        new_word = self.caesar.decode(text, key[1])
        return self.mult.decode(new_word, key[0])


class Unbreakable(Cipher):

    # Hjelpemetode for å finne det 'motsatte' ordet av det jeg har fått i nøkkelen.
    # Da kommer jeg tilbake til der jeg var
    def generate_key(self, key):
        new_key = ""
        for letter in key:
            new_letter = self.characters[(95 - self.get_index(letter)) % 95]
            new_key += new_letter
        return new_key

    # Roterer igjennom nøkkelen, slik at jeg kan plusse på verdien til den enkelte bokstaven jeg er på
    def decode(self, text, key):
        new_word = ""
        for i in range(len(text)):
            new_letter = self.characters[(self.get_index(text[i]) + self.get_index(key[i % len(key)])) % 95]
            new_word += new_letter

        return new_word

    # Bruker hjelpemetoden for å finne det motsatte ordet, for så og encode, men med det nye ordet
    def encode(self, text, key):
        new_key = self.generate_key(key)
        return self.decode(text, new_key)


class RSA(Cipher):

    # Bruker metodene fra crypto_utils til å lage blokker av heltall som er blitt konvertert fra
    # nøkkelen som er gitt av mottakeren
    def encode(self, text, receiver):
        public_key = receiver.get_public_key()
        blocks = []
        for i in range(0, len(text), 2):
            t = blocks_from_text(text[i:i+2], 4)
            c = pow(t[0], public_key[1], public_key[0])
            blocks.append(c)
        return blocks

    # Bruker pow for å konvertere blokktallene til den riktige asciiverdien for stringblokken gitt
    # for så og bruke  text_from_blocks fra crypto_util for å konvertere tilbake til strenger
    # Deretter returnerer jeg listen som én streng, slik at det ikke ser ut som en liste
    def decode(self, text, key):
        new_text = []
        for block in text:
            t = pow(block, key[1], key[0])
            new_text += text_from_blocks([t], 4)
        return "".join(new_text)


