"""AppleScript execution utilities."""

import os
import tempfile
import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)


async def execute_applescript(code: str, timeout: int = 60) -> str:
    """
    Execute AppleScript code and return the result.

    Args:
        code: The AppleScript code to execute
        timeout: Execution timeout in seconds (default: 60)

    Returns:
        The output from the AppleScript execution

    Raises:
        Exception: If execution fails or times out
    """
    logger.debug(f"Executing AppleScript with timeout {timeout}s")

    # Create temp file for the AppleScript
    with tempfile.NamedTemporaryFile(suffix='.scpt', delete=False) as temp:
        temp_path = temp.name
        try:
            # Write the AppleScript to the temp file
            temp.write(code.encode('utf-8'))
            temp.flush()

            # Execute the AppleScript
            cmd = ["/usr/bin/osascript", temp_path]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            if result.returncode != 0:
                error_message = f"AppleScript execution failed: {result.stderr}"
                logger.error(error_message)
                return error_message

            logger.debug("AppleScript executed successfully")
            return result.stdout.strip()

        except subprocess.TimeoutExpired:
            error_message = f"AppleScript execution timed out after {timeout} seconds"
            logger.error(error_message)
            return error_message
        except Exception as e:
            error_message = f"Error executing AppleScript: {str(e)}"
            logger.error(error_message)
            return error_message
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_path)
            except Exception as e:
                logger.warning(f"Failed to delete temporary file: {e}")