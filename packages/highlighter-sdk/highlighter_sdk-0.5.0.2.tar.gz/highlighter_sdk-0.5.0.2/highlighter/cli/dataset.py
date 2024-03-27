import click
import yaml
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from pathlib import Path
from highlighter.cli.common import CommonOptions
from highlighter.io import multithread_graphql_file_download
from highlighter import (
        get_latest_assessments_gen,
        DatasetSubmissionTypeConnection,
        )

from highlighter.pagination import DEFAULT_PAGE_SIZE
from highlighter.datasets import (
        read_dataset_from_highlighter,
        CocoWriter,
        Dataset,
        get_reader,
        DatasetFormat,
        )
from highlighter.splits import (
        get_split_fn,
        SUPPORTED_SPLIT_FNS,
        )



def _download_data_files(ctx, dataset, data_file_dir):
    if data_file_dir is not None:
        client = ctx.obj["client"]
        multithread_graphql_file_download(
                client,
                list(dataset.data_files_df.data_file_id.unique()),
                data_file_dir,
                )


@click.group("dataset")
@click.pass_context
def dataset_group(ctx):
    pass


@dataset_group.command("create",
        help="""
Create a Dataset in Highlighter

\b
Note: If using the --dataset-id param. There are no safety rails! That is to
say; the cli will allow duplicate assessments and data_files if you ask it to.

  ie: If dataset 123 has data_file 456 and workflow 789 also has data_file 456 the
  assessments for both will be added to the dataset.

Typically you would use the --dataset-id param if you wanted to combine 2 or
more datasets, or combine some new data from a workflow with an existing dataset.
In which case a new dataset would be created that simply has all assessments
appended together.
        """)
@click.option("-n", "--name",
        type=str, required=True,
        )
@click.option("-pid", "--workflow-id",
        type=int, required=False, default=None, multiple=True,
        )
@click.option("-oid", "--object-class-id",
        type=int, required=False, default=None, multiple=True,
        )
@click.option("-uid", "--user-id",
        type=int, required=False, default=None, multiple=True,
        )
@click.option("-did", "--dataset-id",
        type=int, required=False, default=None, multiple=True,
        help = (
            "Add assessments from existing dataset(s), see Note in help string "
            " for more context and a warrning."
            )
        )
@click.option("--split-type",
        type=click.Choice(SUPPORTED_SPLIT_FNS.keys()), required=False,
        default="random_split", show_default=True,
        )
@click.option("--split-seed",
        type=int, required=False, default=42,
        show_default=True,
        )
@click.option("--split-frac",
        type=click.Tuple([str, float]), required=False, multiple=True,
        default=[("data", 1.0)], show_default=True,
        )
