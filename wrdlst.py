# wrdlst 1.0
# Created by Camden Sloan
import math

# Welcome message
print("wrdlst 1.0")
start_message = "Choose an option to begin\n" \
                "1 - Create wordlist from scratch\n" \
                "2 - Modify existing wordlist\n" \
                "3 - Combine 2 wordlists\n" \
                "4 - Create smart wordlist based on target profile"
print(start_message)

# Determining which option the user selected
option = '0'
option_input = input("Enter the number of the option you would like to use: ")
if option_input == '1' or '2' or '3' or '4':
    option = option_input

# Defining lists of common character sets
lower_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

upper_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

special_chars = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/'
                 ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|',
                 '}', '~']


def gen_list(length, charset):
    """This function will generate a wordlist given a character or word set and a given length"""
    final_list = []
    current_entry = ''
    set_len = len(charset)
    for i in range(0, len(charset)**length):
        for k in range(0, length):
            # Calculates the index of the list for the two values and combines them
            current_entry = f"{charset[math.floor(i/(set_len**k))%set_len]}{current_entry}"
        final_list.append(current_entry)
        current_entry = ''

    return final_list


def create_input():
    """This function will create a character set from user input"""
    password_length_raw = input("Number of characters for each entry (enter a range in the form min-max): ")

    # Parses user input while catching errors
    parsed_length = password_length_raw.split('-')
    try:
        min_length = int(parsed_length[0])
    except ValueError:
        print("Invalid input")
        exit()
    charset_choice_raw = input("Character set (0: Lower letters, 1: Upper letters, 2: Numbers, 3: Special Chars): ")

    # Parses input into actual range
    if len(parsed_length) == 2:
        max_length = int(parsed_length[1])
    else:
        max_length = min_length

    # Determines which character sets the user selected and adds them together
    chars = []
    choice_split = [*charset_choice_raw]

    if '0' in choice_split:
        for char in lower_letters:
            chars.append(char)
    if '1' in choice_split:
        for char in upper_letters:
            chars.append(char)
    if '2' in choice_split:
        for char in numbers:
            chars.append(char)
    if '3' in choice_split:
        for char in special_chars:
            chars.append(char)

    final_lst = []

    # Generates a wordlist for each number in the range using the characters selected and creates a final list
    for i in range(min_length, max_length + 1):
        final_lst = final_lst + gen_list(i, chars)

    return final_lst


def combine_list(list1, list2):
    """This function combines two wordlists"""
    combined = []

    for line1 in list1:
        for line2 in list2:
            combined.append(f"{line1}{line2}")

    return combined


if option == "1":
    # Custom wordlist from scratch
    custom_list = create_input()
    out_file_path = input("Output file path: ")

    # Writes wordlist to output file
    with open(out_file_path, 'w') as file_object:
        for c in custom_list:
            file_object.write(f"{c}\n")

if option == "2":
    # Modify existing wordlist
    file_path = input("Input file / path: ")
    out_file = input("Output file: ")

    # Opens input file and saves it as the input list
    with open(file_path) as file_object:
        input_list = file_object.read().split()

    # Displays option message
    option_message = "-----Options----- \n" \
                     "p - add prefix\n" \
                     "s - add suffix\n" \
                     "l - leetspeak\n" \
                     "r - reverse\n" \
                     "u - uppercase\n" \
                     "o - lowercase"
    print(option_message)

    # Takes user input and splits it into a list
    options_raw = input('Select option(s): ')
    options_split = [*options_raw]

    for letter in options_split:

        if letter == 'p':
            # Prefix option
            print("---Define prefix---")
            prefixes = create_input()
            input_list = combine_list(prefixes, input_list)

        if letter == 's':
            # Suffix option
            print("---Define suffix---")
            suffixes = create_input()
            input_list = combine_list(input_list, suffixes)

        if letter == 'l':
            # Leetspeak option
            split_words = []
            for word in input_list:
                split_word = [*word]
                leet_word = []
                for char in split_word:
                    if char == 'e' or char == 'E':
                        leet_word.append('3')
                    elif char == 'o' or char == 'O':
                        leet_word.append('0')
                    elif char == 'i' or char == 'I' or char == 'l' or char == 'L':
                        leet_word.append('1')
                    elif char == 's' or char == 'S':
                        leet_word.append('5')
                    elif char == 't' or char == 'T':
                        leet_word.append('7')
                    else:
                        leet_word.append(char)
                split_words.append(leet_word)

            leet_list = []

            for word in split_words:
                new_word = ''
                for char in word:
                    new_word = f"{new_word}{char}"
                leet_list.append(new_word)

            input_list = leet_list

        if letter == 'r':
            # Reverse option
            reversed_words = []
            for word in input_list:
                reversed_words.append(word[::-1])
            input_list = reversed_words

        if letter == 'u':
            # Uppercase option
            upper_words = []
            for word in input_list:
                upper_words.append(word.upper())
            input_list = upper_words

        if letter == 'o':
            # Lowercase option
            lower_words = []
            for word in input_list:
                lower_words.append(word.lower())
            input_list = lower_words

    # Writes to output file
    with open(out_file, 'w') as file_object:
        for word in input_list:
            file_object.write(f"{word}\n")

if option == "3":
    # Combine wordlists
    file1_path = input("Enter the file name / path to file of the first file: ")
    file2_path = input("Enter the file name / path to file of the second file: ")
    out_file_path = input("Enter a name for the output file: ")

    # Opens wordlists to combine
    with open(file1_path) as file_object:
        contents1 = file_object.read().split()

    with open(file2_path) as file_object:
        contents2 = file_object.read().split()

    # Combines the lists
    combined_list = combine_list(contents1, contents2)

    # Writes to file
    with open(out_file_path, 'w') as file_object:
        for c in combined_list:
            file_object.write(f"{c}\n")

