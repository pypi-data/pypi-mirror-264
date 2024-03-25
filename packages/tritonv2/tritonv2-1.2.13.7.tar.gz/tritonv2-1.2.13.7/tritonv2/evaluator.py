# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
testing.py
"""
import json
import logit
from typing import Optional
import cv2
import ray
import numpy as np
from tritonclient.utils import triton_to_np_dtype
from tritonclient import http as http_client
from windmillmodelv1.client.model_api_model import ModelName, parse_model_name

from server.config import TritonServerConfig
from server.local import TritonServerLocal
from ds_formatter import (
    AnnotationFormatter,
    _update_image_id_byMD5,
    gaeainfer_to_vistudioV1,
)
from utils import list_stack_ndarray
from client_factory import TritonClientFactory


def image_preprocess(path: str, d_type):
    """
    Image preprocess
    :param path:
    :param d_type:
    :return:
    """
    frame = cv2.imread(path)
    img_resize = cv2.resize(frame, (1920, 1080))
    org_h, org_w, _ = img_resize.shape
    img_encode = cv2.imencode(".jpg", img_resize)[1]
    return np.frombuffer(img_encode.tobytes(), dtype=d_type)


def infer(model_name, triton_client, image_id, image_path):
    """
    Infer
    :param model_name:
    :param triton_client:
    :param image_id:
    :param image_path:
    :return:
    """
    input_metadata, output_metadata, batch_size = (
        triton_client.get_inputs_and_outputs_detail(model_name=model_name)
    )

    file_names = [image_path]
    repeated_image_data = []
    for file_path in file_names:
        img = image_preprocess(
            file_path, triton_to_np_dtype(input_metadata[0]["datatype"])
        )
        repeated_image_data.append(np.array(img))

    batched_image_data = list_stack_ndarray(repeated_image_data)

    meta_json = json.dumps({"image_id": image_id})
    byte_meta_json = meta_json.encode()
    np_meta_json = np.frombuffer(byte_meta_json, dtype="uint8")
    send_meta_json = np.array(np_meta_json)
    send_meta_json = np.expand_dims(send_meta_json, axis=0)
    # build triton input
    inputs = [
        http_client.InferInput(
            input_metadata[0]["name"],
            list(batched_image_data.shape),
            input_metadata[0]["datatype"],
        ),
        http_client.InferInput(
            input_metadata[1]["name"],
            send_meta_json.shape,
            input_metadata[1]["datatype"],
        ),
    ]
    inputs[0].set_data_from_numpy(batched_image_data, binary_data=False)
    inputs[1].set_data_from_numpy(send_meta_json)
    # build triton output
    output_names = [output["name"] for output in output_metadata]
    outputs = []
    for output_name in output_names:
        outputs.append(http_client.InferRequestedOutput(output_name, binary_data=True))

    # infer
    result = triton_client.model_infer(model_name, inputs, outputs=outputs)
    # print detailed output
    output_dict = {}
    for output_name in output_names:
        output_dict[output_name] = eval(result.as_numpy(output_name))

    return output_dict["skill_out_json"]


def evaluate(
    model_name: str,
    model_path: str,
    dataset_path: str,
    output_uri: str,
    annotation_format: Optional[str] = "COCO",
    triton_server_extra_args: Optional[dict] = None,
    metric=None,
    windmill_client=None,
):
    """
    Testing
    :param annotation_format:
    :param triton_server_extra_args:
    :param windmill_client:
    :param metric:
    :param model_path:
    :param model_name:
    :param dataset_path:
    :param output_uri:
    :return:
    """

    triton_server_extra_args["model-repository"] = model_path

    triton_server_config = TritonServerConfig().update_config(
        params=triton_server_extra_args
    )

    triton_instance = TritonServerLocal(config=triton_server_config)
    triton_instance.start()

    while True:
        if triton_instance.is_ready():
            break

    logit.info("Triton server is ready")

    triton_client = TritonClientFactory.create_http_client(
        server_url=triton_instance.http_base_uri,
        verbose=True,
    )

    ds = ray.data.read_json(paths=[dataset_path + "/val.json"])
    label_ds = ds.flat_map(lambda row: row["categories"])
    image_ds = ds.flat_map(lambda row: row["images"])
    image_ds = image_ds.add_column("image_id", lambda df: _update_image_id_byMD5(df))

    formatter = AnnotationFormatter(annotation_format, artifact_name=model_name)
    references = formatter.fit(ds).stats_
    with open(dataset_path + "/jsonls/annotation.jsonl", "w") as f:
        for i in references.iter_rows():
            f.write(json.dumps(i) + "\n")

    m_name = parse_model_name(model_name)
    if m_name is None:
        m_name = ModelName(local_name=model_name)

    infer_raw = []
    for image in image_ds.iter_rows():
        infer_dict = infer(
            m_name.local_name, triton_client, image["image_id"], image["file_name"]
        )
        infer_raw.append(infer_dict[0])

    predictions = gaeainfer_to_vistudioV1(infer_raw, model_name)

    with open(dataset_path + "/jsonls/prediction.jsonl", "w") as f:
        for p in predictions:
            f.write(json.dumps(p) + "\n")

    metric(
        predictions=predictions,
        references=references.take_all(),
        output_uri=output_uri,
    )

    logit.info("Evaluation finished, begin to stop Triton server")
    triton_instance.stop()
