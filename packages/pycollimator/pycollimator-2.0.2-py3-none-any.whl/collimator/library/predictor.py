# Copyright (C) 2024 Collimator, Inc.
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, version 3. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General
# Public License for more details.  You should have received a copy of the GNU
# Affero General Public License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

import os
import zipfile

import jax
import jax.numpy as jnp
import numpy as np

from ..framework import LeafSystem
from ..framework.system_base import UpstreamEvalError
from ..lazy_loader import LazyLoader
from ..logging import logger

torch = LazyLoader("torch", globals(), "torch")
tf = LazyLoader("tensorflow", globals(), "tensorflow")


class Predictor(LeafSystem):
    """
    Block to perform inference with a pre-trained model. Currently supports
    TorchScript and TensorFlow SavedModel formats.

    The input to the block should be of compatible type and shape expected by
    the TorchScript or TensorFlow model. For example, if the TorchScript model expects
    a `torch.float32` tensor of shape `(3, 224, 224)`, the input to the block should be
    a `jax.numpy` array of shape (3, 224, 224) of dtype `jnp.float32`. Similarly, if the
    TensorFlow SavedModel model expects a `tf.float32` tensor of shape `(3, 224, 224)`,
    the input to the block should be a `jax.numpy` array of shape (3, 224, 224) of dtype
    `jnp.float32`.

    For output types, if no casting is specified through the `cast_outputs_to_dtype`
    parameter, the output of the block will have the same dtype as the TorchScript or
    TensorFlow model output, but expressed as `jax.numpy` types. For example. if the
    TorchScript model outputs a `torch.float32` tensor, the output of the block will be
    a `jax.numpy` array of dtype `jnp.float32`.

    If casting is specified through `cast_outputs_to_dtype` parameter, all the outputs,
    of the block will be casted to this specific `jax.numpy` dtype.

    Input ports:
        (i) The ith input to the model.

    Output ports:
        (j) The jth output of the model.

    Parameters:
        filename (str):
            Path to the model file. For TorchScript, this should be a `.pt` file. For
            TensorFlow SavedModel, this should be a `.zip` containing the
            saved model. File extensions are used to infer the model format.

        num_inputs (int):
            The number of inputs to the model. Only required for TorchScript models.
            For TensorFlow SavedModel, the number of inputs is inferred from the model
            signature.

        num_outputs (int):
            The number of outputs of the model. Only required for TorchScript models.
            For TensorFlow SavedModel, the number of outputs is inferred from the model
            signature.

        cast_outputs_to_dtype (str):
            The dtype to cast all the outputs of the block to. Must correspond to a
            `jax.numpy` datatype. For example, "float32", "float64", "int32", "int64".

        add_batch_dim_to_inputs (bool):
            Whether to add a new first dimension to the inputs before evaluating the
            TorchScript or TensorFlow model. This is useful when the model expects a
            batch dimension.
    """

    def __init__(
        self,
        file_name,
        num_inputs=1,
        num_outputs=1,
        cast_outputs_to_dtype=None,
        add_batch_dim_to_inputs=False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.declare_configuration_parameters(
            file_name=file_name,
            num_inputs=num_inputs,
            num_outputs=num_outputs,
            cast_outputs_to_dtype=cast_outputs_to_dtype,
            add_batch_dim_to_inputs=add_batch_dim_to_inputs,
        )

        self.dtype_output = (
            getattr(jnp, cast_outputs_to_dtype)
            if cast_outputs_to_dtype is not None
            else None
        )

        self.add_batch_dim_to_inputs = add_batch_dim_to_inputs

        _, ext = os.path.splitext(file_name)

        if ext == ".pt":
            self.model_format = "TorchScript"
            self.model = torch.jit.load(file_name)
            self.model.eval()
            self._evaluate_output = self._evaluate_output_torch
        elif ext == ".zip":
            self.model_format = "TFSavedModel"

            model_dir = file_name[:-4]  # Remove .zip extension for directory name
            with zipfile.ZipFile(file_name, "r") as zip_ref:
                zip_ref.extractall(model_dir)

            model = tf.saved_model.load(model_dir)
            self.model = model.signatures["serving_default"]

            self.num_args = len(self.model.structured_input_signature[0])
            self.kwargs_signature = self.model.structured_input_signature[1]
            self.num_kwargs = len(self.kwargs_signature)

            num_inputs = self.num_args + self.num_kwargs
            num_outputs = len(self.model.structured_outputs)

            self._evaluate_output = self._evaluate_output_tf
        else:
            raise ValueError(
                "Unsupported filetype: the model file must have a `.pt` extension for "
                "TorchScript models, or a `.zip` extension for TensorFlow SavedModel "
                "format."
            )

        for _ in range(num_inputs):
            self.declare_input_port()

        def _make_output_callback(output_index):
            def _output_callback(time, state, *inputs, **params):
                outputs = self._evaluate_output(time, state, *inputs, **params)
                return outputs[output_index]

            return _output_callback

        for output_index in range(num_outputs):
            self.declare_output_port(
                _make_output_callback(output_index),
                requires_inputs=True,
            )

    def initialize_static_data(self, context):
        """Infer the output shapes and dtypes of the ML model."""
        # If building as part of a subsystem, this may not be fully connected yet.
        # That's fine, as long as it is connected by root context creation time.
        # This probably isn't a good long-term solution:
        #   see https://collimator.atlassian.net/browse/WC-51
        try:
            inputs = self.collect_inputs(context)

            if self.model_format == "TorchScript":
                outputs_jax = self._pure_callback_torch(*inputs)
            elif self.model_format == "TFSavedModel":
                outputs_jax = self._pure_callback_tf(*inputs)

            self.pure_callback_result_type = [
                jax.ShapeDtypeStruct(x.shape, x.dtype) for x in outputs_jax
            ]
        except UpstreamEvalError:
            logger.debug(
                "Predictor.initialize_static_data: UpstreamEvalError. "
                "Continuing without default value initialization."
            )
        return super().initialize_static_data(context)

    def _evaluate_output_torch(self, time, state, *inputs, **params):
        return jax.pure_callback(
            self._pure_callback_torch,
            self.pure_callback_result_type,
            *inputs,
        )

    def _pure_callback_torch(self, *inputs):
        inputs_casted = [torch.tensor(np.array(item)) for item in inputs]

        if self.add_batch_dim_to_inputs:
            inputs_casted = [x.unsqueeze(0) for x in inputs_casted]
        outputs = self.model(*inputs_casted)

        if not isinstance(outputs, tuple):
            outputs = (outputs,)

        outputs_jax = (
            [jnp.array(x, self.dtype_output) for x in outputs]
            if self.dtype_output is not None
            else [jnp.array(x) for x in outputs]
        )
        return outputs_jax

    def _evaluate_output_tf(self, time, state, *inputs, **params):
        return jax.pure_callback(
            self._pure_callback_tf,
            self.pure_callback_result_type,
            *inputs,
        )

    def _pure_callback_tf(self, *inputs):
        inputs_casted = [
            tf.convert_to_tensor(np.array(item), dtype=sig.dtype)
            for item, sig in zip(inputs, self.kwargs_signature.values())
        ]
        args_casted = inputs_casted[: self.num_args]

        # kwargs and outputs are reversed in the model signature, so reverse the
        # order again for alignment.
        kwargs_casted = dict(
            zip(reversed(self.kwargs_signature.keys()), inputs_casted[self.num_args :])
        )

        if self.add_batch_dim_to_inputs:
            args_casted = [tf.expand_dims(x, axis=0) for x in args_casted]
            kwargs_casted = {
                key: tf.expand_dims(value, axis=0)
                for key, value in kwargs_casted.items()
            }

        if self.num_args == 0:
            outputs_dict = self.model(**kwargs_casted)
        else:
            outputs_dict = self.model(*args_casted, **kwargs_casted)

        outputs_jax = (
            [jnp.array(x, self.dtype_output) for x in reversed(outputs_dict.values())]
            if self.dtype_output is not None
            else [jnp.array(x) for x in reversed(outputs_dict.values())]
        )
        return outputs_jax
