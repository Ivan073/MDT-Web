from Lab2.Task1.helpers import process_abbreviations, get_word_list, get_sentence_list
from Lab2.Task1.parser import count_sentences, count_nondeclarative_sentences, count_average_length_of_sentences
from input import get_text
# ‪D:\Programming\BSUIR\SCOI\Lab2\Task1\sample.txt


def main():
    print("Choose the way to get text:\n" +
          "1. Input text\n" +
          "2. Input path to file")
    text = get_text()

    optimized_text = process_abbreviations(text)
    print("Text:", text)
    print("Sentence amount:", count_sentences(optimized_text))
    print("Non-declarative sentence amount:", count_nondeclarative_sentences(optimized_text))
    print("Average sentence length:", count_average_length_of_sentences(optimized_text))




if __name__ == '__main__':
    main()
