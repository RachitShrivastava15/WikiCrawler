import requests
from bs4 import BeautifulSoup
from collections import Counter
from prettytable import PrettyTable

def get_word_count(targetUrl, section_heading, number_of_words, excluded_words):
    response = requests.get(targetUrl)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the section based on heading
    heading_element = soup.find(lambda tag: tag.name == 'span' and section_heading.lower() in tag.get_text().lower())

    if heading_element:
        # Get the parent of the heading and find all text elements in the following siblings
        history_section = heading_element.find_parent().find_all_next(['p', 'ul', 'ol'])

        # Concatenate the text from all elements in the history section
        text = ' '.join(element.get_text() for element in history_section)

        # Tokenize and count words
        words = [word.lower() for word in text.split() if not (word.startswith('"') or word.endswith('"')) and word.lower() not in excluded_words]
        word_count = Counter(words)

        # Get the top N words
        top_words = word_count.most_common(number_of_words)

        return top_words
    else:
        print("Section not found.")
        return []

def display_results(word_count):
    table = PrettyTable()
    table.field_names = ["Word", "Occurrences"]

    for word, count in word_count:
        table.add_row([word, count])

    print(table)

def main():

    url = "https://en.wikipedia.org/wiki/Microsoft"
    section_heading = "History"
    default_num_words = 10
    # User input for number_of_words
    number_of_words = input("Enter the number of words to display: ")
    #handle the default value of no of words
    if not number_of_words:
        number_of_words = default_num_words

    number_of_words = int(number_of_words)
    # User input for excluded_words
    excluded_words_input = input("Enter excluded words (comma-separated): ")
    excluded_words = [word.strip().lower() for word in excluded_words_input.split(',')]

    word_count = get_word_count(url, section_heading, number_of_words, excluded_words)

    print(f"Top {number_of_words} words and their occurrences:")
    display_results(word_count)

if __name__ == "__main__":
    main()