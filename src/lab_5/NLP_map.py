import tkinter as tk
from tkinter import filedialog
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk

# Download necessary nltk packages
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


class WordCloudGenerator:
    """
    A class used to generate word clouds from text files.

    ...

    Attributes
    ----------
    master : tk.Tk
        a tkinter GUI window
    load_buttons : list
        a list of tkinter buttons for loading text files
    file_paths : list
        a list of tkinter StringVars to hold the file paths
    labels : list
        a list of tkinter labels to display the file paths
    generate_button : tk.Button
        a tkinter button to generate the word clouds
    texts : list
        a list to hold the texts from the loaded files

    Methods
    -------
    load_file(index)
        Opens a file dialog to load a text file and reads its content.
    generate_word_clouds()
        Generates and displays word clouds for the loaded texts.
    process_text(text)
        Processes the text by removing punctuation, stop words and lemmatizing.
    """

    def __init__(self, master):
        """
        Constructs all the necessary attributes for the WordCloudGenerator object.

        Parameters
        ----------
            master : tk.Tk
                a tkinter GUI window
        """

        self.master = master
        self.master.title("Word Cloud Generator")

        # Create buttons for loading files
        self.load_buttons = [tk.Button(master, text=f"Load Text {i + 1}", command=lambda i=i: self.load_file(i))
                             for i in range(3)]
        for i, button in enumerate(self.load_buttons):
            button.pack()

        # Create StringVars for file paths
        self.file_paths = [tk.StringVar() for _ in range(3)]
        self.labels = [tk.Label(master, textvariable=self.file_paths[i]) for i in range(3)]
        for label in self.labels:
            label.pack()

        # Create button for generating word clouds
        self.generate_button = tk.Button(master, text="Generate Word Clouds", command=self.generate_word_clouds)
        self.generate_button.pack()

        # Initialize texts list
        self.texts = [None] * 3

    def load_file(self, index):
        """
        Opens a file dialog to load a text file and reads its content.

        Parameters
        ----------
            index : int
                the index of the file to load
        """

        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            self.file_paths[index].set(path)
            with open(path, 'r', encoding='utf-8') as file:
                self.texts[index] = file.read()

    def generate_word_clouds(self):
        """
        Generates and displays word clouds for the loaded texts.
        """

        for i, text in enumerate(self.texts):
            if text:
                processed_text = self.process_text(text)
                wordcloud = WordCloud(width=800, height=400).generate(processed_text)
                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                plt.title(f'Word Cloud for Text {i + 1}')
                plt.show()

    def process_text(self, text):
        """
        Processes the text by removing punctuation, stop words and lemmatizing.

        Parameters
        ----------
            text : str
                the text to process

        Returns
        -------
            str
                the processed text
        """

        custom_stop_words = {'w', 'np', 'naz', 'wym', 'z', 'na', 'o'}  # Custom stop words
        stop_words = set(stopwords.words('english')).union(custom_stop_words)
        lemmatizer = WordNetLemmatizer()

        # Remove punctuation
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalpha()]

        # Remove stop words and lemmatize
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
        return ' '.join(words)


root = tk.Tk()
app = WordCloudGenerator(root)
root.mainloop()