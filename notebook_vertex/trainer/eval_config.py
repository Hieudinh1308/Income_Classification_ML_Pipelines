import tensorflow_model_analysis as tfma

eval_config = tfma.EvalConfig(
    model_specs=[
        # This assumes a serving model with signature 'serving_default'.
        tfma.ModelSpec(
            signature_name='serving_default',
            label_key='label'
            )
        ],
    metrics_specs=[
        tfma.MetricsSpec(
            # The metrics added here are in addition to those saved with the
            # model (assuming either a keras model or EvalSavedModel is used).
            # Any metrics added into the saved model (for example using
            # model.compile(..., metrics=[...]), etc) will be computed
            # automatically.
            # To add validation thresholds for metrics saved with the model,
            # add them keyed by metric name to the thresholds map.
            metrics=[
                tfma.MetricConfig(class_name='ExampleCount'),
                tfma.MetricConfig(class_name='BinaryAccuracy',
                      threshold=tfma.MetricThreshold(
                          value_threshold=tfma.GenericValueThreshold(
                              lower_bound={'value': 0.5}),
                              # Change threshold will be ignored if there is no
                              # baseline model resolved from MLMD (first run).
                              change_threshold=tfma.GenericChangeThreshold(
                                  direction=tfma.MetricDirection.HIGHER_IS_BETTER,
                                  absolute={'value': -1e-10}
                                  )
                              )
                      )
            ]
        )
    ],
    slicing_specs=[
        # An empty slice spec means the overall slice, i.e. the whole dataset.
        tfma.SlicingSpec(),
        # Data can be sliced along a feature column.
        tfma.SlicingSpec(
            feature_keys=['sex']),
        tfma.SlicingSpec(
            feature_keys=['race']),
    ])