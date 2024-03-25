# JFrog ML (frogML)

## Table of contents:

- [Overview](#Overview)
- [Build](#Build)
- [Usage](#Usage)

### Overview

JFrog ML (jfrogml) is a smart python client library provides a simple method of storing and downloading models and model
data from the JFrog platform, utilizing the advanced capabilities of the JFrog platform

### Package Build
```
python3 -m build
```
#### Run CI

#### Locally run tests using artifactory docker 

To run the tests, use the ```make test``` command which start an Artifactory container, create a local repository in
it, generate a user token, and runs the test using the generated token

#### Locally run tests using exiting Artifacotry

To run the tests, use the ```pytest``` command pointing it to an existing Artifactory host, select a generic local repository in
, generate a user token or provide user credentials , and runs the test:
```
python3 -m  pytest tests/integrations/test_artifactory_integration.py  --rt_host "<RT host>" --rt_token <token>   --repo_name <generic-repo-name> -s
alternatively use --rt_user <username>  and --rt_password <password> instead of --rt_token
```


### Usage

The below example shows TensorFlow & Keras model upload and download capabilities. The library capabilities are not tied
to a specific framework, different flavors of models can be stored and downloaded similarly

Logs are saved to <user_home>/.frog-ml/frog-ml-log-history.log

Setup client environment variables (available variables and example values):

```angular2html
export JFML_URL=http://ml.jfrog.io/artifactory/ml-local
export JFML_TOKEN=...
export JFML_TIMEOUT=30 (changes timeout for outbound requests to Artifactory)
export JFML_DEBUG=true (sets log level to debug)
```

Import and initialize client

```
from jfrog_ml.artifactory import Artifactory
artifactory = Artifactory()
```

Store model in Artifactory

```
from tensorflow.keras.models import Sequential
model = Sequential(...)
model.save(temp_model_dir + '/sentiment_model.h5')

repo.log_artifacts("my_sentiment_model", temp_model_dir)
```

Load model from Artifactory:

```
repo.download_artifacts("my_sentiment_model", temp_download_dir)
model = tf.keras.models.load_model(temp_download_dir + '/sentiment_model.h5')
```
