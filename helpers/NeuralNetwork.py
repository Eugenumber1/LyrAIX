import tensorflow as tf
import pandas as pd
import numpy as np


"""
This method does the preprocessing of the text, create the vocabulary of it.
It uses the character level only
"""
def preprocess(text):
    tokenizer = tf.keras.preprocessing.text.Tokenizer(char_level=True)
    tokenizer.fit_on_texts([text])
    [encoded] = np.array(tokenizer.texts_to_sequences([text])) - 1
    max_id = len(tokenizer.word_index)
    dataset_size = tokenizer.document_count
    return encoded, max_id, dataset_size




