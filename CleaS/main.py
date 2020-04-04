import sys
import argparse
import CleaS.functions as functions
import CleaS.settings as settings


class ArgException(Exception):
    """Raise it when user is idiot"""
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def __str__(self):
        return self.expression + ": " + self.message


def create_parser():
    """Args parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', required=True, help="""Programm mode (ex: python witproject.py -m 1): \n 
    1(default): Say smth. Must be arg -a(--additional) SECONDS_FOR_SPEECH \n
    2: File .wav input. Must be arg -a(--additional) FILE_PATH""")
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help="""
    If exists program will display outputs text view of speech recognizing in output.txt""")
    parser.add_argument('-a', '--additional', default=False, help="""Additional info (not use if don't need)""")
    parser.add_argument('-e', '--equal', default=False, help="""If exists program will compare input text with received text, must be file path""")
    return parser


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    text = ""
    # Mode difference only in text input. Here is different types of input:
    if int(namespace.mode) == 1:
        print("Speak!")
        functions.audio_recording(filename='input.wav', seconds=int(namespace.additional))
        text = functions.recognize_speech('input.wav')
    elif int(namespace.mode) == 2:
        text = functions.recognize_speech(namespace.additional)
    else:
        raise ArgException(expression='Wrong args', message='Please check correct of input args and try again.')

    if namespace.verbose:
        with open('output.txt', 'w') as output:
            output.write(text)

    if namespace.equal:
        with open(namespace.equal) as file_to_compare:
            words_in_wav_to_compare = [x for x in text.lower().split()]
            words_in_wav = words_in_wav_to_compare.copy()
            words_in_compare = []
            count = 0
            buffer = ""
            for x in file_to_compare.read()+" ":
                if x != " ":
                    buffer += x
                elif settings.ALLOWED_SYMBOLS.__contains__(x):
                    if buffer != "":
                        if words_in_wav.__contains__(buffer.lower()):
                            words_in_wav.remove(buffer.lower())
                            count += 1
                        else:
                            words_in_compare.append(buffer.lower())
                        buffer = ""
            if not len(words_in_compare) and not len(words_in_wav):
                if namespace.verbose:
                    with open('output.txt', 'a') as output:
                        output.write("\n---------------------------------\nPerfect! 100%")
                print("Perfect! 100%")
            else:
                response = "Purity: {a}%".format(
                    a=int(10000*(count/(len(words_in_wav)+len(words_in_compare))))/100) + \
                        "\nExcess words that you said: " + " ".join(words_in_wav) + '.' + \
                        "\nExpected words that you should have said: " + " ".join(words_in_compare) + '.'
                print(response)
                if namespace.verbose:
                    with open('output.txt', 'a') as output:
                        output.write("\n---------------------------------\n{a}%".format(a=response))
