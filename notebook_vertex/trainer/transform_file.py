
import tensorflow as tf
import tensorflow_transform as tft





# Features with string data types that will be converted to indices
_VOCAB_FEATURE_DICT = {
    'education': 16, 'marital-status': 7, 'occupation': 15, 'race': 5,
    'relationship': 6, 'workclass': 9, 'sex': 2, 'native-country': 42
}

# Numerical features that are marked as continuous
_NUMERIC_FEATURE_KEYS = ['fnlwgt', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']

# Feature that can be grouped into buckets
_BUCKET_FEATURE_DICT = {'age': 4}

# Number of out-of-vocabulary buckets
_NUM_OOV_BUCKETS = 5

# Feature that the model will predict
_LABEL_KEY = 'label'



 

# Define the transformations
def preprocessing_fn(inputs):
    """tf.transform's callback function for preprocessing inputs.
    Args:
        inputs: map from feature keys to raw not-yet-transformed features.
    Returns:
        Map from string feature key to transformed feature operations.
    """

    # Initialize outputs dictionary
    outputs = {}

    # Scale these features to the range [0,1]
    for key in _NUMERIC_FEATURE_KEYS:
        scaled = tft.scale_to_0_1(inputs[key])
        outputs[key] = tf.reshape(scaled, [-1])

    # Convert strings to indices and convert to one-hot vectors
    for key, vocab_size in _VOCAB_FEATURE_DICT.items():
        indices = tft.compute_and_apply_vocabulary(inputs[key], num_oov_buckets=_NUM_OOV_BUCKETS)
        one_hot = tf.one_hot(indices, vocab_size + _NUM_OOV_BUCKETS)
        outputs[key] = tf.reshape(one_hot, [-1, vocab_size + _NUM_OOV_BUCKETS])

    # Bucketize this feature and convert to one-hot vectors
    for key, num_buckets in _BUCKET_FEATURE_DICT.items():
        indices = tft.bucketize(inputs[key], num_buckets)
        one_hot = tf.one_hot(indices, num_buckets)
        outputs[key] = tf.reshape(one_hot, [-1, num_buckets])

    # Cast label to float
    outputs[_LABEL_KEY] = tf.cast(inputs[_LABEL_KEY], tf.float32)

    return outputs
