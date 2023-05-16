file_path = '../cmudict.dict'

# Create an empty dictionary to store the word-phoneme mappings
word_phoneme_dict = {}

encodings = ['utf-8']
for encoding in encodings:
    try:
        with open(file_path, 'r') as file:
            # print(file)
            for line in file:
                line = line.strip()
                if line:
                    print(line)
                    split = line.split()
                    word_phoneme_dict[split[0]] = ' '.join(split[1:])
            break
    except UnicodeDecodeError:
        print('Error')



print(len(word_phoneme_dict))