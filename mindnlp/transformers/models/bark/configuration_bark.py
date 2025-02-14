# Copyright 2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""
Bark config
"""
import os
from typing import Dict, Optional, Union
from mindspore import log as logger

from ...configuration_utils import PretrainedConfig
from ..auto import CONFIG_MAPPING



BARK_PRETRAINED_CONFIG_ARCHIVE_MAP = {
    "bark":       "https://huggingface.co/bark/resolve/main/config.json",
    "bark_small": "https://huggingface.co/bark_small/resolve/main/config.json",
}

__all__ = ["BarkSubModelConfig", "BarkConfig", "BarkSemanticConfig", "BarkCoarseConfig", "BarkFineConfig"]

class BarkSubModelConfig(PretrainedConfig):
    r"""
    BarkSubModelConfig
    """
    model_type = "bark_module"
    keys_to_ignore_at_inference = ["past_key_values"]

    attribute_map = {
        "num_attention_heads": "num_heads",
        "num_hidden_layers": "num_layers",
        "vocab_size": "input_vocab_size",
        "window_size": "block_size",
    }

    def __init__(
        self,
        block_size=1024,
        input_vocab_size=10_048,
        output_vocab_size=10_048,
        num_layers=12,
        num_heads=12,
        hidden_size=768,
        dropout=0.1,
        bias=True,  # True: bias in Linears and LayerNorms, like GPT-2. False: a bit better and faster
        initializer_range=0.02,
        use_cache=True,
        **kwargs,
    ):
        self.block_size = block_size
        self.input_vocab_size = input_vocab_size
        self.output_vocab_size = output_vocab_size
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.hidden_size = hidden_size
        self.dropout = dropout
        self.bias = bias
        self.use_cache = use_cache
        self.initializer_range = initializer_range

        super().__init__(**kwargs)

    @classmethod
    def from_pretrained(
        cls,
        pretrained_model_name_or_path: Union[str, os.PathLike],
        cache_dir: Optional[Union[str, os.PathLike]] = None,
        force_download: bool = False,
        local_files_only: bool = False,
        **kwargs,
    ) -> "PretrainedConfig":
        kwargs["cache_dir"] = cache_dir
        kwargs["force_download"] = force_download
        kwargs["local_files_only"] = local_files_only


        config_dict, kwargs = cls.get_config_dict(pretrained_model_name_or_path, **kwargs)

        # get the config dict if we are loading from Bark
        if config_dict.get("model_type") == "bark":
            config_dict = config_dict[f"{cls.model_type}_config"]

        if "model_type" in config_dict and hasattr(cls, "model_type") and config_dict["model_type"] != cls.model_type:
            logger.warning(
                f"You are using a model of type {config_dict['model_type']} to instantiate a model of type "
                f"{cls.model_type}. This is not supported for all configurations of models and can yield errors."
            )

        return cls.from_dict(config_dict, **kwargs)


class BarkSemanticConfig(BarkSubModelConfig):
    r"""
    BarkSemanticConfig
    """
    model_type = "semantic"

class BarkCoarseConfig(BarkSubModelConfig):
    r"""
    BarkCoarseConfig
    """
    model_type = "coarse_acoustics"

class BarkFineConfig(BarkSubModelConfig):
    r"""
    BarkFineConfig
    """
    model_type = "fine_acoustics"

    def __init__(self, tie_word_embeddings=True, n_codes_total=8, n_codes_given=1, **kwargs):
        self.n_codes_total = n_codes_total
        self.n_codes_given = n_codes_given

        super().__init__(tie_word_embeddings=tie_word_embeddings, **kwargs)

class BarkConfig(PretrainedConfig):
    """
    This is the configuration class to store the configuration of a [`BarkModel`]. It is used to instantiate a Bark
    model according to the specified sub-models configurations, defining the model architecture.

    Instantiating a configuration with the defaults will yield a similar configuration to that of the Bark
    [suno/bark](https://huggingface.co/suno/bark) architecture.

    Configuration objects inherit from [`PretrainedConfig`] and can be used to control the model outputs. Read the
    documentation from [`PretrainedConfig`] for more information.

    Args:
    semantic_config ([`BarkSemanticConfig`], *optional*):
        Configuration of the underlying semantic sub-model.
    coarse_acoustics_config ([`BarkCoarseConfig`], *optional*):
        Configuration of the underlying coarse acoustics sub-model.
    fine_acoustics_config ([`BarkFineConfig`], *optional*):
        Configuration of the underlying fine acoustics sub-model.
    codec_config ([`AutoConfig`], *optional*):
        Configuration of the underlying codec sub-model.

    Example:

    ```python
    >>> from transformers import (
    ...     BarkSemanticConfig,
    ...     BarkCoarseConfig,
    ...     BarkFineConfig,
    ...     BarkModel,
    ...     BarkConfig,
    ...     AutoConfig,
    ... )

    >>> # Initializing Bark sub-modules configurations.
    >>> semantic_config = BarkSemanticConfig()
    >>> coarse_acoustics_config = BarkCoarseConfig()
    >>> fine_acoustics_config = BarkFineConfig()
    >>> codec_config = AutoConfig.from_pretrained("facebook/encodec_24khz")


    >>> # Initializing a Bark module style configuration
    >>> configuration = BarkConfig.from_sub_model_configs(
    ...     semantic_config, coarse_acoustics_config, fine_acoustics_config, codec_config
    ... )

    >>> # Initializing a model (with random weights)
    >>> model = BarkModel(configuration)

    >>> # Accessing the model configuration
    >>> configuration = model.config
    ```
    """

    model_type = "bark"

    def __init__(
        self,
        semantic_config: Dict = None,
        coarse_acoustics_config: Dict = None,
        fine_acoustics_config: Dict = None,
        codec_config: Dict = None,
        initializer_range=0.02,
        **kwargs,
    ):
        if semantic_config is None:
            semantic_config = {}
            logger.info("semantic_config is None. initializing the semantic model with default values.")

        if coarse_acoustics_config is None:
            coarse_acoustics_config = {}
            logger.info("coarse_acoustics_config is None. initializing the coarse model with default values.")

        if fine_acoustics_config is None:
            fine_acoustics_config = {}
            logger.info("fine_acoustics_config is None. initializing the fine model with default values.")

        if codec_config is None:
            codec_config = {}
            logger.info("codec_config is None. initializing the codec model with default values.")

        self.semantic_config = BarkSemanticConfig(**semantic_config)
        self.coarse_acoustics_config = BarkCoarseConfig(**coarse_acoustics_config)
        self.fine_acoustics_config = BarkFineConfig(**fine_acoustics_config)
        codec_model_type = codec_config["model_type"] if "model_type" in codec_config else "encodec"
        self.codec_config = CONFIG_MAPPING[codec_model_type](**codec_config)

        self.initializer_range = initializer_range

        super().__init__(**kwargs)

    @classmethod
    def from_sub_model_configs(
        cls,
        semantic_config: BarkSemanticConfig,
        coarse_acoustics_config: BarkCoarseConfig,
        fine_acoustics_config: BarkFineConfig,
        codec_config: PretrainedConfig,
        **kwargs,
    ):
        r"""
        Instantiate a [`BarkConfig`] (or a derived class) from bark sub-models configuration.

        Returns:
            [`BarkConfig`]: An instance of a configuration object
        """
        return cls(
            semantic_config=semantic_config.to_dict(),
            coarse_acoustics_config=coarse_acoustics_config.to_dict(),
            fine_acoustics_config=fine_acoustics_config.to_dict(),
            codec_config=codec_config.to_dict(),
            **kwargs,
        )
