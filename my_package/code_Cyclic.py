#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random
from copy import copy
# длина блока кодирования
CHUNK_LENGTH = 4

# проверка длины блока
#assert not CHUNK_LENGTH % 8, 'Длина блока должна быть кратна 8'

# вычисление контрольных бит
# CHECK_BITS = [i for i in range(1, CHUNK_LENGTH + 1) if not i & (i - 1)]
# print(CHECK_BITS)

def chars_to_bin(chars):
    """
    Преобразование символов в бинарный формат
    #ord - преобразование в int
    #bin - преобразование в 2сс
    #zfill - заполнение нулями
    """
    #assert not len(chars) * 8 % CHUNK_LENGTH, 'Длина кодируемых данных должна быть кратна длине блока кодирования'
    # print (ord(chars))
    # print (bin(ord(chars)))
    # print (bin(ord(chars)).zfill(8))
    # print (bin(ord(chars))[2:])
    # print (bin(ord(chars))[2:].zfill(8))
    return ''.join([bin(ord(c))[2:].zfill(8) for c in chars])

def chunk_iterator(text_bin, chunk_size=CHUNK_LENGTH):
    """
    Поблочный вывод бинарных данных
    """
    for i in range(len(text_bin)):
        if not i % chunk_size:
            yield text_bin[i:i + chunk_size]



def set_errors(encoded):
    """
    Допустить ошибку в блоках бинарных данных
    """
    result = ''
    for chunk in chunk_iterator(encoded, CHUNK_LENGTH + 3):
        num_bit = random.randint(1, len(chunk))
        chunk = '{0}{1}{2}'.format(chunk[:num_bit - 1], int(chunk[num_bit - 1]) ^ 1, chunk[num_bit:])
        result += (chunk)
    return result


# def check_and_fix_error(encoded_chunk):
#     """
#     Проверка и исправление ошибки в блоке бинарных данных
#     """
#     check_bits_encoded = get_check_bits(encoded_chunk)
#     check_item = exclude_check_bits(encoded_chunk)
#     check_item = set_check_bits(check_item)
#     check_bits = get_check_bits(check_item)
#     if check_bits_encoded != check_bits:
#         invalid_bits = []
#         for check_bit_encoded, value in check_bits_encoded.items():
#             if check_bits[check_bit_encoded] != value:
#                 invalid_bits.append(check_bit_encoded)
#         num_bit = sum(invalid_bits)
#         encoded_chunk = '{0}{1}{2}'.format(
#             encoded_chunk[:num_bit - 1],
#             int(encoded_chunk[num_bit - 1]) ^ 1,
#             encoded_chunk[num_bit:])
#     return encoded_chunk


def get_diff_index_list(value_bin1, value_bin2):
    """
    Получить список индексов различающихся битов
    """
    diff_index_list = []
    for index, char_bin_items in enumerate(zip(list(value_bin1), list(value_bin2)), 1):
        if char_bin_items[0] != char_bin_items[1]:
            diff_index_list.append(index)
    return diff_index_list




def fact(n):
    if n == 1 or n == 0:
        return 1
    return n * fact(n-1)

def comb(n, k):
    return fact(n) / fact(n - k) / fact(k)

def division(code, g):
    part = code[:len(g)]
    for k in range(len(code) - len(g) + 1):
        part = del_zeros(part)
        if len(part) < len(g) and (k == (len(code) - len(g))):
            break
        if len(part) < len(g):
            part.append(code[k + len(g)])
            continue
        mod = []
        for i in range(1, len(g)):
            if part[i] == g[i]:
                mod.append(0)
            else:
                mod.append(1)
        if k != (len(code) - len(g)):
            mod.append(code[k + len(g)])
        part = copy(mod)
    return part

# def encode(source):
#     """
#     Кодирование данных
#     """
#     text_bin = chars_to_bin(source)
#     result = ''
#     for chunk_bin in chunk_iterator(text_bin):
#         chunk_bin = set_check_bits(chunk_bin)
#         result += chunk_bin
#     return result

def encode_loop(source):
    text_bin = chars_to_bin(source)#получаем из исходных данных, str типа '01011... '
    result = ''

    for chunk_bin in chunk_iterator(text_bin, 4):#перебираем чанки
        code = [0 if i=='0' else 1 for i in chunk_bin]#chunk_bin преобразуем в list int типа [0,1,0,0,1 ...]
        zeros = [0 for i in range(3)]
        code.extend(zeros)
        g = [1, 0, 1, 1]
        mod = division(code, g)
        while len(mod) < len(g) - 1:
            mod.insert(0, 0)
        del code[4:]
        code.extend(mod)
        #return code
        result += ''.join(['0' if i==0 else '1' for i in code])
    return result

