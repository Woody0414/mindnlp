# coding=utf-8
# Copyright 2021 The Eleuther AI and HuggingFace Inc. team. All rights reserved.
# Copyright 2023 Huawei Technologies Co., Ltd

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
# ============================================================================
"""
Codegen Model init
"""
from . import codegen, codegen_config, tokenization_codegen, tokenization_codegen_fast

from .codegen import *
from .codegen_config import *
from .tokenization_codegen import *
from .tokenization_codegen_fast import *

__all__ = []
__all__.extend(codegen.__all__)
__all__.extend(codegen_config.__all__)
__all__.extend(tokenization_codegen.__all__)
__all__.extend(tokenization_codegen_fast.__all__)
