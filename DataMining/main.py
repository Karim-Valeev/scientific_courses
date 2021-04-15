from collections import OrderedDict

import requests
import re
import operator
import time

# Words in English and Russian containing a dash
PATTERN_FOR_CYRILLIC_CHARACTERS = '[#A-Za-zА-Яа-я\-]+'
# Disadvantages of regular expression
UNNECESSARY_WORDS = ['-']


def split_to_cyrillic_alphabet_words(text: str):
    return re.findall(PATTERN_FOR_CYRILLIC_CHARACTERS, text)


def count_unique_words_in_list_to_dic(words: list):
    unique_words_dic = {}

    for word in words:
        if word in unique_words_dic:
            unique_words_dic[word] += 1
        else:
            unique_words_dic[word] = 1

    return unique_words_dic


def remove_unnecessary_words(words_dic):
    for key in list(words_dic):
        if key in UNNECESSARY_WORDS:
            del words_dic[key]
    return words_dic


if __name__ == '__main__':

    access_token = "2742013827420138274201389a273511902274227420138471f03a09b78c47602f0148b"
    version = '5.130'
    domain = 'itis_kfu'

    url = 'https://api.vk.com/method/wall.get?access_token'

    offset = 0
    count = 100
    posts = []
    data = {}

    start = time.perf_counter_ns()

    # For multiprocessing
    # process = multiprocessing.Process(
    #     # f - function to be executed
    #     target=f,
    #     args=(src, i)
    # )
    # process.start()

    for i in range(2):
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    "access_token": access_token,
                                    "v": version,
                                    'domain': domain,
                                    "count": count,
                                    "offset": offset
                                })

        data = response.json()["response"]["items"]
        offset += count
        posts.extend(data)

    end = time.perf_counter_ns()
    print('Downloading: ',(end-start)/10**9, " sec\n")

    all_text = ''
    for i in range(200):
        post = posts[i]
        post_text = post["text"]

        # If you want to count words from inner posts too

        # if "copy_history" in list(post):
        #     copy_history = post["copy_history"]
        #     for inner_post in copy_history:
        #         post_text += inner_post["text"]

        all_text += post_text

    # To lower case
    all_text.lower()

    start_processing = time.perf_counter_ns()

    all_words = split_to_cyrillic_alphabet_words(all_text)

    # Result dictionary
    result = count_unique_words_in_list_to_dic(all_words)

    result = remove_unnecessary_words(result)

    #
    sorted_result = dict(sorted(result.items(), key=operator.itemgetter(1), reverse=True))

    end_processing = time.perf_counter_ns()

    index = 1
    for key, value in sorted_result.items():
        if index == 100:
            break
        print(key, ' : ', value)
        index += 1

    print()
    print("Processed in: ",(end_processing-start_processing)/10**9,"sec")
    print("THE END")