@click.pass_context
def create(
        ctx,
        name,
        workflow_id,
        object_class_id,
        user_id,
        dataset_id,
        split_type,
        split_seed,
        split_frac,
        ):
    client = ctx.obj["client"]

    query_args = dict(
            projectId=workflow_id,
            objectClassId=object_class_id,
            userId=user_id,
            )
    def not_empty(v):
        if v is None:
            return False
        if v == ():
            return False
        if v == []:
            return False
        return True

    query_args = {k: v for k, v in query_args.items() if not_empty(v)}

    datasets = []
    if query_args:
        latest_subs_gen = get_latest_assessments_gen(
                client,
                **query_args,
                )

        reader = get_reader("highlighter_assessments")(latest_subs_gen)
        ds = Dataset.load_from_reader(reader)
        datasets.append(ds)


    dataset_description_fields = []
    if dataset_id:
        # add to query_args here because datasetId is not a valid
        # arg to get_latest_assessments_gen, but we still want it
        # to appear in the Highlighter Dataset description.
        query_args["datasetId"] = dataset_id
        dataset_list = [
                Dataset.read_from(
                    dataset_format=DatasetFormat.HIGHLIGHTER_DATASET,
                    client=client,
                    dataset_id=ds_id,
                    page_size=DEFAULT_PAGE_SIZE) for ds_id in dataset_id]

        datasets.extend(dataset_list)

        def get_dataset_url(id, client=client):
            return client.endpoint_url.replace("graphql", f"datasets/{id}")

        def get_dataset_name(id, client=client):

            class DatasetNameOnly(BaseModel):
                name: str

            name = client.dataset(
                    return_type=DatasetNameOnly,
                    id=id,
                    ).name
            return name.replace('_', '\\_')

        base_dataset_links = [
                f"  - [{id}]({get_dataset_url(id)}): {get_dataset_name(id)}"
                for id in dataset_id
                ]
        base_dataset_links_str = "\n".join(base_dataset_links)
        dataset_description_fields.append(
                ("Base Datasets", base_dataset_links_str)
                )



    dataset = Dataset.combine(datasets)

    split_fn = get_split_fn(split_type)
    split_names = [s[0] for s in split_frac]
    fracs = [s[1] for s in split_frac]
    split_args = dict(
            seed=split_seed,
            fracs=fracs,
            names=split_names,
            )
    dataset.apply_split(split_fn, split_args)

    split_args["type"] = split_fn.__name__
    split_str = yaml.safe_dump(split_args)
    split_str = f"<pre>" + split_str + "</pre> \n"

    query_str = yaml.safe_dump(query_args)
    query_str = f"<pre>" + query_str + "</pre> \n"

    # List of tuples with e[0] being the heading and e[1]
    # being the content. This will be rendered as Markdown
    # in the publish_to_highlighter function.
    dataset_description_fields.extend([
            ("Query", query_str),
            ("Split", split_str),
            ])

    dataset.publish_to_highlighter(
            client,
            name,
            dataset_description_fields=dataset_description_fields,
            split_fracs={s: f for s, f in zip(split_names, fracs)},
            )


@click.group("read")
@click.option(
        "-i",
        "--dataset-ids",
        type=int,
        required=False,
        multiple=True,
        default=[],
        show_default=True,
        )
@click.option(
        "--page-size",
        type=int,
        required=False,
        default=DEFAULT_PAGE_SIZE,
        show_default=True,
        )
@click.pass_context
def read_group(ctx, dataset_ids, page_size):
    ctx.obj["dataset_ids"] = list(dataset_ids)
    ctx.obj["page_size"] = page_size

@read_group.command("hdf")
@CommonOptions.annotations_dir
@CommonOptions.data_file_dir
@click.pass_context
def read_hdf(ctx, annotations_dir, data_file_dir):
    client = ctx.obj["client"]
    page_size = ctx.obj["page_size"]

    for dataset_id in ctx.obj["dataset_ids"]:
        ds = Dataset.read_from(
                dataset_format=DatasetFormat.HIGHLIGHTER_DATASET,
                client=client,
                dataset_id=dataset_id,
                page_size=page_size)
        hdf_path = annotations_dir / f"{dataset_id}.hdf"
        ds.write_hdf(hdf_path)
        _download_data_files(ctx, ds, data_file_dir)

@read_group.command(CocoWriter.format_name)
@CommonOptions.annotations_dir
@CommonOptions.data_file_dir
@click.pass_context
def read_coco(ctx, annotations_dir, data_file_dir):
    client = ctx.obj["client"]
    page_size = ctx.obj["page_size"]

    for dataset_id in ctx.obj["dataset_ids"]:
        ds = Dataset.read_from(
                dataset_format=DatasetFormat.HIGHLIGHTER_DATASET,
                client=client,
                dataset_id=dataset_id,
                page_size=page_size)

        writer = CocoWriter(annotations_dir / f"{dataset_id}_splits")
        writer.write(ds)
        _download_data_files(ctx, ds, data_file_dir)


read_group.add_command(read_hdf)
read_group.add_command(read_coco)
dataset_group.add_command(read_group)
