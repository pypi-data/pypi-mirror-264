# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
formatter.py
"""
import datetime
import hashlib

import pandas as pd
import ray
from ray.data import Preprocessor, Dataset

time_pattern = "%Y-%m-%dT%H:%M:%SZ"


def _update_image_id_byMD5(df: pd.DataFrame) -> "pd.Series":
    """
    update image_id = MD5(row(file_name))
    :param row:
    :return:
    """
    df["image_id"] = df["file_name"].apply(
        lambda x: hashlib.md5(x.encode()).hexdigest()
    )
    image_id_series = df["image_id"].rename("image_id")
    return image_id_series


class AnnotationFormatter(Preprocessor):
    """
    AnnotationFormatter
    """

    def __init__(self, annotation_format, artifact_name: str = ""):
        """
        constructor
        :param annotation_format:
        :param artifact_name:
        """
        self._is_fittable = True
        self._annotation_format = annotation_format
        self._artifact_name = artifact_name

    def _fit(self, ds: "Dataset") -> "Preprocessor":
        """
        _fit
        :param ds:
        :return:
        """
        if self._annotation_format == "COCO":
            final_anno_ds = self._fit_coco(ds)
        # if self._annotation_format == "Gaea":
        #     final_anno_ds = self._fit_gaea(ds)
        self.stats_ = final_anno_ds
        return self

    def _group_by_image_id(self, group: pd.DataFrame) -> pd.DataFrame:
        """
        group bu image_id
        :param group:
        :return:
        """
        image_id = group["image_id"][0]
        ids = group["id"].tolist()
        annoations = list()
        for i in range(len(ids)):
            id = ids[i]
            bbox = group["bbox"].tolist()[i]
            segmentation = group["segmentation"].tolist()[i]
            area = group["area"].tolist()[i]
            cate = group["category_id"].tolist()[i]
            iscrowd = group["iscrowd"].tolist()[i]
            anno = {
                "id": id,
                "bbox": bbox,
                "segmentation": segmentation,
                "area": area,
                "labels": [{"id": cate, "confidence": 1}],
                "iscrowd": iscrowd,
            }
            annoations.append(anno)

        annoation_res = {
            "image_id": image_id,
            "created_at": datetime.datetime.utcnow().strftime(time_pattern),
            "annotations": [annoations],
            "doc_type": "annotation",
            "task_kind": "Manual",
            "artifact_name": self._artifact_name,
            "image_created_at": datetime.datetime.utcnow().strftime(time_pattern),
        }
        return pd.DataFrame(annoation_res)

    def _fit_coco(self, ds: "Dataset") -> "Dataset":
        # 展开 images
        image_ds = ds.flat_map(lambda row: row["images"])

        # 展开 annoations
        annoation_ds = ds.flat_map(lambda row: row["annotations"])

        # merge image_ds and annoation_ds on annoation_ds.image_id = image_ds.id
        drop_id_annotaion_ds = annoation_ds.drop_columns(cols=["id"])
        image_df = image_ds.to_pandas()
        annotation_df = drop_id_annotaion_ds.to_pandas()
        merged_df = pd.merge(annotation_df, image_df, left_on="image_id", right_on="id")
        #
        bboxs = merged_df["bbox"].tolist()
        segmentation = merged_df["segmentation"].tolist()
        normal_bbox_list = [arr.tolist() for arr in bboxs]
        normal_segmentation_list = [arr.tolist() for arr in segmentation]
        merged_df["bbox"] = normal_bbox_list
        merged_df["segmentation"] = normal_segmentation_list
        merged_annotaion_ds = ray.data.from_pandas(merged_df).drop_columns(
            cols=["image_id"]
        )

        # # update image_id to md5(file_name)
        updated_annoation_ds = merged_annotaion_ds.add_column(
            "image_id", lambda df: _update_image_id_byMD5(df)
        )
        droped_annoation_ds = updated_annoation_ds.drop_columns(
            cols=["file_name", "height", "width"]
        )
        # groupby and map_groups
        group_data = droped_annoation_ds.groupby("image_id")
        group_anno_ds = group_data.map_groups(lambda g: self._group_by_image_id(g))
        group_anno_ds = group_anno_ds.drop_columns(cols=["image_id"])

        return group_anno_ds


def gaeainfer_to_vistudioV1(raw_data, artifact_name):
    """
    Convert GaeaInfer format to VistudioV1 format
    :param raw_data:
    :param artifact_name:
    :return:
    """
    # 初始化annotations列表
    annotations_list = []

    # 为每个image_id处理annotations
    for item in raw_data:
        annotations = []
        image_id = item["image_id"]  # 假设这是一个递增的标识符

        for pred in item["predictions"]:
            bbox = pred["bbox"]
            area = pred["area"]
            labels = [
                {"id": category["id"], "confidence": category["confidence"]}
                for category in pred["categories"]
            ]

            annotation = {
                "id": image_id,  # 使用image_id作为annotation的id
                "bbox": bbox,
                "labels": labels,
                "area": area,
            }
            annotations.append(annotation)

        # 将每个图片的annotations加入到最终列表中
        annotations_list.append(
            {
                "doc_type": "annotation",
                "artifact_name": artifact_name,
                "task_kind": "Model",
                "annotations": annotations,
            }
        )

    return annotations_list
