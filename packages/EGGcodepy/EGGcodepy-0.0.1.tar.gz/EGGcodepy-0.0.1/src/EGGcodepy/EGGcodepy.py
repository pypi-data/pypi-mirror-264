class Egg:
    def encode(plaintext:str) -> str:
        '''
        Encode plaintext to egg
        '''
        egg = ''.join(format(ord(i), '08b') for i in plaintext)

        egg_out = ""
        for e in egg:
            if e == "1":
                egg_out = egg_out + "EGG "
            else:
                egg_out = egg_out + "egg "
        return egg_out
    
    def decode(eggtext:str) -> str:
        '''
        Decode egg to plaintext
        '''
        egg_list = eggtext.split()  # Split the input into individual binary representations
        decoded_text = ""
        for egg in egg_list:
            if egg == "EGG":
                decoded_text += "1"
            else:
                decoded_text += "0"
        # Convert binary string back to text
        plaintext = ''.join(chr(int(decoded_text[i:i+8], 2)) for i in range(0, len(decoded_text), 8))
        return plaintext