def del_zeros(lst):
    for i in range(len(lst)):
        if lst[i] == 1:
            return lst[i:]
    return [0]

def decode_loop(encoded):
    sub_result = ''
    result = ''
    bin_result_unfixed = ''
    bin_result_fixed = ''

    fixed_encoded_list = []
    for encoded_chunk in chunk_iterator(encoded, CHUNK_LENGTH + 3):  #выделяем чанки из encoded 
        code = [0 if i=='0' else 1 for i in encoded_chunk]#encoded_chunk преобразуем в list int типа [0,1,0,0,1 ...]
        code_copy = copy(code)
        g = [1, 0, 1, 1]
        code = del_zeros(code)
        syndrom = code if len(code) < len(g) else del_zeros(division(code, g))
        
        syndrom_table = {'1': 6, '10': 5, '100': 4, '11': 3, '110': 2, '111': 1, '101': 0}
        
        bin_result_unfixed += ''.join(['0' if i==0 else '1' for i in code_copy[:4]])

        if syndrom != [0]:#исправляем по синдрому
            code_copy[syndrom_table[''.join(list(map(str, syndrom)))]] = (code_copy[syndrom_table[''.join(list(map(str, syndrom)))]] + 1) % 2

        current_chunk = ''.join(['0' if i==0 else '1' for i in code_copy[:4]])
        bin_result_fixed += current_chunk

        #fixed_encoded_list.append(code_copy[0:len(code_copy)-len(syndrom)])#в конечный list добавляем данные без циклического кода
        sub_result += current_chunk
        if len(sub_result) == 8:
            fixed_encoded_list.append(sub_result)#в конечный list добавляем данные(str) без циклического кода
            sub_result = ''
        # for fixed_chunk in fixed_encoded_list:
        #     for clean_char in [fixed_chunk[i:i + 4] for i in range(len(fixed_chunk)) if not i % 4]:#зачем тут if not i%8
        #         result += chr(int(clean_char, 2))

    for fixed_chunk in fixed_encoded_list:
        result += chr(int(fixed_chunk, 2))
    return result, bin_result_fixed, bin_result_unfixed




# def decode(encoded, fix_errors=True):
#     """
#     Декодирование данных
#     """
#     decoded_value = ''
#     fixed_encoded_list = []
#     for encoded_chunk in chunk_iterator(encoded, CHUNK_LENGTH + len(CHECK_BITS)):
#         if fix_errors:
#             encoded_chunk = check_and_fix_error(encoded_chunk)
#         fixed_encoded_list.append(encoded_chunk)

#     clean_chunk_list = []
#     for encoded_chunk in fixed_encoded_list:
#         encoded_chunk = exclude_check_bits(encoded_chunk)
#         clean_chunk_list.append(encoded_chunk)

#     for clean_chunk in clean_chunk_list:
#         for clean_char in [clean_chunk[i:i + 8] for i in range(len(clean_chunk)) if not i % 8]:
#             decoded_value += chr(int(clean_char, 2))
#     return decoded_value

# length = 4
# input_code = [1,1,0,1]

# all_length = 7

# fixed_errors = {}
# tracked_errors = {}
# for i in range(1, all_length + 1):
#     fixed_errors[i] = 0
#     tracked_errors[i] = 0
    
# encoded_code = encode_loop(copy(input_code))
# for err in range(1, 2**all_length):
#     noise_code = []
#     for i in range(all_length):
#         noise_code.append(((encoded_code[i] + int((err & 2**(all_length - i - 1)) > 0)) % 2))
#     ones_count = bin(err)[2:].count('1')
#     decoded_code, syndrom = decode_loop(copy(noise_code))
#     if syndrom!=[0]:
#         tracked_errors[ones_count] += 1
#         if decoded_code == encoded_code:
#             fixed_errors[ones_count] += 1
# print_table(all_length, fixed_errors, tracked_errors)

