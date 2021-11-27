import string

cyrillic = 'йцукенгшщзхъфывапролджэячсмитьбюё'


def encode(message, offset, key):
    base_alphabet = cyrillic
    if len(key) > len(base_alphabet):
        raise RuntimeError('key is longer than alphabet!')
    for ch in key:
        if (list(base_alphabet).count(ch) != 1
            or list(key).count(ch) > 1):
            raise RuntimeError('key is invalid')
        

    alphabet = list(key + base_alphabet)

    i = len(alphabet)
    while i > 0:
        i -= 1
        if alphabet.index(alphabet[i]) != i:
            alphabet.pop(i)

    alphabet = alphabet[-offset:] + alphabet[:-offset]

    return ''.join(map(lambda x: x if x not in alphabet else alphabet[base_alphabet.index(x)],
                       message))

def encode_data():
    data = None
    with open('data.txt', 'r') as f:
        data = f.read().lower()
    encoded = encode(data, 5, 'мойключ')
    with open('encoded.txt', 'w') as f:
        f.write(encoded)
    

freq = {'а': 8.01, 'б': 1.59, 'в': 4.54, 'г': 1.7, 'д': 2.98, 'е': 8.45, 'ё': 0.04, 'ж': 0.94, 'з': 1.65, 'и': 7.35, 'й': 1.21, 'к': 3.49, 'л': 4.4, 'м': 3.21, 'н': 6.7, 'о': 10.97, 'п': 2.81, 'р': 4.73, 'с': 5.47, 'т': 6.26, 'у': 2.62, 'ф': 0.26, 'х': 0.97, 'ц': 0.48, 'ч': 1.44, 'ш': 0.73, 'щ': 0.36, 'ъ': 0.04, 'ы': 1.9, 'ь': 1.74, 'э': 0.32, 'ю': 0.64, 'я': 2.01}

for k in freq.keys():
    freq[k] /= 100

def get_bigrams(text):
    bi = {}
    count = 0
    for i in range(len(text)-1):
        if text[i] in cyrillic and text[i+1] in cyrillic:
            count += 1
            s = text[i] + text[i+1]
            if s in bi.keys():
                bi[s] += 1
            else:
                bi.setdefault(text[i] + text[i+1], 0)

    for k in bi.keys():
        bi[k] /= count
    return bi

lang_bi = None
with open('data.txt') as f:
    lang_bi = get_bigrams(f.read())

def decode(text, relations):
    """relations - пары {'a':'b'} букв алфавита которые соовтетствуют друг другу"""
    return ''.join([x if x not in relations.keys() else relations[x]
                    for x in text])

sample_text = None
with open('encoded.txt') as f:
    sample_text = f.read()[:300]

def decode_data():
    data = None
    with open('encoded.txt') as f:
        data = f.read()
    s = list(''.join([c if c in cyrillic else '' for c in data]))
    l = len(s)
    letter_freq = {}
    for k in freq.keys():
        letter_freq.setdefault(k, s.count(k)/l)
    sorted_letters = sorted([ [x, letter_freq[x]] for x in letter_freq.keys()],
                            key=lambda x: -x[1])
    sorted_lang = sorted([ [x, freq[x]] for x in freq.keys()],
                         key=lambda x: -x[1])
    # print(sorted_letters)
    # print(sorted_lang)

    bi = get_bigrams(data)

    sorted_lang_bi = sorted([ [x, lang_bi[x]] for x in lang_bi.keys()],
                            key=lambda x: -x[1])
    sorted_bi = sorted([ [x, bi[x]] for x in bi.keys()],
                       key=lambda x: -x[1])

    bigrams_count = 50

    # print(sorted_lang_bi[:bigrams_count])
    # print(sorted_bi[:bigrams_count])
    rel = {}
    for i in range(bigrams_count):
        _from1 = sorted_bi[i][0][0]
        _from2 = sorted_bi[i][0][1]
        _to1 = sorted_lang_bi[i][0][0]
        _to2 = sorted_lang_bi[i][0][1]
        if _from1 in rel.keys():
            if _to1 != rel[_from1]:
                continue
        if _from2 in rel.keys():
            if _to2 != rel[_from2]:
                continue
        if _to1 in rel.values() or _to2 in rel.values():
            continue
        rel.setdefault(_from1, _to1)
        rel.setdefault(_from2, _to2)
    # print('rel', rel)
    i = len(sorted_letters)
    while i >= 0:
        i -= 1
        if sorted_lang[i][0] in rel.values():
            sorted_letters.pop(i)
            sorted_lang.pop(i)
    for i in range(len(sorted_lang)):
        if sorted_letters[i][0] not in rel.keys() and sorted_lang[i][0] not in rel.values():
            rel.setdefault(sorted_letters[i][0],
                           sorted_lang[i][0])
    rest_encoded = []
    rest_decoded = []
    for c in cyrillic:
        if c not in rel.keys():
            rest_encoded.append(c)
        if c not in rel.values():
            rest_decoded.append(c)
    i = len(rest_encoded)
    while i >= 0:
        i -= 1
        rel.setdefault(rest_encoded[i],
                       rest_decoded[i])
    return decode(sample_text, rel)

def main():
    with open('data.txt') as f:
        original = f.read()[:300]
    print('Начало оригинального текста:\n' + original)
    print('Зашифрованный текст:\n' + sample_text)
    print('Расшифрованный текст:\n' + decode_data())
