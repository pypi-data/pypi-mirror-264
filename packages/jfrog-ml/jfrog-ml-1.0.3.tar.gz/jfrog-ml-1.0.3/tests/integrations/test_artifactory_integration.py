import json
from datetime import datetime
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense
import pytest
import os

from jfrog_ml._log_config import logger
from jfrog_ml.artifactory import Artifactory
from jfrog_ml._storage_utils import calc_sha2


@pytest.fixture
def temp_model_dir(tmpdir):
    return str(tmpdir.mkdir("model_directory"))


@pytest.fixture
def temp_download_dir(tmpdir):
    return str(tmpdir.mkdir("download_directory"))


@pytest.mark.integration
def test_store_load_models(temp_model_dir, temp_download_dir, pytestconfig):
    # setup RT required variables
    rt_host = pytestconfig.getoption('rt_host')
    logger.info('rt_host={}'.format(rt_host))
    repo_name = pytestconfig.getoption('repo_name')
    logger.info('repo_name={}'.format(repo_name))
    rt_token = pytestconfig.getoption('rt_token')

    model = create_and_fit_model()
    positive_text = "This movie is awesome, I enjoyed watching it."
    first_prediction_score = get_prediction_score(model, positive_text)
    assert first_prediction_score >= 0.5

    # Save model locally
    model_name = "sentiment-model"
    model_location = temp_model_dir + '/sentiment_model.h5'
    model.save(model_location)
    model_size = os.path.getsize(model_location)
    model_checksums = calc_sha2(model_location)

    # Store model in Artifactory
    token = rt_token
    configure_client(rt_host=rt_host, token=token)
    model_namespace = "x-space"
    model_name = "xyz-model"
    repo = Artifactory()
    tags = {"tag1": "tag1", "tag2": "tag2"}
    version = repo.upload_model_version(repo_name, model_name, temp_model_dir, model_namespace, tags=tags)

    # Download the model, and verify it is loaded as expected
    repo.download_model_version(repository=repo_name, namespace="x-space", model_name="xyz-model", version=version,
                                target_path=temp_download_dir)

    model_from_rt = tf.keras.models.load_model(f"{temp_download_dir}/sentiment_model.h5")

    # Assert prediction score
    second_prediction_score = get_prediction_score(model_from_rt, positive_text)
    assert second_prediction_score >= 0.5
    assert second_prediction_score == first_prediction_score

    # Assert model-info.json creation
    expected_data = {
        "model_name": model_name,
        "artifacts": [
            {
                "artifact_path": "sentiment_model.h5",
                "size": model_size,
                "checksums": {"sha2": model_checksums}
            }
        ]
    }

    model_info = repo.get_model_info(repository=repo_name, namespace="x-space", model_name="xyz-model", version=version)
    assert_model_info_created(model_info, "created_date")
    assert_model_info_artifact(model_info, expected_data, 0)


def assert_model_info_created(actual_json, date_field):
    def is_valid_date(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
            return True
        except ValueError:
            return False

    assert is_valid_date(actual_json[date_field]), f"Date field '{date_field}' is not in the correct format"


def assert_model_info_artifact(actual_json, expected_json, artifact_index):
    assert expected_json["artifacts"][artifact_index]["size"] == actual_json["artifacts"][artifact_index]["size"]
    assert expected_json["artifacts"][artifact_index]["artifact_path"] == actual_json["artifacts"][artifact_index][
        "artifact_path"]


def create_and_fit_model():
    vocab_size = 10000
    maxlen = 200
    (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=vocab_size)
    # Pad sequences
    x_train = pad_sequences(x_train, maxlen=maxlen)
    # x_test = pad_sequences(x_test, maxlen=maxlen)
    # Build the model
    model = Sequential([
        Embedding(vocab_size, 16, input_length=maxlen),
        GlobalAveragePooling1D(),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    # Train the model
    model.fit(x_train, y_train, epochs=10, batch_size=512, validation_split=0.2)
    return model


def encode_text(text, maxlen=200):
    # Load the IMDb word index
    word_index = imdb.get_word_index()
    # Convert words to integer indices
    tokens = [word_index.get(word, 1) for word in text.lower().split()]
    # Pad sequences
    return pad_sequences([tokens], maxlen=maxlen, padding='post')


def get_prediction_score(model, new_text):
    # Preprocess the new text
    encoded_text = encode_text(new_text)
    # Predict sentiment
    prediction_score = model.predict(encoded_text)
    return prediction_score


@pytest.fixture(scope="session")
def rt_host(pytestconfig):
    return pytestconfig.getoption("rt_host")


@pytest.fixture(scope="session")
def rt_user(pytestconfig):
    return pytestconfig.getoption("rt_user")


@pytest.fixture(scope="session")
def rt_password(pytestconfig):
    return pytestconfig.getoption("rt_password")


def configure_client(rt_host, token):
    os.environ["JFML_URL"] = rt_host + "/artifactory"
    os.environ["JFML_TOKEN"] = token


def preprocess_input(text, tokenizer, maxlen):
    # Tokenize and pad the input text
    sequences = tokenizer.texts_to_sequences([text])
    padded_sequences = pad_sequences(sequences, maxlen=maxlen)
    return padded_sequences
