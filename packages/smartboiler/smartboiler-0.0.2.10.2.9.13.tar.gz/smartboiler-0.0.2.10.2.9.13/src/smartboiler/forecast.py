from distutils.command import build
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
from datetime import timedelta, datetime
from sklearn.preprocessing import RobustScaler
from tensorflow.keras.models import Sequential
import tensorflow as tf

from keras.layers import LSTM
from keras.layers import Dropout
from keras.models import Model
from keras.layers import Input, Dense
from keras.models import load_model
from keras.callbacks import EarlyStopping, ModelCheckpoint
import keras.backend as K
import numpy as np
import pandas as pd
from scipy import stats
from smartboiler.data_handler import DataHandler


class Forecast:
    def __init__(
        self, dataHandler: DataHandler, start_of_data: datetime, model_path=None
    ):
        self.batch_size = 3
        self.lookback = 6
        self.delay = 1
        self.predicted_column = "longtime_mean"
        self.dataHandler = dataHandler
        self.scaler = RobustScaler()
        self.model_path = model_path
        self.start_of_data = start_of_data

    def train_model(
        self,
        begin_of_training=None,
        end_of_training=datetime.now(),
        df_training_data=None,
    ):
        if df_training_data is None:
            if begin_of_training is None:
                begin_of_training = self.start_of_data
            print("begin of training: ", begin_of_training)
            print("end of training : ", end_of_training)
            df_training_data, _ = self.dataHandler.get_data_for_training_model(
                left_time_interval=begin_of_training,
                right_time_interval=end_of_training,
                predicted_column=self.predicted_column,
                dropna=False,
            )

        self.num_of_features = len(df_training_data.columns) - 1
        self.df_train_norm = df_training_data.copy()
        self.df_train_norm[df_training_data.columns] = self.scaler.fit_transform(
            df_training_data
        )

        self.train_gen = self.generator(
            dataframe=self.df_train_norm,
            target_name=self.predicted_column,
            lookback=self.lookback,
            delay=self.delay,
            min_index=0,
            max_index=int(df_training_data.shape[0] * 0.8),
            step=1,
            shuffle=True,
            batch_size=self.batch_size,
        )

        self.valid_gen = self.generator(
            dataframe=self.df_train_norm,
            target_name=self.predicted_column,
            lookback=self.lookback,
            delay=self.delay,
            min_index=int(df_training_data.shape[0] * 0.8),
            max_index=None,
            step=1,
            shuffle=False,
            batch_size=self.batch_size,
        )

        self.val_steps = int(
            (self.df_train_norm.shape[0] * 0.1 - self.lookback) // self.batch_size
        )
        # This is how many steps to draw from `train_gen`
        # in order to see the whole train set:
        self.train_steps = int(
            (self.df_train_norm.shape[0] * 0.9 - self.lookback) // self.batch_size
        )

    def save_model(self):
        self.model.save(self.model_path)

    def load_model(
        self,
        left_time_interval=datetime.now() - timedelta(days=2),
        right_time_interval=datetime.now(),
    ):

        df, _ = self.dataHandler.get_data_for_training_model(
            left_time_interval=left_time_interval,
            right_time_interval=right_time_interval,
            predicted_column=self.predicted_column,
            dropna=False,
        )
        self.num_of_features = len(df.columns) - 1
        self.df_train_norm = df.copy()
        self.df_train_norm[df.columns] = self.scaler.fit_transform(df)

        self.build_model()

        self.model.load_weights(self.model_path)

    def generator(
        self,
        dataframe,
        target_name,
        lookback,
        delay,
        min_index,
        max_index,
        shuffle=False,
        batch_size=128,
        step=6,
    ):

        data = dataframe.values
        data = data.astype(np.float32)
        target_indx = dataframe.columns.get_loc(target_name)

        if max_index is None:
            max_index = len(data) - delay - 1
        i = min_index + lookback
        while 1:
            if shuffle:
                rows = np.random.randint(
                    min_index + lookback, max_index, size=batch_size
                )
            else:
                if i + batch_size >= max_index:
                    i = min_index + lookback
                rows = np.arange(i, min(i + batch_size, max_index))
                i += len(rows)

            samples = np.zeros((len(rows), lookback // step, data.shape[-1]))
            targets = np.zeros((len(rows),))
            for j, row in enumerate(rows):
                indices = range(rows[j] - lookback, rows[j], step)
                samples[j] = data[indices]
                targets[j] = data[rows[j] + delay][target_indx]
            yield samples, targets

    def r2_keras(self, y_true, y_pred):
        """Coefficient of Determination"""
        SS_res = K.sum(K.square(y_true - y_pred))
        SS_tot = K.sum(K.square(y_true - K.mean(y_true)))
        return 1 - SS_res / (SS_tot + K.epsilon())

    def build_model(self):

        model = Sequential()
        model.add(tf.keras.Input(shape=(None, self.df_train_norm.shape[1])))
        model.add(tf.keras.layers.Conv1D(filters=6, kernel_size=5, activation="relu"))
        model.add(LSTM(50, return_sequences=True, activation="relu"))
        model.add(LSTM(50, return_sequences=False, activation="relu"))
        model.add(Dense(1))

        self.model = model
        return model

    def fit_model(self):
        callbacks = [
            EarlyStopping(
                monitor="loss",
                min_delta=0,
                patience=10,
                verbose=2,
                mode="auto",
                restore_best_weights=True,
            ),
            ModelCheckpoint(
                filepath=self.model_path, monitor="val_loss", save_best_only=True
            ),
        ]

        self.model.compile(loss="mae", optimizer="adam", metrics=[self.r2_keras])
        # history = model.fit(train_gen, epochs=50, batch_size=72, validation_data=valid_gen, verbose=2, shuffle=False, use_multiprocessing=True)
        print("Start training")
        history = self.model.fit(
            self.train_gen,
            steps_per_epoch=self.train_steps,
            epochs=70,
            shuffle=False,
            validation_data=self.valid_gen,
            validation_steps=self.val_steps,
            callbacks=callbacks,
            verbose=2,
        )
        print("End training")
    def add_empty_row(self, df, date_time):
        new_row_df = pd.DataFrame(
            columns=df.columns,
            data=[
                [
                    0,
                    np.sin(2 * np.pi * date_time.weekday() / 7),
                    np.cos(2 * np.pi * date_time.weekday() / 7),
                    np.sin(2 * np.pi * date_time.hour / 24),
                    np.cos(2 * np.pi * date_time.hour / 24),
                    np.sin(2 * np.pi * date_time.minute / 60),
                    np.cos(2 * np.pi * date_time.minute / 60),
                ]
            ],
        )
        df = pd.concat([df, new_row_df], ignore_index=True)
        df = df.reset_index(drop=True)
        return df
    def get_forecast_next_steps(
        self,
        left_time_interval=None,
        right_time_interval=None,
        predicted_column="longtime_mean",
    ) -> pd.DataFrame:
        if left_time_interval is None:
            left_time_interval = datetime.now() - timedelta(days=2)
        if right_time_interval is None:
            right_time_interval = datetime.now()

        df_all = self.dataHandler.get_data_for_prediction(
            left_time_interval=left_time_interval,
            right_time_interval=right_time_interval,
            predicted_column=self.predicted_column,
            dropna=False,
        )

        forecast_future = pd.DataFrame()

        current_forecast_begin_date = right_time_interval + timedelta(hours=0.5)
        df_all = self.add_empty_row(df_all, current_forecast_begin_date)
        

        current_forecast_begin_date = right_time_interval + timedelta(hours=0.5)
        # prediction for next 6 hours
        for i in range(0, 12):


            df_all = self.add_empty_row(df_all, current_forecast_begin_date)
            current_forecast_begin_date += timedelta(hours=0.5)
            
            
            df_predict_norm = df_all.copy()
            df_predict_norm[df_all.columns] = self.scaler.transform(df_all)
            # create predict df with values
            predict_gen = self.generator(
                dataframe=df_predict_norm,
                target_name=self.predicted_column,
                lookback=self.lookback,
                delay=self.delay,
                min_index=0,
                max_index=None,
                step=1,
                shuffle=False,
                batch_size=df_predict_norm.shape[0],
            )
 
            (X, y_truth) = next(predict_gen)
            y_pred = self.model.predict(X, verbose=0)

            # np.expand_dims(y_truth,axis=1).shape
            y_pred_inv = np.concatenate(
                (y_pred, np.zeros((y_pred.shape[0], self.num_of_features))), axis=1
            )
            y_pred_inv = self.scaler.inverse_transform(y_pred_inv)

            # get last predicted value
            y_pred_inv = y_pred_inv[-1, :]


            
            df_all.iloc[-2]["longtime_mean"] = y_pred_inv[0]

            # drop first row
            df_all = df_all[1:]

            forecast_future = pd.concat(
                [
                    forecast_future,
                    df_all.iloc[[-2], df_all.columns.get_loc("longtime_mean")],
                ],
                axis=0,
            )
            forecast_future = forecast_future.reset_index(drop=True)


        # create a dataframe with forecast and datetime as index
        self.dataHandler.write_forecast_to_influxdb(
            forecast_future, "prediction_longtime_mean"
        )
        return forecast_future


if __name__ == "__main__":
    dataHandler = DataHandler(
        "localhost",
        "smart_home_formankovi",
        "root",
        "root",
        "shelly1pm_34945475a969",
        "esphome_web_c771e8_tmp3",
    )
    forecast = Forecast(dataHandler)
    forecast.train_model()
    forecast.build_model()
    forecast.fit_model()
    forecast.get_forecast_next_steps(30)
