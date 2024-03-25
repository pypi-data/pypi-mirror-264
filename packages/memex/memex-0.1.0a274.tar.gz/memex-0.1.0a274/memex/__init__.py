import io
import time
from typing import Any, BinaryIO, Dict, List
from .types import _udf_payload
import pandas as pd
import requests
import os


class MemexSessionError(Exception):
    """Custom exception for API errors."""

    pass


class MemexSession:
    def __init__(self, base_url: str, api_key: str = None, verify_ssl: bool = True) -> None:
        """Connect to Memex API at the specified base URL.
        Set the API key for authentication explicitly or via environment variable `MEMEX_API_KEY`.

        Parameters:
            base_url (str, required): The base URL of the Memex API
            api_key (str, optional): The API key to use for authentication. If not provided, it will be read from the `MEMEX_API_KEY` environment variable.
            verify_ssl (bool, optional): Whether to verify the SSL certificate. Defaults to True.
        """
        self.base_url = base_url.rstrip("/")
        self.verify_ssl = verify_ssl
        self.api_key = api_key or os.getenv("MEMEX_API_KEY")
        if self.api_key is None:
            raise MemexSessionError(
                "No API key provided and MEMEX_API_KEY environment variable not set."
            )

    def headers(self) -> Dict[str, str]:
        """Returns the headers to use for API requests."""
        return {"Authorization": f"Bearer {self.api_key}"}

    def _handle_response(self, response: requests.Response, as_csv: bool = False) -> Any:
        """
        Handles the HTTP response, raising an error if it's not successful.

        Args:
            response (requests.Response): The response object to handle.

        Returns:
            Any: The JSON content from the response, if successful.
        """
        try:
            response.raise_for_status()
        except requests.HTTPError as http_err:
            # Attempt to provide a JSON-based error message if one can be parsed
            try:
                error_data = response.json()
                error_message = error_data.get("detail", str(error_data))
            except ValueError:  # JSON response could not be decoded
                error_message = str(http_err)

            raise MemexSessionError(f"API request unsuccessful: {error_message}") from http_err

        if as_csv:
            content_type = response.headers.get("Content-Type")
            if "text/csv" in content_type:
                return pd.read_csv(io.StringIO(response.content.decode()))
            else:
                return response.json()
        else:
            return response.json()

    def list_datasets(self) -> List[Dict[str, Any]]:
        """Fetches available datasets."""
        response = requests.get(
            f"{self.base_url}/api/datasets", headers=self.headers(), verify=self.verify_ssl
        )
        return self._handle_response(response)

    def save_prompt_as_function(
        self, name: str, prompt: str, variables: List[str], overwrite: bool = False
    ) -> Dict[str, Any]:
        """Saves a prompt as a function."""
        function_data = {"name": name, "content": prompt, "variables": variables}
        function_param = {"function": function_data, "overwrite": overwrite}
        response = requests.post(
            f"{self.base_url}/api/functions",
            json=function_param,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def query(self, query: str, **kwargs) -> pd.DataFrame:
        """Execute a SQL query and return the results as a pandas DataFrame.

        Parameters:
            query (str): The SQL query to execute.
            **kwargs: Additional keyword arguments to pass to the query.

        Kwargs:
            - max_tokens (int, optional): The maximum number of tokens to generate.
            - temperature (float, optional): The temperature for generation
            - use_cache (bool, optional): Whether to use the cache for the query
        """
        query_data = {"query": query, **kwargs}
        response = requests.post(
            f"{self.base_url}/api/query",
            json=query_data,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        task_response = self._handle_response(response)

        task_id = task_response.get("task_id")
        if not task_id:
            raise MemexSessionError("Query did not return a task_id")

        task_status_json = self._poll_for_task(task_id)

        # Assuming the task result is directly the data needed for DataFrame
        if "result" not in task_status_json:
            raise MemexSessionError(f"Task {task_id} completed but no result found")

        # Convert the task result to a pandas DataFrame
        return pd.DataFrame(task_status_json["result"]["data"])

    def _poll_for_task(
        self, task_id: str, initial_polling_interval: float = 0.1, max_polling_interval: float = 5
    ) -> dict:
        """Polls the task status until it is completed or failed.

        Parameters:
            task_id (str): The ID of the task to poll.
            initial_polling_interval (float, optional): The initial polling interval in seconds. Defaults to 0.1.
            max_polling_interval (float, optional): The maximum polling interval in seconds. Defaults to 5.

        Returns:
            dict: The final status of the task.
        """
        task_status = None
        polling_interval = initial_polling_interval

        while task_status not in ["completed", "failed"]:
            task_status_response = requests.get(
                f"{self.base_url}/api/tasks/{task_id}",
                headers=self.headers(),
                verify=self.verify_ssl,
            )
            task_status_json = self._handle_response(task_status_response)
            task_status = task_status_json.get("status")

            if task_status == "failed":
                raise MemexSessionError(
                    f"Task {task_id} failed, error: {task_status_json.get('error')}"
                )

            time.sleep(polling_interval)
            polling_interval = min(
                polling_interval * 2, max_polling_interval
            )  # Exponential backoff

        return task_status_json

    def upload_dataset(self, file: BinaryIO, file_name: str) -> Dict[str, Any]:
        """Uploads a dataset."""
        files = {"file": (file_name, file)}
        response = requests.put(
            f"{self.base_url}/api/datasets/upload",
            files=files,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def download_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Download a dataset in CSV format.
        Returns:
            pd.DataFrame: The dataset as a pandas DataFrame.
        """
        response = requests.get(
            f"{self.base_url}/api/datasets/download/{dataset_name}",
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response, as_csv=True)

    def get_models(self) -> List[Dict[str, Any]]:
        """Retrieves the list of available models."""
        response = requests.get(
            f"{self.base_url}/api/models", headers=self.headers(), verify=self.verify_ssl
        )
        return self._handle_response(response)

    def llm(self, prompts: list[str], model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
        """Invokes an LLM with a specified prompt."""
        prompt_data = {"items": prompts, "model": model}
        response = requests.post(
            f"{self.base_url}/api/llm",
            json=prompt_data,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def update_function(self, function_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates a function with new details."""
        response = requests.put(
            f"{self.base_url}/api/functions",
            json=function_data,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def save_function(self, function_data: Dict[str, Any]) -> Dict[str, Any]:
        """Saves a new function."""
        response = requests.post(
            f"{self.base_url}/api/functions",
            json=function_data,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def get_function(self, name: str) -> Dict[str, Any]:
        """Fetches a function with the given name."""
        response = requests.get(
            f"{self.base_url}/api/functions/{name}", headers=self.headers(), verify=self.verify_ssl
        )
        return self._handle_response(response)

    def save_as_table(self, name: str, query: str, *, overwrite=False, **kwargs) -> Dict[str, Any]:
        """Saves a query as a table with a specified name.

        Args:
            name (str): The name of the table.
            query (str): The SQL query to save as a table.
            overwrite (bool, optional): Whether to overwrite an existing table with the same name. Defaults to False.
            **kwargs: Additional keyword arguments to pass to the query.

        Kwargs:
            - max_tokens (int, optional): The maximum number of tokens to generate.

            - temperature (float, optional): The temperature for generation

            - use_cache (bool, optional): Whether to use the cache for the query

        Returns:
            Dict[str, Any]: The JSON response from the API.
        """
        payload = {"name": name, "query": {"query": query, **kwargs}, "overwrite": overwrite}
        response = requests.post(
            f"{self.base_url}/api/tables",
            json=payload,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        task_response = self._handle_response(response)

        task_id = task_response.get("task_id")
        if not task_id:
            raise MemexSessionError("Query did not return a task_id")

        task_status_json = self._poll_for_task(task_id)

        if "result" not in task_status_json:
            raise MemexSessionError(f"Task {task_id} completed but no result found")

        return task_status_json["result"]

    def delete_table(self, table_name: str) -> Dict[str, Any]:
        """Deletes a table with the given reference."""
        response = requests.delete(
            f"{self.base_url}/api/tables",
            json=dict(name=table_name),
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def list_queries(self) -> List[Dict[str, Any]]:
        """Lists all saved queries."""
        response = requests.get(
            f"{self.base_url}/api/queries", headers=self.headers(), verify=self.verify_ssl
        )
        return self._handle_response(response)

    def get_query(self, name: str) -> Dict[str, Any]:
        """Fetches a query with the given name."""
        response = requests.get(
            f"{self.base_url}/api/queries/{name}", headers=self.headers(), verify=self.verify_ssl
        )
        return self._handle_response(response)

    def save_query(self, name: str, query: str, overwrite: bool = False) -> Dict[str, Any]:
        """Saves a query with a specified name."""
        payload = {"name": name, "query": query, "overwrite": overwrite}
        response = requests.post(
            f"{self.base_url}/api/queries",
            json=payload,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def delete_query(self, name: str) -> Dict[str, Any]:
        """Deletes a query with the given name."""
        response = requests.delete(
            f"{self.base_url}/api/queries/{name}", headers=self.headers(), verify=self.verify_ssl
        )
        return self._handle_response(response)

    def save_label(self, label_data: Dict[str, Any]) -> Dict[str, Any]:
        """Saves label data for a dataset."""
        response = requests.post(
            f"{self.base_url}/api/labels/items",
            json=label_data,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def create_label_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a label session for labeling tasks."""
        response = requests.post(
            f"{self.base_url}/api/labels",
            json=session_data,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def delete_label_session(self, session_reference: Dict[str, str]) -> Dict[str, Any]:
        """Deletes a label session with the given reference."""
        response = requests.delete(
            f"{self.base_url}/api/labels",
            json=session_reference,
            headers=self.headers(),
            verify=self.verify_ssl,
        )
        return self._handle_response(response)

    def list_functions(self) -> List[Dict[str, Any]]:
        """Lists all available functions."""
        response = requests.get(
            f"{self.base_url}/api/functions", headers=self.headers(), verify=self.verify_ssl
        )
        return self._handle_response(response)

    def udf(self, func=None, *, prompt=False, resources=None, remote=False):
        """
        Decorator that registers a function as a User-Defined Function (UDF) for use within Memex SQL queries.

        This decorator is intended to be used on functions to either register them as native Python functions or as LLM
        prompt functions for execution within Memex SQL.

        Parameters:
            func (callable): The function to register as a UDF.
            prompt (bool, optional): If True, the function is registered as an LLM prompt function, using its docstring as the prompt. Defaults to False.
            session (MemexSession, optional): The session instance for registration. Defaults to a new MemexSession instance.
            resources (any, optional): Additional resources required by the UDF. Defaults to None. Any resources specified will be stored and make available to the UDF at runtime. Resources are only applicable to Python native functions.
            remote (bool, optional): If True, indicates the UDF should be executed remotely. Defaults to False.

        Example usage:
        ```
        @mx.udf
        def is_anagram(a:str, b:str) -> bool:
            return sorted(a) == sorted(b)
        ```
        """
        return _udf(func, prompt=prompt, session=self, resources=resources, remote=remote)

    def prompt(self, func=None):
        """
        Decorator that registers a function as a Prompt User-Defined Function (UDF) for use within Memex SQL queries.

        Example usage:
        ```
        @mx.prompt
        def joke(topic:str) -> str:
            "Tell me a joke about {topic}"
        ```
        """
        return _udf(func, prompt=True, session=self)


def _udf(func=None, *, prompt=False, session=None, resources=None, remote=False):
    # this is to allow for both @udf and @udf()
    if func is None:
        return lambda f: _udf(f, prompt=prompt, session=session, resources=resources, remote=remote)

    payload = _udf_payload(func, prompt, resources, remote)

    session.update_function(payload)

    return func


def make_resources(resources: dict[str, str]):
    """Wrap a dictionary of resources to make it available to the Python UDF in Memex.
    For example:
    ```
    resources = make_resources({"my_resource": "path/to/my/resource"})

    @mx.udf(resources=resources)
    def my_udf():
        resource = resources("my_resource")
        ...
    ```
    The `resources` will be made available to the Python function local scope at runtime under the name `__resources`.
    """
    return resources


def get_model(model_name: str, **extra_args):
    """
    Fetch a specific Large Language Model (LLM) by name.

    This function serves as a stub for use within user-defined functions (@udf) and is only operational when
    executed as part of a @udf function within the Memex backend environment.

    Parameters:
        model_name (str): The identifier for the desired model (e.g., "gpt-3.5-turbo").
        **extra_args: Arbitrary keyword arguments representing additional parameters for model configuration.
            Supported parameters include:
            - max_tokens (int, optional): Defines the maximum number of tokens the model should generate.
            - temperature (float, optional): Controls the randomness of the output (ranging from 0 to 1.0).

    """
    raise NotImplementedError("This function is only available when running inside Memex.")


def run_strict(
    model,
    prompt: str,
    response_type,
    max_retries: int = 3,
    error_template: str = "Your previous attempt failed with the following error message: {error}\n\nPlease try again",
    **kwargs,
):  # noqa: F821
    """
    Execute a model with retries on response validation error, halting after a specified number of retries.

    Parameters:
        model: The model to be executed.
        prompt (str): The input prompt for the model.
        response_type: The expected type of the response.
        max_retries (int, optional): The maximum number of retry attempts. Defaults to 3.
        error_template (str, optional): The error message template to use on retry.
            Should include a `{error}` placeholder for the validation error message. Defaults to a standard error message.
        **kwargs: Additional keyword arguments to pass to the model's run method.

    Returns:
        The response from the model, cast to `response_type` if it is a Pydantic model, otherwise the raw response.

    """
    raise NotImplementedError("This function is only available when running inside Memex.")


__all__ = [MemexSession, make_resources, get_model, run_strict]
