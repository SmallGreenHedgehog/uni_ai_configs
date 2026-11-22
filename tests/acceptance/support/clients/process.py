import json
import subprocess
from pathlib import Path


class HookScriptClient:
    def run(self, script_path: Path, payload: dict, workspace: Path) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [str(script_path)],
            input=json.dumps(payload),
            cwd=workspace,
            capture_output=True,
            text=True,
            check=False,
        )
        return result
