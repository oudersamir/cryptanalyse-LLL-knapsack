import sys
import constants
import liblll
import utility
import ciphering
import deciphering
import attacking
import logger
import time

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
    private_key_vector = utility.generate_super_increasing_vector()
    modulo = utility.determine_modulo_acc_to_random_key_vector(private_key_vector)
    multiplicative_to_mask = utility.determine_element_to_mask(modulo)

    print("\n la cle privee (suite super croissante): " + str(private_key_vector))
    print("modulo (m) : " + str(modulo))
    print("multiplicative_to_mask (n) : " + str(multiplicative_to_mask))

    public_key_vector = ciphering.generate_public_key_vector(private_key_vector, modulo, multiplicative_to_mask)
    print("\n la cle public est : "+str(public_key_vector) )

    
    write_in_file("resultat/public_key.txt",public_key_vector)

    input_text = ""
    if not utility.random_text_test:
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

    ciphered_vector = ciphering.cipher_with_bit_sequences(public_key_vector, bit_grouped_sequences)

    print("le text chiffrer : " + str(ciphered_vector) )
    write_in_file("resultat/output_msg_crypt.txt",ciphered_vector)

    input_text = utility.user_input("Which one do you want to continue as? \n" +
                                    "For receiver: R, For man-in-the-middle attacker: A",
                                    constants.regex_pattern_decipher_side_choice)

    if input_text.upper() == "R":
        decipher_as_receiver(ciphered_vector, modulo, multiplicative_to_mask, private_key_vector)
    elif input_text.upper() == "A":
        decipher_as_attacker(ciphered_vector, public_key_vector)

    print("\n" + constants.foreground_colorant_yellow + "The application ended" + constants.attribute_default)
    print(constants.terminal_delimiter)
   

#open and read the file after the appending:
   

   

def decipher_as_receiver(ciphered_vector, modulo, multiplicative_to_mask, private_key_vector):
    t = time.process_time()
    print("\nAs a " + constants.bold_attribute + "RECEIVER" + constants.attribute_default +
          " who generated public key, you own the modulo, multiplicative and private key vector. " +
          "\nThese were used to generate public key vector. \n" +
          constants.foreground_colorant_green +
          "So, you can easily decipher the cipher text with using private key vector." + constants.attribute_default + "\n")

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
   

    return True


def decipher_as_attacker(ciphered_vector, public_key_vector):
    t = time.process_time()
    print("\nAs an " + constants.bold_attribute + "ATTACKER" + constants.attribute_default +
          ", you own the ciphered vector, public key vector. \n" +
          constants.foreground_colorant_green +
          "So, you can decipher the cipher text with using lattice reduction." + constants.attribute_default + "\n")

    print("Deciphering part is about to start...\n")
    deciphered_text = ""
    print("LLL basis lattice reduction algorithm is about to start...\n")
    for i in range(0, len(ciphered_vector)):
        ciphered_message = ciphered_vector[i]
        base_vector_list = attacking.create_base_vector_list(public_key_vector, ciphered_message)
        if utility.log_enabled:
            print("base_vector_list: " + str(base_vector_list) + "\n")

        matrix_to_lll_reduction = liblll.create_matrix(base_vector_list)
        if utility.log_enabled:
            print("matrix_to_lll_reduction:\n")
            liblll.print_mat(matrix_to_lll_reduction)
            print("\n")
        reduced_matrix = liblll.lll_reduction(matrix_to_lll_reduction)
        if utility.log_enabled:
            print("reduced_matrix:\n")
            liblll.print_mat(reduced_matrix)
            print("\n")

        deciphered_bit_sequence = attacking.get_first_column_as_bit_sequence(reduced_matrix)

        if utility.log_enabled:
            print("deciphered_bit_sequence:\n")
            liblll.print_mat(deciphered_bit_sequence)
            print("\n")
        bit_to_text = utility.convert_bit_to_text(deciphered_bit_sequence, len(public_key_vector))
        deciphered_text += bit_to_text

    print("Lattice reduction algorithm is over.\n")
    print("Finished to decipher the text in " + str(time.process_time()-t) + " ms as an attacker.\n\n" +
          "Original text: " +
          str(deciphered_text))
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


if __name__ == "__main__":
    
        main()
        print("*****************************************************************8.\n")

