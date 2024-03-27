# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import json
from pathlib import Path
from typing import Dict, Any

from transformers.modeling_utils import PreTrainedModel
from transformers.tokenization_utils_base import PreTrainedTokenizerBase
from transformers.deepspeed import is_deepspeed_zero3_enabled

import torch
import deepspeed

from azureml.acft.common_components import get_logger_app
from azureml.acft.accelerator.finetune import AzuremlFinetuneArgs

from ....constants.constants import SaveFileConstants


logger = get_logger_app(__name__)


class FinetuneBase:
    def _save_mininum_finetune_args(self, finetune_args: AzuremlFinetuneArgs):
        """
        model_selector component reads model_name from finetune_args.json if resume_from_checkpoint=true.
        In case of pre-emption, finetune_args.json will not be found since it's saved after training is successful.
        Here we save a bare-minimum finetune_args.json before the training starts.
        """
        if finetune_args.trainer_args.should_save:
            finetune_args_path = Path(self.finetune_params["pytorch_model_folder"], SaveFileConstants.FINETUNE_ARGS_SAVE_PATH)
            params = {"model_name": self.finetune_params["model_name"]}
            with open(finetune_args_path, 'w') as rptr:
                json.dump(params, rptr, indent=2)

    @classmethod
    def _check_if_vocab_size_changed(cls, model: PreTrainedModel, tokenizer: PreTrainedTokenizerBase) -> bool:
        """Check if the vocabulary size changed due to the added pad token.

        :param model: HuggingFace Pretrained model.
        :type model: PreTrainedModel
        :param tokenizer: HuggingFace Tokenizer
        :type tokenizer: PreTrainedTokenizerBase
        :param return True if vocab size changed else return False
        :rtype boolean
        """
        old_embeddings = model.get_input_embeddings()
        if is_deepspeed_zero3_enabled():
            with deepspeed.zero.GatheredParameters(old_embeddings.weight, modifier_rank=0):
                old_num_tokens, _ = old_embeddings.weight.size()
        else:
            old_num_tokens, _ = old_embeddings.weight.size()

        return old_num_tokens != len(tokenizer)

    @classmethod
    def resize_token_embeddings_and_reset_pad_token_embedding(
        cls, model: PreTrainedModel, tokenizer: PreTrainedTokenizerBase, token_resize_kwargs: Dict[str, Any]
    ) -> None:
        """
        Resizes token embeddings and reset embedding of pad token index.

        :param model: HuggingFace Pretrained model.
        :type model: PreTrainedModel
        :param tokenizer: HuggingFace Tokenizer
        :type tokenizer: PreTrainedTokenizerBase
        :param token_resize_kwargs: kwargs used for resizing token embeddings. For example, pad_to_a_multiple_of
          is one possible key.
        :type token_resize_kwargs: Dict[str, Any]
        """
        # resize token embeddings in case pad token is added
        model.config.pad_token_id = tokenizer.pad_token_id
        logger.info(f"Setting the model config pad token id to {model.config.pad_token_id}")

        # resize embeddings only when the vocab size changed
        if cls._check_if_vocab_size_changed(model, tokenizer):
            logger.info("Calling resize token embeddings")
            model.resize_token_embeddings(len(tokenizer), **token_resize_kwargs)
            model.get_input_embeddings().padding_idx = tokenizer.pad_token_id
            # in case of deepspeed stage3, the model tensors are dummy as they are distributed.
            # in order to modify the tensors, we need to gather the parameters using deepspeed.zero
            # GatherParameters and then modify them.
            if is_deepspeed_zero3_enabled():
                input_embeddings = model.get_input_embeddings()
                with deepspeed.zero.GatheredParameters([input_embeddings.weight], modifier_rank=0):
                    with torch.no_grad():
                        input_embeddings.weight[tokenizer.pad_token_id] = torch.zeros(input_embeddings.weight.shape[1])
            else:
                model.get_input_embeddings()._fill_padding_idx_with_zero()
