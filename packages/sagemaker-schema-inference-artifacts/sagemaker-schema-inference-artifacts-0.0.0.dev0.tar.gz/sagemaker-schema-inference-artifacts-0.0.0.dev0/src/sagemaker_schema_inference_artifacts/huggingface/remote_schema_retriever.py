# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""Accessors to retrieve task fallback input/output schema"""
import os
import json5
from typing import Any, Tuple
from sagemaker_schema_inference_artifacts.huggingface.config import (SUPPORTED_TASKS, SAMPLE_IMAGE, SAMPLE_AUDIO,
                                                                     PATH_TO_SAMPLE_IMAGE, PATH_TO_SAMPLE_AUDIO,
                                                                     PATH_TO_HF_TASKS_NPM)


class RemoteSchemaRetriever:
    __src_dir = os.path.dirname(os.path.dirname(__file__))

    def get_resolved_hf_schema_for_task(self, task: str) -> Tuple[Any, Any]:
        """Retrieves task sample inputs and outputs from the huggingface tasks npm module.

        Args:
            task (str): Required, the task name

        Returns:
            Tuple[Any, Any]: A tuple that contains the sample input at index 0, and sample output at index 1.

        Raises:
            RuntimeError: If the sample data from huggingface failed to be loaded.
        """
        self.__validate_task_support(task)
        hugging_face_demo_data = self.__retrieve_hf_demo_data_for_task(task)
        sample_inputs, sample_outputs = dict(), dict()
        sample_inputs['properties'], sample_outputs['properties'] = list(), list()
        try:
            input_data, output_data = hugging_face_demo_data['inputs'], hugging_face_demo_data['outputs']
            for item in input_data:
                processed_item = dict(item)
                self.__add_image_or_audio_sample(processed_item)
                sample_inputs['properties'].append(processed_item)
            for item in output_data:
                processed_item = dict(item)
                self.__add_image_or_audio_sample(processed_item)
                sample_outputs['properties'].append(processed_item)
            if not sample_inputs['properties'] or not sample_outputs['properties']:
                raise RuntimeError(f"Sample data for task {task} could not be loaded.")
            return sample_inputs, sample_outputs
        except KeyError as e:
            raise RuntimeError(f"Sample data for task {task} from huggingface was invalid. KeyError: {e}")

    def get_src_dir(self) -> str:
        """Helper method to get the current dir, used in tests

        Returns:
            str: Current dir
        """
        return str(self.__src_dir)

    def __retrieve_hf_demo_data_for_task(self, task: str) -> dict[str, Any]:
        """Retrieves task sample inputs and outputs from the huggingface tasks npm module.

        Args:
            task (str): Required, the task name

        Returns:
            Json5 outputted dict containing raw data from hugging face data.ts "demo" data for the given task.

        Raises:
            RuntimeError: If the data.ts file from huggingface is missing,
            OR, if the loaded data from huggingface does not have the required information ('demo')
        """
        task = task.lower()
        hf_data_typescript_file = os.path.join(self.__src_dir, PATH_TO_HF_TASKS_NPM, task, 'data.ts')
        try:
            with open(hf_data_typescript_file, "r") as file:
                data_string = file.read()
                start, stop = data_string.find('const taskData: TaskDataCustom ='), data_string.rfind(
                    'export default taskData;')
                raw_hf_task_data = data_string[start: stop]
                raw_hf_task_data = raw_hf_task_data.replace("const taskData: TaskDataCustom =", '').strip().strip(';')
                # NOTE: raw data has raw string keys and trailing commas, which only "json5" will ignore.
                json_task_data = json5.loads(raw_hf_task_data)
                try:
                    return json_task_data['demo']
                except KeyError as e:
                    raise RuntimeError(f"Sample data for task {task} could not be loaded. KeyError: {e}")
        except FileNotFoundError as e:
            raise RuntimeError(f"Data.ts file for task {task} was not found. {e}")

    def __validate_task_support(self, task: str) -> None:
        """Validates if the task is supported.

        Args:
            task (str): Required, the task name

        Raises:
            ValueError: If the task is not supported.
        """
        if task not in SUPPORTED_TASKS:
            raise ValueError(f"Task {task} is not supported. Supported tasks are: {', '.join(SUPPORTED_TASKS)}")

    def __add_image_or_audio_sample(self, item: dict[str, Any]) -> None:
        """Adds an image or audio file and path if needed

        Args:
            item (dict[str,Any]): Unaltered HuggingFace object

        Raises:
            RuntimeError: If the sample image or audio files are not found.
        """
        if 'type' in item.keys():
            if item['type'] == 'img':
                item['filename'] = SAMPLE_IMAGE
                img = os.path.join(self.__src_dir, PATH_TO_SAMPLE_IMAGE, SAMPLE_IMAGE)
                try:
                    with open(img) as _:  # Validate file exists
                        item['path'] = img
                except FileNotFoundError as e:
                    raise RuntimeError(f"File '{SAMPLE_IMAGE}' was not found. {e}")
            elif item['type'] == 'audio':
                item['filename'] = SAMPLE_AUDIO
                audio = os.path.join(self.__src_dir, PATH_TO_SAMPLE_AUDIO, SAMPLE_AUDIO)
                try:
                    with open(audio) as _:  # Validate file exists
                        item['path'] = audio
                except FileNotFoundError as e:
                    raise RuntimeError(f"File '{SAMPLE_AUDIO}' was not found. {e}")
