"""
 Copyright (c) 2022, salesforce.com, inc.
 All rights reserved.
 SPDX-License-Identifier: BSD-3-Clause
 For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
"""

import os
from multimodal_eval_main.models.VPGTrans.lavis.common.registry import registry

from multimodal_eval_main.models.VPGTrans.lavis.datasets.builders.base_dataset_builder import BaseDatasetBuilder
from multimodal_eval_main.models.VPGTrans.lavis.datasets.datasets.image_text_pair_datasets import ImageTextPairDataset
from multimodal_eval_main.models.VPGTrans.lavis.datasets.datasets.laion_dataset import LaionDataset, LaionCOCODataset
from multimodal_eval_main.models.VPGTrans.lavis.datasets.datasets.self_instruct_caption import CCSBUAlignDataset
@registry.register_builder("minigpt4_self_instruct_caption")
class MiniGPT4Builder(BaseDatasetBuilder):
    train_dataset_cls = CCSBUAlignDataset

    DATASET_CONFIG_DICT = {
        "default": "configs/datasets/minigpt4/align.yaml",
    }

    def build_datasets(self):
        # at this point, all the annotations and image/videos should be all downloaded to the specified locations.
        self.build_processors()

        build_info = self.config.build_info
        storage_path = build_info.storage

        datasets = dict()

        # create datasets
        dataset_cls = self.train_dataset_cls
        datasets['train'] = dataset_cls(
            vis_processor=self.vis_processors["train"],
            text_processor=self.text_processors["train"],
            vis_root=os.path.join(storage_path, "image"),
            ann_paths=[os.path.join(storage_path, 'filter_cap.json')],)
        return datasets


@registry.register_builder("conceptual_caption_3m")
class ConceptualCaption3MBuilder(BaseDatasetBuilder):
    train_dataset_cls = ImageTextPairDataset

    DATASET_CONFIG_DICT = {
        "default": "configs/datasets/conceptual_caption/defaults_3m.yaml"
    }


@registry.register_builder("conceptual_caption_12m")
class ConceptualCaption12MBuilder(BaseDatasetBuilder):
    train_dataset_cls = ImageTextPairDataset

    DATASET_CONFIG_DICT = {
        "default": "configs/datasets/conceptual_caption/defaults_12m.yaml"
    }


@registry.register_builder("sbu_caption")
class SBUCaptionBuilder(BaseDatasetBuilder):
    train_dataset_cls = ImageTextPairDataset

    DATASET_CONFIG_DICT = {"default": "configs/datasets/sbu_caption/defaults.yaml"}


@registry.register_builder("vg_caption")
class VGCaptionBuilder(BaseDatasetBuilder):
    train_dataset_cls = ImageTextPairDataset

    DATASET_CONFIG_DICT = {"default": "configs/datasets/vg/defaults_caption.yaml"}


@registry.register_builder("laion2B_multi")
class Laion2BMultiBuilder(BaseDatasetBuilder):
    train_dataset_cls = LaionDataset

    DATASET_CONFIG_DICT = {"default": "configs/datasets/laion/defaults_2B_multi.yaml"}

    def _download_ann(self):
        pass

    def _download_vis(self):
        pass

    def build(self):
        self.build_processors()

        build_info = self.config.build_info

        datasets = dict()
        split = "train"  # laion dataset only has train split

        # create datasets
        # [NOTE] return inner_datasets (wds.DataPipeline)
        dataset_cls = self.train_dataset_cls
        datasets[split] = dataset_cls(
            vis_processor=self.vis_processors[split],
            text_processor=self.text_processors[split],
            location=build_info.storage,
        ).inner_dataset

        return datasets

@registry.register_builder("laion_coco")
class Laion2BMultiBuilder(BaseDatasetBuilder):
    train_dataset_cls = LaionCOCODataset

    DATASET_CONFIG_DICT = {"default": "configs/datasets/laion/defaults_coco.yaml"}

    def _download_ann(self):
        pass

    def _download_vis(self):
        pass

    def build(self):
        self.build_processors()

        build_info = self.config.build_info

        datasets = dict()
        split = "train"  # laion dataset only has train split

        # create datasets
        # [NOTE] return inner_datasets (wds.DataPipeline)
        dataset_cls = self.train_dataset_cls
        datasets[split] = dataset_cls(
            vis_processor=self.vis_processors[split],
            text_processor=self.text_processors[split],
            location=build_info.storage,
        ).inner_dataset

        return datasets