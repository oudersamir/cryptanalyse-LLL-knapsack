import sys
import constants
import liblll
import utility
import ciphering
import deciphering
import attacking
import logger
import time
import ast 

"""
For test purposes. You can also use this file as main file to check all application
"""
logger = logger.build_logger("tester")


def main():

    
    
    decipher_as_receiver(ast.literal_eval(read_in_file("resultat/output_msg_crypt.txt")), 
        ast.literal_eval(read_in_file("keys/public_key/modulo.txt")), 
        ast.literal_eval(read_in_file("keys/public_key/multiplicative_to_mask.txt")),
        ast.literal_eval(read_in_file("keys/private_key/private_key.txt")))
    
    os.remove("keys/private_key/private_key.txt")
    os.remove("keys/public_key/modulo.txt")
    os.remove("keys/public_key/multiplicative_to_mask.txt")
    os.remove("keys/public_key/public_key.txt")

#open and read the file after the appending:
   

   
 # la fonction dechiffrement qui prend en parametre le text chiffrer ,et le cle public (modulo,multiplicative) et la cle privee(suite super croissante)
def decipher_as_receiver(ciphered_vector, modulo, multiplicative_to_mask, private_key_vector):
    t = time.process_time()
    print("\nAs a " + constants.bold_attribute + "RECEIVER" + constants.attribute_default +
          " who generated public key, you own the modulo, multiplicative and private key vector. " +
          "\nThese were used to generate public key vector. \n" +
          constants.foreground_colorant_green +
          "So, you can easily decipher the cipher text with using private key vector." + constants.attribute_default + "\n")
    # decheifrere le text
    print("Deciphering part is about to start...\n")
    deciphered_vector = deciphering.decipher_vector_elements(ciphered_vector, modulo, multiplicative_to_mask)

    if utility.log_enabled:
        print("deciphered_vector: " + str(deciphered_vector) + "\n")

    print("Knapsack solution algorithm is about to start...\n")

    deciphered_bit_sequences = list()
    for i in range(0, len(deciphered_vector)):
        deciphered_item = deciphered_vector[i]
        deciphered_bit_sequence = deciphering.deciphered_items_to_bit_sequence(
            constants.algorithm_back_tracking, private_key_vector, deciphered_item)
        deciphered_bit_sequences.append(deciphered_bit_sequence)

    print("Knapsack solution algorithm is over.\n")

    if utility.log_enabled:
        print("deciphered_bit_sequences: " + str(deciphered_bit_sequences) + "\n")

    deciphered_text = ""
    for i in range(0, len(deciphered_bit_sequences)):
        deciphered_bit_sequence = deciphered_bit_sequences[i]
        bit_to_text = utility.convert_bit_to_text(deciphered_bit_sequence, len(private_key_vector))
        deciphered_text += bit_to_text

    print("Finished to decipher the text in " + str(time.process_time()-t) + " ms as a receiver.\n\n" +
          "Original text: " +
          str(deciphered_text))
    print("le text chiffrer : " + str(ciphered_vector) )
    write_in_file("resultat/input_msg_decrypt.txt",deciphered_text)
    text=input("dechiffrement  est termine")

    return True





def _get_selection(prompt, options):
    choice = input(prompt).upper()
    while not choice or choice[0] not in options:
        choice = input("Please enter one of {}. {}".format('/'.join(options), prompt)).upper()
    return choice[0]


def get_filename():
    """Ask the user for a filename, reprompting for nonempty input.

    Doesn't check that the file exists.
    """
    filename = input("Filename? ")
    while not filename:
        filename = input("Filename? ")
    return filename

def get_input(binary=False):
    """Prompt the user for input data, optionally read as bytes."""
    print("* Input *")
    choice = _get_selection("(F)ile or (S)tring? ", "FS")
    if choice == 'S':
        text = input("Enter a string: ").strip().upper()
        while not text:
            text = input("Enter a string: ").strip().upper()
        if binary:
            return bytes(text, encoding='utf8')
        return text
    else:
        filename = get_filename()
        flags = 'r'
        if binary:
            flags += 'b'
        with open(filename, flags) as infile:
            return infile.read()


def set_output(output, binary=False):
    """Write output to a user-specified location."""
    print("* Output *")
    choice = _get_selection("(F)ile or (S)tring? ", "FS")
    if choice == 'S':
        print(output)
    else:
        filename = get_filename()
        flags = 'w'
        if binary:
            flags += 'b'
        with open(filename, flags) as outfile:
            print("Writing data to {}...".format(filename))
            outfile.write(output)


def write_in_file(file,input):
    f = open(file, "w")
    f.write(str(input))
    f.close()

def read_in_file(file):
     f = open(file,"r")
     return f.read()


     
if __name__ == "__main__":
    
        main()
        print("*****************************************************************8.\n")
        
