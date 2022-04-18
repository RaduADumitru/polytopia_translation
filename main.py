import os
import json
import threading
from deep_translator import DeepL, GoogleTranslator
from time import perf_counter
from itertools import islice


def nth_key(dct, n):  # get Nth key of dictionary
    it = iter(dct)
    # Consume n elements.
    next(islice(it, n, n), None)
    # Return the value at the current position.
    # This raises StopIteration if n is beyond the limits.
    # Use next(it, None) to suppress that exception.
    return next(it)


def getRanges(nr_lines, nr_threads):  # Splits data into approximately equal ranges which will be processed by threads
    base_length = nr_lines // nr_threads - 1
    print(f'Base length: {base_length}')
    longer_ranges = nr_lines % nr_threads
    # a number of ranges will be 1 longer than the base length,
    # in order to split the remaining lines after division optimally
    print(f'Number of longer ranges: {longer_ranges}')
    ranges_list = []
    range_start = 0
    nr_ranges = 0
    while nr_ranges < nr_threads:
        if longer_ranges > 0:
            range_end = range_start + base_length + 1
            longer_ranges -= 1
        else:
            range_end = range_start + base_length
        ranges_list.append((range_start, range_end))
        range_start = range_end + 1
        nr_ranges += 1
    return ranges_list


def translateRange(translator, range_start, range_end, translate_data, lock):
    # each thread runs this function for different ranges
    for i in range(range_start, range_end + 1):
        with lock:  # locked lines will only be executed by one thread at a time
            key = nth_key(translate_data, i)  # starts from 0
            nr_lines = len(translate_data.keys())
            print(f'Translating line {i + 1} of {nr_lines}')
            translate_line = translate_data[key]
        translate_value = translator.translate(translate_line)
        with lock:
            translate_data[key] = translate_value
    with lock:
        print(f'Thread ({range_start}, {range_end}) finished')
        # prints under lock in order to avoid multiple prints at same time appearing on same line
    return


if __name__ == '__main__':
    with open('en_US.json') as json_file:
        common_translator = None
        while True:
            translator_option = input('Translator to use (0 - Google Translate, 1 - DeepL): ')
            if translator_option == '0':
                common_translator = GoogleTranslator(source='en', target='ro')
                break
            elif translator_option == '1':
                common_translator = DeepL(api_key=os.environ.get('DEEPL_API_KEY'), source='en', target='ro')
                break
            else:
                print('Option not recognized!')
        threads = int(input('Number of threads: '))
        start_time = perf_counter()
        data = json.load(json_file)
        keys = len(data.keys())
        print(f'Lines translating: {keys}')
        ranges = getRanges(keys, threads)
        print(ranges)
        thread_list = []
        thread_lock = threading.Lock()
        # lock to avoid race conditions (multiple threads accesing same data at the same time)
        for translate_range in ranges:
            translate_thread = threading.Thread(target=translateRange,
                                                args=(common_translator, translate_range[0],
                                                      translate_range[1], data, thread_lock))
            thread_list.append(translate_thread)
            translate_thread.start()
        for thread in thread_list:
            thread.join()  # await termination of each thread
        print('Translation finished!')

    with open('ro.json', 'w') as fp:
        json.dump(data, fp, indent=4)
    end_time = perf_counter()

    print(f'Time: {int((end_time - start_time) // 60)} minutes {((end_time - start_time) % 60):.2f} seconds')
