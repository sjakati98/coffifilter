from typing import Type, Callable, List, Union, Dict, Any, Optional
from langchain_core.callbacks import Callbacks
from langchain.tools import BaseTool
from langchain_core.tools import ToolException
from langchain_core.pydantic_v1 import BaseModel, ValidationError
from .client import Client


## Langchain Tool Wrapper
def wrap_langchain_tool(tool: BaseTool):
    """
    Wraps a BaseTool instance with a coffifilter validation check. If the tool is not added to the Redis database, the
    tool name will be added to redis with the enabled flag set to true.

    Args:
        tool (BaseTool): The tool instance to wrap.

    Returns:
        BaseTool: A wrapped tool instance that performs validation before invoking the original tool's functionality.
    """

    class ValidatedTool(BaseTool):
        name: str = tool.name
        description: str = f"Validated version of {tool.description}"
        args_schema: Optional[Type[BaseModel]] = tool.args_schema
        return_direct: bool = tool.return_direct
        verbose: bool = tool.verbose
        callbacks: Optional[Callbacks] = tool.callbacks  # Explicitly specify the type
        tags: Optional[List[str]] = tool.tags
        metadata: Optional[Dict[str, Any]] = tool.metadata
        handle_tool_error: Optional[
            Union[bool, str, Callable[[ToolException], str]]
        ] = tool.handle_tool_error
        handle_validation_error: Optional[
            Union[bool, str, Callable[[ValidationError], str]]
        ] = tool.handle_validation_error

        # Add the function to the Redis database
        Client()._add_function_to_redis(tool.name)

        def _run(self, *args: Any, **kwargs: Any) -> Any:
            try:
                Client()._check_tool_enabled(tool.name)
            except ValueError as e:
                return str(e)
            return tool._run(*args, **kwargs)

        async def _arun(self, *args: Any, **kwargs: Any) -> Any:
            try:
                Client()._check_tool_enabled(tool.name)
            except ValueError as e:
                return str(e)
            return await tool._arun(*args, **kwargs)

    return ValidatedTool()
