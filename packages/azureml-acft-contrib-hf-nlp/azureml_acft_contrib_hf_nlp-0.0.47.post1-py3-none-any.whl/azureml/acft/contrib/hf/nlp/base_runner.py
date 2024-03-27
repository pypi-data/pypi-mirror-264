# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
# Copyright 2020 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ---------------------------------------------------------
"""
Base runner
"""

import os
from abc import ABC, abstractmethod
from collections import OrderedDict
from argparse import Namespace
from pathlib import Path
from typing import Optional

from transformers.models.auto.modeling_auto import (
    MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING_NAMES,
    MODEL_FOR_TOKEN_CLASSIFICATION_MAPPING_NAMES,
    MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING_NAMES,
    MODEL_FOR_QUESTION_ANSWERING_MAPPING_NAMES,
    MODEL_FOR_CAUSAL_LM_MAPPING_NAMES,
)
from transformers import PretrainedConfig

from .nlp_auto.config import AzuremlAutoConfig
from .constants.constants import Tasks

from azureml.acft.accelerator.constants import SaveFileConstants
from azureml.acft.accelerator.utils.checkpoint_utils import get_checkpoint_step
from azureml.acft.common_components.utils.error_handling.exceptions import ACFTValidationException
from azureml.acft.common_components.utils.error_handling.error_definitions import ModelIncompatibleWithTask
from azureml.acft.common_components import get_logger_app
from azureml._common._error_definition.azureml_error import AzureMLError  # type: ignore


logger = get_logger_app(__name__)


TASK_SUPPORTED_MODEL_TYPES_MAP = OrderedDict([
    (Tasks.SINGLE_LABEL_CLASSIFICATION, MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING_NAMES),
    (Tasks.MULTI_LABEL_CLASSIFICATION, MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING_NAMES),
    (Tasks.REGRESSION, MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING_NAMES),
    (Tasks.NAMED_ENTITY_RECOGNITION, MODEL_FOR_TOKEN_CLASSIFICATION_MAPPING_NAMES),
    (Tasks.SUMMARIZATION, MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING_NAMES),
    (Tasks.TRANSLATION, MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING_NAMES),
    (Tasks.QUESTION_ANSWERING, MODEL_FOR_QUESTION_ANSWERING_MAPPING_NAMES),
    (Tasks.TEXT_GENERATION, MODEL_FOR_CAUSAL_LM_MAPPING_NAMES),
    (Tasks.NLP_NER, MODEL_FOR_TOKEN_CLASSIFICATION_MAPPING_NAMES),
    (Tasks.NLP_MULTICLASS, MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING_NAMES),
    (Tasks.NLP_MULTILABEL, MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING_NAMES),
])


ACFT_TASK_AUTO_TASK_MAP = OrderedDict([
    (Tasks.SINGLE_LABEL_CLASSIFICATION, "AutoModelForSequenceClassification"),
    (Tasks.MULTI_LABEL_CLASSIFICATION, "AutoModelForSequenceClassification"),
    (Tasks.NAMED_ENTITY_RECOGNITION, "AutoModelForTokenClassification"),
    (Tasks.QUESTION_ANSWERING, "AutoModelForQuestionAnswering"),
    (Tasks.SUMMARIZATION, "AutoModelForSeq2SeqLM"),
    (Tasks.TRANSLATION, "AutoModelForSeq2SeqLM"),
    (Tasks.TEXT_GENERATION, "AutoModelForCausalLM"),
])


class BaseRunner(ABC):

    def check_model_task_compatibility(self, model_name_or_path: str, task_name: str, **kwargs) -> None:
        """
        Check if the given model supports the given task in the case of Hugging Face Models
        """
        supported_model_types = TASK_SUPPORTED_MODEL_TYPES_MAP[task_name]
        model_type = AzuremlAutoConfig.get_model_type(hf_model_name_or_path=model_name_or_path, **kwargs)

        if model_type not in supported_model_types:
            config_dict, _ = PretrainedConfig.get_config_dict(model_name_or_path, **kwargs)
            if "auto_map" in config_dict and ACFT_TASK_AUTO_TASK_MAP[task_name] in config_dict["auto_map"]:
                logger.info(
                    f"Task {task_name} is supported with external class - "
                    f"{config_dict['auto_map'][ACFT_TASK_AUTO_TASK_MAP[task_name]]}"
                )
            else:
                raise ACFTValidationException._with_error(
                    AzureMLError.create(
                        ModelIncompatibleWithTask, TaskName=task_name, ModelName=model_name_or_path
                    )
                )

    def resolve_resume_from_checkpoint(self, component_plus_preprocess_args: Namespace) -> None:
        """
        Resolve resume_from_checkpoint path to allow Auto-resuming from checkpoint in case of singularity preemption.
        """
        resume_from_checkpoint = None
        if component_plus_preprocess_args.resume_from_checkpoint:
            last_valid_checkpoint = self._get_last_valid_checkpoint(component_plus_preprocess_args.pytorch_model_folder)
            if last_valid_checkpoint:
                logger.info(f"Found a valid checkpoint in pytorch_model_folder: {last_valid_checkpoint}")
                resume_from_checkpoint = last_valid_checkpoint
            else:
                logger.info("No valid checkpoint found in pytorch_model_folder. Will not resume from checkpoint")
        logger.info(f"Set resume_from_checkpoint path to: {resume_from_checkpoint}")
        component_plus_preprocess_args.resume_from_checkpoint = resume_from_checkpoint

    def _get_last_valid_checkpoint(self, pytorch_model_folder: Path) -> Optional[str]:
        """
        Get the last (latest) checkpoint from pytorch_model_folder that contains checkpoint_done.txt
        checkpoint_done.txt marks whether a checkpoint is safe to use.
        """
        contents = os.listdir(pytorch_model_folder)
        logger.info(f"pytorch_model_folder contents: {contents}")
        checkpoint_steps = []
        for name in contents:
            checkpoint_step = get_checkpoint_step(name)
            if Path(pytorch_model_folder, name).is_dir() and checkpoint_step is not None:
                checkpoint_steps.append(checkpoint_step)
        for checkpoint_step in sorted(checkpoint_steps, reverse=True):
            checkpoint_path = Path(pytorch_model_folder, f"checkpoint-{checkpoint_step}")
            checkpoint_done_filepath = checkpoint_path / SaveFileConstants.CHECKPOINT_DONE_PATH
            logger.info(f"Checking if {SaveFileConstants.CHECKPOINT_DONE_PATH} exists: {checkpoint_done_filepath}")
            if checkpoint_done_filepath.exists():
                return str(checkpoint_path)

    @abstractmethod
    def run_preprocess_for_finetune(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def run_finetune(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def run_preprocess_for_infer(self, *args, **kwargs) -> None:
        pass

    def run_modelselector(self, **kwargs) -> None:
        """
        Downloads model from azureml-preview registry if present
        Prepares model for continual finetuning
        Save model selector args
        """
        pass
