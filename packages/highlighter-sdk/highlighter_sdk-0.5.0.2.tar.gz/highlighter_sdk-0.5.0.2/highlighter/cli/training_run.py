import json
from pathlib import Path
from typing import Dict, List, Optional

import click
import yaml
from pydantic import BaseModel

from highlighter.aws_s3 import upload_file_to_s3
from highlighter.base_models import (ExperimentResult,
                                               TrainingRunArtefactType,
                                               TrainingRunArtefactTypeEnum,
                                               TrainingRunType)
from highlighter.cli.common import _to_pathlib
from highlighter.const import DEPRECATED_CAPABILITY_IMPLEMENTATION_FILE
from highlighter.training_config import MetricType
from highlighter.training_runs import \
    get_latest_training_run_artefact


def load_config(cfg_path: Optional[Path]) -> Dict:
    if cfg_path is None:
        return {}

    loaders = {
        ".yaml": yaml.safe_load,
        ".json": json.load,
    }

    with cfg_path.open("r") as f:
        cfg = loaders[cfg_path.suffix](f)

    if cfg.get("parameters", {}).get("cropper", {}).get("scale", 1.0) != 1.0:
        raise ValueError(
            "Got'cha!!!, Dont push an artefact with "
            "cropping scale other than 1.0 or remove from dict"
        )

    return cfg


@click.group("training-run")
@click.pass_context
def training_run_group(ctx):
    pass


@training_run_group.group("artefact")
@click.pass_context
def artefact_group(ctx):
    pass


@artefact_group.command("read")
@click.option(
    "-i",
    "--id",
    type=str,
    required=True,
)
@click.option(
    "-s",
    "--save-path",
    type=click.Path(file_okay=True, writable=True),
    required=True,
    callback=_to_pathlib,
)
@click.option(
    "-a",
    "--artefact-type",
    type=click.Choice(
        list(TrainingRunArtefactTypeEnum.__members__.keys())
        + [DEPRECATED_CAPABILITY_IMPLEMENTATION_FILE]
    ),
    required=True,
)
@click.pass_context
def read_artefact(ctx, id, save_path, artefact_type):
    client = ctx.obj["client"]

    artefact = get_latest_training_run_artefact(
        client,
        id,
        download_file_url=True,
        file_url_save_path=save_path,
        filter_by_artefact_type=artefact_type,
    )
    artefact_yaml_path = save_path.parent / f"{artefact.id}.yaml"
    artefact.dump_yaml(artefact_yaml_path)
    click.echo(f"{artefact}")


@artefact_group.command("create")
@click.option(
    "-i",
    "--id",
    type=str,
    required=True,
    help="training run id",
)
@click.option(
    "-a",
    "--artefact-yaml",
    type=click.Path(file_okay=True, dir_okay=False, exists=True),
    required=True,
    callback=_to_pathlib,
    help=".yaml file base_model.py:TrainingRunArtefactType",
)
@click.pass_context
def create_artefact(ctx, id, artefact_yaml):
    """Create an artefact for a training run and upload artefact-yaml.fileUrl to s3.

    \b
    Fields in artefact.yaml:
    - fileUrl: should contain the absolute path to the checkpoint file you want to upload.
    - type: [REQUIRED] one of OnnxOpset11, OnnxOpset14, OnnxRuntimeAmd64, OnnxRuntimeArm, TorchScriptV1
    - checkpoint: path to checkpoint in file
    - inferenceConfig: [REQUIRED] inference configuration in json format
    - trainingConfig: [REQUIRED] training configuration in json format

    \b
    # artefact.yaml
    fileUrl: /home/users/rick/checkpoint.onnx14
    type: OnnxOpset14
    inferenceConfig: {}
    trainingConfig: {}
    """
    client = ctx.obj["client"]

    artefact: TrainingRunArtefactType = TrainingRunArtefactType.from_yaml(artefact_yaml)

    artefact_file_data = upload_file_to_s3(
        client,
        artefact.fileUrl,
        mimetype="application/octet-stream",
    )
    print(f"Created file in s3:\n{artefact_file_data}")

    class _TrainingRunArtefactType(BaseModel):
        id: str

    class CreateTrainingRunPayload(BaseModel):
        errors: List[str]
        trainingRunArtefact: Optional[_TrainingRunArtefactType]

    artefact_result = client.createTrainingRunArtefact(
        return_type=CreateTrainingRunPayload,
        trainingRunId=id,
        type=artefact.type,
        checkpoint=artefact.checkpoint,
        fileData=artefact_file_data,
        inferenceConfig=artefact.inferenceConfig,
        trainingConfig=artefact.trainingConfig,
    )
    print(f"create artefact result: {artefact_result}")

    create_capability_for_artefact(
        client=client,
        artefact_id=artefact_result.trainingRunArtefact.id,
        training_run_id=id,
        inference_config=artefact.inferenceConfig,
    )