if option == "4":
    # Smart wordlist generator
    print("\n--Smart Wordlist Generator--")
    message = "To use, enter any keywords\n" \
              "To specify what the keyword is, use the format {type}={keyword}\n" \
              "For example, input 'birthyear=1990' to enter the target's birth year\n" \
              "For a list of types, input 't=?'\n" \
              "To stop, input t=stop"
    print(message)

    # Data to use for custom list
    types = ['first', 'middle', 'last', 'birthday=DDMMYYYY', 'birthyear=YYYY', 'birthmonth=MM',
             'website', 'kidnames=name1,name2,...', 'partner', 'pets', 'sportsteam']

    months = {'01': ['January', 'Jan'], '02': ['February', 'Feb'], '03': ['March', 'Mar'], '04': ['April', 'Apr'],
              '05': ['May', 'May'], '06': ['June', 'Jun'], '07': ['July', 'Jul'], '08': ['August', 'Aug'],
              '09': ['September', 'Sep'], '10': ['October', 'Oct'], '11': ['November', 'Nov'],
              '12': ['December', 'Dec']}

    keep_going = True
    words = []
    initials = []

    while keep_going:
        # This loop continues until the user inputs stop
        raw_word = input("Enter info: ")
        split_word = raw_word.split('=')

        if len(split_word) == 1:
            # Keyword only
            words.append(split_word[0])
        elif len(split_word) == 2:
            # Type + Keyword
            type = split_word[0]
            word = split_word[1]
            if type == 't' and word == 'stop':
                keep_going = False
            elif type == 't' and word == '?':
                for t in types:
                    print(t)
            else:
                # Adds custom words to final list according to keyword type
                if type == 'first' or 'middle' or 'last':
                    # Adds lowercase and titled name to wordlist and adds initials to list of initials
                    words.append(word.lower())
                    words.append(word.title())
                    if type == 'first':
                        initials.insert(0, list(word)[0].upper())
                    if type == 'last':
                        initials.append(list(word)[0].upper())
                    if type == 'middle':
                        initials.insert(1, list(word)[0].upper())
                if type == 'birthday':
                    # Splits up birthday into day, month, and year and adds versions of each to the final list
                    bday_split = list(word)
                    if len(bday_split) == 8:
                        day_list = bday_split[0:2]
                        day = ''
                        for c in day_list:
                            day = f"{day}{c}"
                        month_list = bday_split[2:4]
                        month = ''
                        for c in month_list:
                            month = f"{month}{c}"
                        if word in months:
                            words.append(months[word][0])
                            words.append(months[word][1])
                            words.append(months[word][0].upper())
                            words.append(months[word][1].upper())
                            words.append(word)
                        year_list = bday_split[4:8]
                        year = ''
                        for c in year_list:
                            year = f"{year}{c}"
                        year_list_2 = bday_split[6:8]
                        year_2 = ''
                        for c in year_list_2:
                            year_2 = f"{year_2}{c}"
                        words.append(day)
                        words.append(month)
                        words.append(year)
                        words.append(year_2)
                        words.append(word)
                if type == 'birthyear':
                    # Adds birth year and last two digits of birth year to final list
                    year_split = list(word)
                    if len(year_split) == 4:
                        year_list_2 = year_split[6:8]
                        year_2 = ''
                        for c in year_list_2:
                            year_2 = f"{year_2}{c}"
                        words.append(word)
                        words.append(year_2)
                if type == 'birthmonth':
                    # Adds digits of the birth month in addition to the actual name of the month and abbreviated form
                    if word in months:
                        words.append(months[word][0])
                        words.append(months[word][1])
                        words.append(word)
                        words.append(months[word][0].lower())
                        words.append(months[word][1].lower())
                if type == 'website':
                    words.append(f"@{word}")
                    words.append(word)
                if type == 'kidnames':
                    # Adds kids' names and different variations
                    kids = word.split(',')
                    print(kids)
                    for kid in kids:
                        words.append(kid.lower())
                        words.append(kid.title())
                    num_kids = len(kids)
                    words.append(f"{num_kids}kids")
                    words.append(f"{num_kids}Kids")
                if type == 'partner':
                    # Adds partner's name and phrases related to it
                    words.append(word.lower())
                    words.append(word.title())
                    words.append(f"ILove{word.title()}")
                    words.append(f"ilove{word.lower()}")
                if type == 'sportsteam':
                    # Adds sports team and phrases related to it
                    words.append(word.lower())
                    words.append(word.title())
                    words.append(f"{word.lower()}fan")
                    words.append(f"{word.title()}fan")
        else:
            # Bad input
            print("Invalid entry, try again")

    # Adds versions of initials to the final list
    if len(initials) == 1:
        words.append(initials[0].lower())
        words.append(initials[0].upper())
    if len(initials) == 2:
        words.append(f"{initials[0].lower()}{initials[1].lower()}")
        words.append(f"{initials[0].upper()}{initials[1].upper()}")
    if len(initials) == 3:
        words.append(f"{initials[0].lower()}{initials[1].lower()}{initials[2].lower()}")
        words.append(f"{initials[0].upper()}{initials[1].upper()}{initials[2].upper()}")
        words.append(f"{initials[0].lower()}{initials[2].lower()}")
        words.append(f"{initials[0].upper()}{initials[2].upper()}")

    # Asks for entry length and output file path and catches errors
    try:
        entry_length = int(input("Length of each entry: "))
    except ValueError:
        print('Invalid input')
        exit()
    out_file_name = input("Output file name: ")

    # Generates wordlist and writes to file
    fnal_list = gen_list(entry_length, words)
    with open(out_file_name, 'w') as file_object:
        for c in fnal_list:
            file_object.write(f"{c}\n")