if __name__ == '__main__':
    source = input('Укажите текст для кодирования/декодирования:')
    print('Длина блока кодирования: {0}'.format(CHUNK_LENGTH))
    #print('Контрольные биты: {0}'.format(CHECK_BITS))
    encoded = encode_loop(source)
    print('Закодированные данные: {0}'.format(encoded))
    decoded, bin_decoded, a = decode_loop(encoded)
    print('Результат декодирования BIN: {0}'.format(bin_decoded))
    print('Результат декодирования: {0}'.format(decoded))



    encoded_with_error = set_errors(encoded)
    print('Допускаем ошибки в закодированных данных: {0}'.format(encoded_with_error))
    diff_index_list = get_diff_index_list(encoded, encoded_with_error)
    print('Допущены ошибки в битах: {0}'.format(diff_index_list))

    decoded, bin_decoded_right, bin_decoded_wrong = decode_loop(encoded_with_error)

    print('Результат декодирования ошибочных данных без исправления ошибок BIN: {0}'.format(bin_decoded_wrong))
    print('Результат декодирования ошибочных данных с исправлением ошибок BIN: {0}'.format(bin_decoded_right))
    print('Результат декодирования ошибочных данных с исправлением ошибок: {0}'.format(decoded))


    #Тут кусок циклического кода из дз прошлого года.........................................................................

# def print_table(all_length, fixed_errors, tracked_errors):
#     all_errors = {}
#     n = all_length
#     for k in range(1, all_length + 1):
#         all_errors[k] = comb(n, k)
        
#     print('| i\tCn(i)\t\tNk\tCk(%)\tNo\tCo(%) |')
#     for i in range(1, all_length + 1):
#         print("|-----------------------------------------------------|")

#         Ck = round(fixed_errors[i] / all_errors[i], 2)*100
#         Co = round(tracked_errors[i] / all_errors[i], 2)*100
#         output = f"| {i}\t{round(all_errors[i])}\t\t{fixed_errors[i]}\t{Ck}\t{tracked_errors[i]}\t{Co} "
        
#         #for num in range(1, 6 - len(str(Ck))):
#          #   output += ' '
#         for num in range(1, 6 - len(str(Co))):
#             output += ' '
#         output += '|'
#         print(output)

#     print("|-----------------------------------------------------|")



# length = 4
# input_code = [1,1,0,1]

# all_length = 7

# fixed_errors = {}
# tracked_errors = {}
# for i in range(1, all_length + 1):
#     fixed_errors[i] = 0
#     tracked_errors[i] = 0
    
# encoded_code = encode_loop(copy(input_code))
# for err in range(1, 2**all_length):
#     noise_code = []
#     for i in range(all_length):
#         noise_code.append(((encoded_code[i] + int((err & 2**(all_length - i - 1)) > 0)) % 2))
#     ones_count = bin(err)[2:].count('1')
#     decoded_code, syndrom = decode_loop(copy(noise_code))
#     if syndrom!=[0]:
#         tracked_errors[ones_count] += 1
#         if decoded_code == encoded_code:
#             fixed_errors[ones_count] += 1
# print_table(all_length, fixed_errors, tracked_errors)










# def get_check_bits_data(value_bin):
#     """
#     Получение информации о контрольных битах из бинарного блока данных
#     """
#     check_bits_count_map = {k: 0 for k in CHECK_BITS}
#     for index, value in enumerate(value_bin, 1):
#         if int(value):
#             bin_char_list = list(bin(index)[2:].zfill(8))
#             bin_char_list.reverse()
#             for degree in [2 ** int(i) for i, value in enumerate(bin_char_list) if int(value)]:
#                 check_bits_count_map[degree] += 1
#     check_bits_value_map = {}
#     for check_bit, count in check_bits_count_map.items():
#         check_bits_value_map[check_bit] = 0 if not count % 2 else 1
#     return check_bits_value_map


# def set_empty_check_bits(value_bin):
#     """
#     Добавить в бинарный блок "пустые" контрольные биты
#     """
#     for bit in CHECK_BITS:
#         value_bin = value_bin[:bit - 1] + '0' + value_bin[bit - 1:]
#     return value_bin


# def set_check_bits(value_bin):
#     """
#     Установить значения контрольных бит
#     """
#     value_bin = set_empty_check_bits(value_bin)
#     check_bits_data = get_check_bits_data(value_bin)
#     for check_bit, bit_value in check_bits_data.items():
#         value_bin = '{0}{1}{2}'.format(
#             value_bin[:check_bit - 1], bit_value, value_bin[check_bit:])
#     return value_bin


# def get_check_bits(value_bin):
#     """
#     Получить информацию о контрольных битах из блока бинарных данных
#     """
#     check_bits = {}
#     for index, value in enumerate(value_bin, 1):
#         if index in CHECK_BITS:
#             check_bits[index] = int(value)
#     return check_bits


# def exclude_check_bits(value_bin):
#     """
#     Исключить информацию о контрольных битах из блока бинарных данных
#     """
#     clean_value_bin = ''
#     for index, char_bin in enumerate(list(value_bin), 1):
#         if index not in CHECK_BITS:
#             clean_value_bin += char_bin

#     return clean_value_bin