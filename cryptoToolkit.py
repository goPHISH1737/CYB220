# Defining lists of needed letters and frequencies
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

english_words = []

frequencies = [12.702, 9.056, 8.167, 7.507, 6.966, 6.749, 6.327, 6.094, 5.987,
               4.253, 4.025, 2.782, 2.758, 2.406, 2.360, 2.228, 2.015, 1.974,
               1.929, 1.772, 1.492, 0.978, 0.253, 0.250, 0.095, 0.074]

freq_sort_letters = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u',
                     'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']

# Moving the englishwords.txt file into a list
with open('englishwords.txt') as file:
    for line in file:
        english_words.append(line.split())


def split_ciphertext(text):
    """This function makes the ciphertext usable by the other functions"""
    split_text = text.split()

    words = []
    for word in split_text:
        placeholder = ''
        for char in word:
            if char.lower() in letters:
                placeholder += char.lower()
        if placeholder:
            words.append(placeholder)

    return words


def is_english(ciphertext):
    """This function checks what percentage of words in a plaintext are in the list of english words"""
    words = split_ciphertext(ciphertext)
    num_words = len(words)
    num_english_words = 0

    for word in words:
        if len(word) > 1 or word == 'i' or word == 'a':
            if [word] in english_words:
                num_english_words += 1

    return num_english_words / num_words


def check_caesar(ciphertext):
    """Caesar cipher decoder / best key finder"""
    english_score = 0
    best_key = 0
    best_candidate = ciphertext
    for i in range(0,26):
        plaintext = ''
        for char in ciphertext:
            if char.lower() in letters:
                plaintext += letters[((letters.index(char.lower())) + i) % 26]
            else:
                plaintext = f"{plaintext}{char}"

        if is_english(plaintext) > english_score:
            english_score = is_english(plaintext)
            best_key = i
            best_candidate = plaintext

    return english_score, 26-best_key, best_candidate


def frequency_analysis(ciphertext, compare=False):
    """This function does a frequency analysis of the ciphertext, and can optionally return only the mapping
    , which is useful for certain decoders"""
    mapping = {}
    total_letters = 0
    for char in letters:
        mapping[char] = 0

    for char in ciphertext:
        if char.lower() in letters:
            mapping[char.lower()] += 1
            total_letters += 1

    letter_percentages = []

    for key, value in mapping.items():
        letter_percentages.append((value / total_letters) * 100)

    letter_percentages.sort(reverse=True)

    total = 0
    for i in letter_percentages:
        total += i

    english_closeness = 100

    for i, value in enumerate(letter_percentages):
        english_closeness -= abs(frequencies[i] - value)

    if compare:
        return mapping, english_closeness

    return english_closeness


def check_atbash(ciphertext):
    """This function simply reverses the alphabet and swaps the ciphertext into the reversed alphabet"""
    reverse_alphabet = letters[::-1]

    plaintext = ''
    for char in ciphertext:
        if char.lower() in letters:
            plaintext = f"{plaintext}{reverse_alphabet[letters.index(char.lower())]}"
        else:
            plaintext = f"{plaintext}{char}"

    return is_english(plaintext), plaintext


