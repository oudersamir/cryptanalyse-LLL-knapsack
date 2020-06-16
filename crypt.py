import sys
import constants
import liblll
import utility
import ciphering
import deciphering
import attacking
import logger
import time
import os

"""
For test purposes. You can also use this file as main file to check all application
"""
logger = logger.build_logger("tester")


def main():
    validation_message = utility.validate_initial_parameters()
    if validation_message != "":
        print(validation_message)
        sys.exit()
    
    print(constants.terminal_delimiter)
    print("\n" + constants.foreground_colorant_yellow + "The application started" + constants.attribute_default)
    #la generation de la suite super croissante  ( cle privee)
    private_key_vector = utility.generate_super_increasing_vector()
    #la generation de modulo
    modulo = utility.determine_modulo_acc_to_random_key_vector(private_key_vector)
    multiplicative_to_mask = utility.determine_element_to_mask(modulo)

    print("\n la cle privee (suite super croissante): " + str(private_key_vector))
    # stocker la cle prive (suite super crioissante) 
    write_in_file("keys/private_key/private_key.txt",private_key_vector)

    print("modulo (m) : " + str(modulo))
    # stocker la cle public (modulo est multiplicative ) 
    write_in_file("keys/public_key/modulo.txt",modulo)

    print("multiplicative_to_mask (n) : " + str(multiplicative_to_mask))
    write_in_file("keys/public_key/multiplicative_to_mask.txt",multiplicative_to_mask)

    #la generation de la cle publique a partir  de cle prive ,modulo et multiplicatif 
    public_key_vector = ciphering.generate_public_key_vector(private_key_vector, modulo, multiplicative_to_mask)
    print("\n la cle public est : "+str(public_key_vector) )


    write_in_file("keys/public_key/public_key.txt",public_key_vector)

    input_text = ""
    if not utility.random_text_test:
         # saisir le text claire
        input_text = utility.user_input("entrer le text ", "")
        print("input text: " + str(input_text) + "\n")
        write_in_file("resultat/input_msg_clear.txt",input_text)

    else:
        input_text = utility.generate_random_text(utility.length_of_random_text)
        print("generated input text: " + str(input_text) + "\n")
        utility.press_enter_to_continue()

    bit_converted_text = utility.convert_text_to_bit(input_text, len(public_key_vector))
    bit_grouped_sequences = utility.group_on_sequence(bit_converted_text, len(private_key_vector))

    print(" debut de chiffrement ...\n")

    if utility.log_enabled:
        print("bit_converted_text: " + str(bit_converted_text) + "\n")
        print("bit_grouped_sequences: " + str(bit_grouped_sequences) + "\n")
   # chiffrer le text claire
    ciphered_vector = ciphering.cipher_with_bit_sequences(public_key_vector, bit_grouped_sequences)
    # stocker le text chiffrer
    print("le text chiffrer : " + str(ciphered_vector) )
    write_in_file("resultat/output_msg_crypt.txt",ciphered_vector)


   
    
    print("\n" + constants.foreground_colorant_yellow + "The application ended" + constants.attribute_default)
    print(constants.terminal_delimiter)

    
    # S=131  
    # a=[4,6,11,25,50,110]
    # z=[0,0,0,0,0,0,]
    # n=len(a)
    # i=n
    # while i >=1 :
    #     if S>= a[i] :
    #         x[i]=1
    #         S=S-a[i]
    #     else: x[i]=0
    #     i=i-1


#open and read the file after the appending:
   

   




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


if __name__ == "__main__":
    
        main()
        print("*****************************************************************8.\n")

