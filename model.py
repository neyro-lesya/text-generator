from __future__ import print_function

import pickle
import random
import numpy as np


# Размер префикса будет выбираться рандомно(1 или2)
# n_model - класс, описывающий N-граммную модель, которая и генерирует новый текст, на основе старого
class n_model:
    COUNT_WORDS_IN_PREFIX = random.randint(1, 2)

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, text=''):
        self.__dictionaries_prefixes = dict.fromkeys('', np.array(['']))
        self.__size = 0
        if text != '':
            self.__fit(text)
        else:
            file = open("save_model.txt", "rb")
            self.__dictionaries_prefixes = pickle.load(file)

    def __fit(self, text):
        new_text = n_model.text_preparation(text)
        number_prefix = 0
        number_last = 0
        while number_last != len(new_text) - 1:
            prefix_tabs_and_word = self.__get_words_and_tabs_number(new_text, number_prefix)
            if self.__dictionaries_prefixes.get(prefix_tabs_and_word[0]) is not None:
                array = self.__dictionaries_prefixes.get(prefix_tabs_and_word[0])
                array = np.append(array, prefix_tabs_and_word[1])
                self.__dictionaries_prefixes.pop(prefix_tabs_and_word[0])
                self.__dictionaries_prefixes[prefix_tabs_and_word[0]] = array
            else:
                new_cell = np.array([prefix_tabs_and_word[1]])
                self.__dictionaries_prefixes[prefix_tabs_and_word[0]] = new_cell
                self.__size += 1
            number_prefix = prefix_tabs_and_word[2]
            number_last = prefix_tabs_and_word[3]

    @classmethod
    # Метод __get_words_and_tabs_number возвращает нам префикс, слово, следующее за префиксом, номер пробела с которого
    # будем смотреть следующий префикс и номер последнего символа для определения конца строки
    def __get_words_and_tabs_number(cls, text, first_tab):
        i = first_tab
        if text[first_tab] == ' ':
            first_tab += 1
        prefix = ''
        count_tabs = 0
        word = ''
        number_first_tab = 0
        for i in range(first_tab, len(text)):
            if text[i] != ' ':
                if not text[i].isalpha():
                    continue
                if count_tabs < n_model.COUNT_WORDS_IN_PREFIX:
                    prefix += text[i]
                if count_tabs == n_model.COUNT_WORDS_IN_PREFIX:
                    word += text[i]
            else:
                if count_tabs == 0:
                    prefix += text[i]
                    number_first_tab = i
                if count_tabs == n_model.COUNT_WORDS_IN_PREFIX:
                    break
                count_tabs += 1
        return prefix, word, number_first_tab, i

    @staticmethod
    def text_preparation(text):
        new_text = ''
        for i in text:
            if i.isalpha():
                if i.isupper():
                    new_symbol = i.lower()
                    new_text += new_symbol
                    continue
                new_text += i
                continue
            else:
                if i == '\n':
                    new_text += ' '
                if i.isspace():
                    if new_text[len(new_text) - 1] != ' ':
                        new_text += i
                elif new_text[len(new_text) - 1] != ' ':
                    new_text += ' '
        return new_text

    def __save_model(self):
        file = open(r'save_model.txt', "wb")
        pickle.dump(self.__dictionaries_prefixes, file)
        file.close()

    def __generate(self):
        array_keys = list(self.__dictionaries_prefixes.keys())
        size = random.randint(1, len(array_keys))
        array_random_keys = [''] * size
        text = ''
        for i in range(size):
            random_index = random.randint(0, len(array_keys) - 1)
            array_random_keys[i] = array_keys[random_index]
        count_constructions_in_sentence = random.randint(0, 5)
        number_construction = 0
        for i in range(size):
            word_in_sentence = array_random_keys[i]
            if number_construction == 0:
                word_in_sentence = word_in_sentence.capitalize()
            word = list(self.__dictionaries_prefixes.get(array_random_keys[i]))
            number_construction += 1
            text += ' ' + word_in_sentence + ' ' + word[random.randint(0, len(word)) - 1]
            if number_construction == count_constructions_in_sentence or i == size - 1:
                text += '.'
                number_construction = 0
                count_constructions_in_sentence = random.randint(0, 5)
        return text

    def print(self):
        text = self.__generate()
        print(text)

    def __del__(self):
        if self.__size != 0:
            self.__save_model()
        else:
            self.print()