def check_vigenere(ciphertext, key_range):
    """This function first determines which key length is the best, then determines which key is the best,
    then decodes the ciphertext based on the best key"""
    key_size = 2
    best_key_size = 2
    best_freq = 0
    best_chunks = []
    for k in range(2, key_range + 1):
        nth_ciphertext = ['' for i in range(0, k)]
        split_ct = split_ciphertext(ciphertext)
        clean_ct = ''
        for word in split_ct:
            clean_ct = f"{clean_ct}{word}"
        for n, block in enumerate(nth_ciphertext):
            count = n
            for i in range(0, int(len(clean_ct) / k)):
                block = f"{block}{clean_ct[count]}"
                count += k
            nth_ciphertext[n] = block

        total_freq = 0.0
        for block in nth_ciphertext:
            total_freq += frequency_analysis(block)
        total_freq = total_freq / k

        if total_freq > best_freq:
            best_freq = total_freq
            best_key_size = k
            best_chunks = nth_ciphertext[:]

    # This starts the process of trying to find the best key
    english_closeness = 0

    best_key = ''

    for chunk in best_chunks:
        rotated_chunks = []
        for rot in range(0, 26):
            rotated_chunk = ''
            for char in chunk:
                rotated_chunk = f"{rotated_chunk}{(letters[((letters.index(char.lower())) + rot) % 26])}"
            rotated_chunks.append(rotated_chunk)

        best_letter_close = -200
        best_letter = 'a'
        for rot, rotated_chunk in enumerate(rotated_chunks):
            mapping = frequency_analysis(rotated_chunk, True)[0]
            sorted_freqs = sorted(mapping.items(), key=lambda x:x[1], reverse=True)

            letter_close = 100
            for pos, group in enumerate(sorted_freqs):
                letter = group[0]
                letter_close -= abs(freq_sort_letters.index(letter) - pos)

            if letter_close > best_letter_close:
                best_letter_close = letter_close
                if rot == 0:
                    best_letter = 'a'
                else:
                    best_letter = letters[26 - rot]

        best_key = f"{best_key}{best_letter}"

    plaintext_chunks = ['' for i in range(0, len(best_key))]

    for i, chunk in enumerate(best_chunks):
        for char in chunk:
            plaintext_chunks[i] = f"{plaintext_chunks[i]}{letters[(letters.index(char) - letters.index(best_key[i])) % 26]}"

    plaintext = ''
    count = 0

    for i in range(0, len(best_chunks[0]) * best_key_size):
        if i % best_key_size == 0 and i != 0:
            count += 1
        plaintext = f"{plaintext}{plaintext_chunks[i % best_key_size][count]}"

    return best_key, plaintext


def decode_rail_fence(ciphertext, rails):
    """This function first makes the fence, then maps the ciphertext to the fence, then decodes it based on this"""
    rail_fence = [['' for x in range(0, len(ciphertext))] for i in range(0, rails)]

    count = 0
    direction = 'up'

    for i, char in enumerate(ciphertext):

        rail_fence[count][i] = 'a'

        if count == 0:
            if direction == 'down':
                direction = 'up'
        if count == rails - 1:
            if direction == 'up':
                direction = 'down'
        if direction == 'up':
            count += 1
        if direction == 'down':
            count -= 1

    number_each = []

    for i, rail in enumerate(rail_fence):
        number_each.append(rail.count('a'))

    split_cipher = []
    total = 0
    for num in number_each:
        split_cipher.append(ciphertext[total:total+num])
        total += num

    final_fence = [[] for i in range(0, rails)]
    iteration = 0
    for i, rail in enumerate(rail_fence):
        for letter in rail:
            if letter == 'a':
                final_fence[i].append(split_cipher[i][iteration])
                iteration += 1
            else:
                final_fence[i].append('')
        iteration = 0

    final_ciphertext = ''

    count = 0

    for i, char in enumerate(ciphertext):

        final_ciphertext = f"{final_ciphertext}{final_fence[count][i]}"

        if count == 0:
            if direction == 'down':
                direction = 'up'
        if count == rails - 1:
            if direction == 'up':
                direction = 'down'
        if direction == 'up':
            count += 1
        if direction == 'down':
            count -= 1

    return final_ciphertext


def check_rail_fence(ciphertext):
    """This function checks all possible numbers of rails from 2 to 10"""
    print("Rail Fence")
    for i in range(2, 10):
        print(f"{i} Rails: {decode_rail_fence(ciphertext, i)}")


def check_all(ciphertext):
    """This function does all the checks on the ciphertext"""
    caesar = check_caesar(ciphertext)
    atbash = check_atbash(ciphertext)
    vigenere = check_vigenere(ciphertext, 10)
    print(f"Best Caesar key: {caesar[1]}. English percentage: {int(caesar[0] * 100)}")
    print(f"Best Caesar plaintext: {caesar[2]}")
    print(f"Atbash: {atbash[1]}. English percentage: {int(caesar[0] * 100)}")
    print(f"Best Vigenere Key: {vigenere[0]}")
    print(f"Best Vigenere Plaintext: {vigenere[1]}")
    check_rail_fence(ciphertext)

print("--Simple Cipher Type Identifier--")
ct = input("Enter ciphertext: ")

check_all(ct)