@training_run_group.command("create")
@click.option(
    "-eid",
    "--evaluation-id",
    type=str,
    required=True,
)
@click.option(
    "-eid",
    "--experiment-id",
    type=str,
    required=True,
)
@click.option(
    "-mid",
    "--capability-id",
    type=str,
    required=True,
)
@click.option(
    "-pid",
    "--workflow-id",
    type=str,
    required=True,
)
@click.option(
    "-n",
    "--name",
    type=str,
    required=True,
)
@click.option(
    "--source-code-url",
    type=str,
    required=False,
)
@click.option(
    "--source-code-commit-hash",
    type=str,
    required=False,
)
@click.option(
    "--training-log-archive",
    type=click.Path(dir_okay=False),
    callback=_to_pathlib,
    required=False,
)
@click.pass_context
def create_training_run(
    ctx,
    evaluation_id,
    experiment_id,
    capability_id,
    workflow_id,
    name,
    source_code_url,
    source_code_commit_hash,
    training_log_archive,
):

    client = ctx.obj["client"]

    class CreateTrainingRunPayload(BaseModel):
        errors: List[str]
        trainingRun: TrainingRunType

    training_logs_file_data = None
    if training_log_archive is not None:
        training_logs_file_data = upload_file_to_s3(
            client,
            training_log_archive,
        )
        print(f"Created file in s3:\n{training_logs_file_data}")

    result = client.createTrainingRun(
        return_type=CreateTrainingRunPayload,
        researchPlanId=evaluation_id,
        experimentId=experiment_id,
        modelId=model_id,
        projectId=workflow_id,
        name=name,
        sourceCodeUrl=source_code_url,
        sourceCodeCommitHash=source_code_commit_hash,
        trainingLogsFileData=training_logs_file_data,
    )
    print(result.trainingRun.id)


@training_run_group.group("metrics-result")
@click.pass_context
def metrics_result_group(ctx):
    pass


@metrics_result_group.command("create")
@click.option(
    "-m",
    "--metrics-json-path",
    type=click.Path(dir_okay=False),
    required=True,
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False),
    required=False,
    help="File to output results (yaml), otherwise print to screen (json)",
)
@click.pass_context
def create_metrics_result(
    ctx,
    metrics_json_path,
    output,
):
    """Create a metric result for a training run."""
    client = ctx.obj["client"]

    metric: MetricType = MetricType.from_yaml(metrics_json_path)

    class CreateExperimentResultPayload(BaseModel):
        errors: List[str]
        experimentResult: Optional[ExperimentResult]

    result = client.createExperimentResult(
        return_type=CreateExperimentResultPayload,
        researchPlanId=metric.researchPlanId,
        experimentId=metric.experimentId,
        researchPlanMetricId=metric.researchPlanMetricId,
        result=metric.result,
        objectClassUuid=metric.objectClassUuid,
        occuredAt=metric.occuredAt,
    ).dict()

    if output:
        with open(output, "w") as f:
            yaml.dump(result, f)
    else:
        print(json.dumps(result))
