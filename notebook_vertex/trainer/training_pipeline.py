import tensorflow as tf
from tfx import v1 as tfx
import kfp
import os

import eval_config

def _create_pipeline(pipeline_name: str, pipeline_root: str, data_root: str,
                     transform_module_file: str, trainer_module_file : str,
                     serving_model_dir: str,
                     metadata_path: str) -> tfx.dsl.Pipeline:
  """Creates pipeline with TFX.""" 

  # Brings data into the pipeline.
  example_gen = tfx.components.CsvExampleGen(input_base=data_root)

  statistics_gen = tfx.components.StatisticsGen(
    examples=example_gen.outputs['examples'])

  schema_gen = tfx.components.SchemaGen(
    statistics=statistics_gen.outputs['statistics'])

  example_validator = tfx.components.ExampleValidator(
    statistics=statistics_gen.outputs['statistics'],
    schema=schema_gen.outputs['schema'])

  transform = tfx.components.Transform(
    examples=example_gen.outputs['examples'],
    schema=schema_gen.outputs['schema'],
    module_file=os.path.abspath(transform_module_file))

  # Uses user-provided Python function that trains a model.
  trainer = tfx.components.Trainer(
    module_file=os.path.abspath(trainer_module_file),
    examples=transform.outputs['transformed_examples'],
    transform_graph=transform.outputs['transform_graph'],
    schema=schema_gen.outputs['schema'],
    train_args=tfx.proto.TrainArgs(num_steps=50),
    eval_args=tfx.proto.EvalArgs(num_steps=50))

  model_resolver = tfx.dsl.Resolver(
      strategy_class=tfx.dsl.experimental.LatestBlessedModelStrategy,
      model=tfx.dsl.Channel(type=tfx.types.standard_artifacts.Model),
      model_blessing=tfx.dsl.Channel(
          type=tfx.types.standard_artifacts.ModelBlessing)).with_id(
              'latest_blessed_model_resolver')

  evaluator = tfx.components.Evaluator(
    examples=example_gen.outputs['examples'],
    model=trainer.outputs['model'],
    baseline_model=model_resolver.outputs['model'],
    eval_config=eval_config)

  # Pushes the model to a filesystem destination.
  pusher = tfx.components.Pusher(
    model=trainer.outputs['model'],
    model_blessing=evaluator.outputs['blessing'],
    push_destination=tfx.proto.PushDestination(
        filesystem=tfx.proto.PushDestination.Filesystem(
            base_directory=serving_model_dir)))

  # Following three components will be included in the pipeline.
  components = [
      example_gen,
      statistics_gen,
      schema_gen,
      example_validator,
      transform,
      trainer,
      model_resolver,
      evaluator,
      pusher,
  ]

  return tfx.dsl.Pipeline(
      pipeline_name=pipeline_name,
      pipeline_root=pipeline_root,
      metadata_connection_config=tfx.orchestration.metadata
      .sqlite_metadata_connection_config(metadata_path),
      components=components)