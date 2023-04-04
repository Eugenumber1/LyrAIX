import tensorflow as tf
import pandas as pd
import numpy as np
from tqdm import tqdm


class SongCreator:

    def __init__(self, songs, avarage, n_steps=100, temp=1):
        self.songs = songs
        self.avarage = avarage
        self.texts = str()
        self.titles = list()
        self.n_steps = n_steps
        self.temperature = temp
        self.new_song = str()
        #print(self.texts)

    """
    This method populates two lists with song titles and song texts
    """
    def input(self):
        for song in self.songs:
            self.texts += song.song_text
            #print(type(song.song_text))
            #self.titles.append(song.song_title)
        #print(self.texts)
        #for text in self.texts:
            #print(text)

    def create_tokenizer_texts(self):
        tokenizer = tf.keras.preprocessing.text.Tokenizer(char_level=True)
        # print(type(self.texts))
        # print(self.texts)
        # for text in self.texts:
        #     print(text[0])
        tokenizer.fit_on_texts(self.texts)
        return tokenizer

    def create_tokenizer_titles(self):
        tokenizer = tf.keras.preprocessing.text.Tokenizer(char_level=False)

        tokenizer.fit_on_texts([self.titles])
        return tokenizer

    """
    This method creates the encoding and some initial preprocessing
    """
    def preprocessing(self):
        self.input()

        #print(self.texts)
        tokenizer_texts = self.create_tokenizer_texts()
        #tokenizer_titles = self.create_tokenizer_titles()
        max_id_texts = len(tokenizer_texts.word_index) # number of distinct chars
        dataset_size_texts = tokenizer_texts.document_count # total number of chars
        print(tokenizer_texts.texts_to_sequences(["First"]))
        print(tokenizer_texts.sequences_to_texts([[20, 6, 9, 8, 3]]))
        print("max id is " + str(max_id_texts))
        print("dataset size is " + str(dataset_size_texts))

        #max_id_titles = len(tokenizer_titles.word_index)
        #dataset_size_titles = tokenizer_titles.document_count
        [encoded_texts] = np.array(tokenizer_texts.texts_to_sequences([self.texts])) - 1
        print(type(encoded_texts))
        print(len(encoded_texts))

        #[encoded_titles] = np.array(tokenizer_titles.texts_to_sequences(self.titles)) - 1
        # print(encoded_texts)
        # for i in encoded_texts:
        #     print(i)
        return (max_id_texts, dataset_size_texts, encoded_texts, tokenizer_texts)#, (max_id_titles, dataset_size_titles, encoded_titles, tokenizer_titles)


    def split_texts(self, tup):
        max_id_texts, dataset_size_texts, encoded_texts = tup[0], tup[1], tup[2]
        train_size = dataset_size_texts * 80 // 100
        dataset = tf.data.Dataset.from_tensor_slices(encoded_texts[:train_size])
        # for i in dataset:
        #     print(i)
        return dataset

    def chop_texts_into_windows(self, dataset, max_id):
        window_len = self.n_steps
        dataset = dataset.window(window_len, shift=1, drop_remainder=True)
        dataset = dataset.flat_map(lambda window: window.batch(window_len))
        batch_size = 32
        dataset = dataset.shuffle(10000).batch(batch_size)
        dataset = dataset.map(lambda windows: (windows[:, :-1], windows[:, 1:]))
        dataset = dataset.map(lambda X_batch, Y_batch: (tf.one_hot(tf.cast(X_batch, tf.int64), depth=max_id, dtype=tf.int64), Y_batch))
        dataset = dataset.prefetch(1)
        return dataset

    def create_model(self, dataset, max_id):
        model = tf.keras.models.Sequential([
            tf.keras.layers.GRU(64, return_sequences=True, input_shape=[None, max_id], dropout=0.2, recurrent_dropout=0.2),
            tf.keras.layers.GRU(16, return_sequences=True, dropout=0.2, recurrent_dropout=0.2),
            tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(max_id, activation="softmax"))])
        model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", run_eagerly=True, metrics=['accuracy'])
        # for i in dataset:
        #     print(i)
        history = model.fit(dataset, epochs=15)
        print(history)
        return model


    def next_char(self, model_texts, max_id_texts, tokenizer_texts):
        X = np.array(tokenizer_texts.texts_to_sequences("W")) - 1
        one_hot_texts = tf.one_hot(X, max_id_texts)
        y_proba = model_texts.predict(one_hot_texts)[0, -1:, :]
        rescaled_logits = tf.math.log(y_proba) / self.temperature
        char_id = tf.random.categorical(rescaled_logits, num_samples=1) + 1
        return tokenizer_texts.sequences_to_texts(char_id.numpy())[0]

    def generate_song(self):
        text_tup = self.preprocessing()#, title_tup = self.preprocessing()
        (max_id_texts, dataset_size_texts, encoded_texts, tokenizer_texts) = text_tup
        #(max_id_titles, dataset_size_titles, encoded_titles, tokenizer_titles) = title_tup
        dataset_texts = self.split_texts(text_tup)
        dataset_texts = self.chop_texts_into_windows(dataset_texts, max_id_texts)
        model_texts = self.create_model(dataset_texts, max_id_texts)
        # fake prepocess
        for _ in range(self.avarage):
            self.new_song += self.next_char(model_texts, max_id_texts, tokenizer_texts)

        return self.new_song








