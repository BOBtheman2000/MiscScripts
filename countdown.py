import msvcrt as m
import random as r
import os

# words

probs = {
    'a':15,
    'b':2,
    'c':3,
    'd':6,
    'e':21,
    'f':2,
    'g':3,
    'h':2,
    'i':13,
    'j':1,
    'k':1,
    'l':5,
    'm':4,
    'n':8,
    'o':13,
    'p':4,
    'q':1,
    'r':9,
    's':9,
    't':9,
    'u':5,
    'v':1,
    'w':1,
    'x':1,
    'y':1,
    'z':1,
}

pot_vowels = ['a','e','i','o','u']
pot_consonants = [l for l in
                  [chr(i+97) for i in range(ord('z') - ord('a') + 1)]
                    if l not in pot_vowels]

def gen_letters():
    vowels = [l for l in pot_vowels for x in range(probs[l])]
    consonants = [l for l in pot_consonants for x in range(probs[l])]
    return vowels, consonants

with open(os.path.realpath(__file__) + '\..\\words.txt', 'r') as file:
    words = [line.strip('\n') for line in file]

def get_character(vowels, consonants):
    kp = m.getch()
    match kp:
        case b'v':
            out = vowels[r.randint(0, len(vowels)-1)]
            vowels.remove(out)
            return out
        case b'c':
            out = consonants[r.randint(0, len(consonants)-1)]
            consonants.remove(out)
            return out
        case b'h':
            return False
    exit()

def check_word(letters, word):
    temp_letter_set = letters.copy()
    for ch in word:
        if ch in temp_letter_set:
            temp_letter_set.remove(ch)
        else:
            return False
    return True

def check_word_flexible(letters, word):
    letter_slots = 10 - len(letters)
    temp_word = list(word)
    for ch in letters:
        if ch in temp_word:
            temp_word.remove(ch)
    if len(temp_word) <= letter_slots:
        return True
    return False

def assess_letters(chr_set):
    found_words = {}
    flexible_words = {}
    for word in words:
        if len(word) <= len(chr_set):
            if check_word(chr_set, word):
                app_tab = found_words.get(len(word), [])
                app_tab.append(word)
                found_words[len(word)] = app_tab
        if check_word_flexible(chr_set, word):
            app_tab = flexible_words.get(len(word), [])
            app_tab.append(word)
            flexible_words[len(word)] = app_tab
    return found_words, flexible_words

# numbers

def get_number_kb():
    kp = m.getch()
    try:
        return int(kp)
    except ValueError:
        exit()

def get_oper_kb():
    print('+ - x /')
    kp = m.getch()
    match kp:
        case b'0':
            return '+'
        case b'1':
            return '-'
        case b'2':
            return 'x'
        case b'3':
            return '/'

def gen_numbers(lg_count: int):
    if lg_count > 4:
        exit()
    out = []
    smalls = [i + 1 for i in list(range(10))*2]
    larges = [(i + 1) * 25 for i in list(range(4))]
    for i in range(6):
        if i < lg_count:
            add = larges[r.randint(0, len(larges)-1)]
            out.append(add)
            larges.remove(add)
        else:
            add = smalls[r.randint(0, len(smalls)-1)]
            out.append(add)
            smalls.remove(add)
    return out

def operate_numbers(l:int|float, r:int|float, op:str):
    match op:
        case '+':
            return l+r
        case '-':
            return l-r
        case 'x':
            return l*r
        case '/':
            res = l/r
            if int(res) != float(res):
                print("hey")
                exit()
            return int(res)
    return l+r

# main loop
os.system('cls')

print('pick one')

play_words = False

kp = m.getch()
if kp == b'n':
    play_words = False
elif kp == b'w':
    play_words = True
else:
    exit()

while True:
    os.system('cls')

    if play_words:
        v, c = gen_letters()

        letter_set = []
        print('get letters')
        for i in range(10):
            letter = False
            while letter == False:
                print(' '.join(letter_set))
                letter = get_character(v, c)
                if letter == False:
                    ass, flex = assess_letters(letter_set)
                    print('possible so far:', ', '.join(ass.get(max([i for i in ass if i <= len(letter_set)]), ['none lol'])))
                    print('best potential words:', ', '.join(flex[max([i for i in flex if i <= 10])]))
                    m.getch()
                    os.system('cls')
                    print('')
            letter_set.append(letter)
            print('\033[1A', end='\x1b[2K')
        print(' '.join(letter_set))

        player_word = input('get word\n')

        cpu_words = []
        cpu_len = 0
        cpu_found_words = 0
        for word in words:
            if check_word(letter_set, word):
                cpu_found_words += 1
                if len(word) > cpu_len:
                    cpu_words.clear()
                    cpu_len = len(word)
                if len(word) == cpu_len:
                    cpu_words.append(word)

        if player_word not in words:
            print('what')
            print(cpu_found_words, 'potential words')
            print('i had', ', '.join(cpu_words))
        elif not check_word(letter_set, player_word):
            print('hey')
            print(cpu_found_words, 'potential words')
            print('i had', ', '.join(cpu_words))
        elif player_word in cpu_words:
            cpu_words.remove(player_word)
            print('NICE')
            print(cpu_found_words, 'potential words')
            if len(cpu_words) > 0:
                print('i also had', ', '.join(cpu_words))
            else:
                print('that was it btw')
        else:
            print('yea we good')
            print(cpu_found_words, 'potential words')
            print('i had', ', '.join(cpu_words))

        kp = m.getch()
        if kp == b'n':
            play_words = False
        elif kp != b'\r':
            exit()
    else:
        target = r.randint(100, 999)

        print('get large')
        num_pool = gen_numbers(get_number_kb())

        print('\033[1A', end='\x1b[2K')
        print(target)

        while len(num_pool) > 1:
            np_write = [str(i) for i in num_pool]
            print(' '.join(np_write))

            ind_1 = get_number_kb()
            np_write[ind_1] = f"[{np_write[ind_1]}]"
            print('\033[1A', end='\x1b[2K')
            print(' '.join(np_write))

            ind_2 = get_number_kb()
            if ind_2 == ind_1:
                print('\033[1A', end='\x1b[2K')
                num_pool = [num_pool[ind_2]]
                break
            np_write[ind_2] = f"<{np_write[ind_2]}>"
            print('\033[1A', end='\x1b[2K')
            print(' '.join(np_write))

            ind_o = get_oper_kb()


            num_1 = num_pool[ind_1]
            num_2 = num_pool[ind_2]
            num_pool.append(operate_numbers(num_1, num_2, ind_o))
            num_pool.remove(num_1)
            num_pool.remove(num_2)
            print('\033[1A', end='\x1b[2K')
            print('\033[1A', end='\x1b[2K')

        result = num_pool[0]
        print(result)
        if result == target:
            print('NICE')
        elif abs(result - target) <= 5:
            print('yea we good')
            print('off by', abs(result - target))
        elif abs(result - target) <= 10:
            print('ooer')
            print('off by', abs(result - target))
        else:
            print('nah')
            print('off by', abs(result - target))

        kp = m.getch()
        if kp == b'w':
            play_words = True
        elif kp != b'\r':
            exit()