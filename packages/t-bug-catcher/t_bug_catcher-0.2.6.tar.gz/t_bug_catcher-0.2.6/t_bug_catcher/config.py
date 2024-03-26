import os

from .workitems import variables


class Config:
    """Config class for configuring the application."""

    class LIMITS:
        """Limits class for configuring the application."""

        MAX_ATTACHMENTS: int = 5
        MAX_ISSUE_ATTACHMENTS: int = 100
        MAX_DESCRIPTION_LENGTH: int = 250

    RC_RUN_LINK = (
        f"https://cloud.robocorp.com/organizations/{os.environ.get('RC_ORGANIZATION_ID')}"
        f"/workspaces/{os.environ.get('RC_WORKSPACE_ID')}/processes"
        f"/{os.environ.get('RC_PROCESS_ID')}/runs/{os.environ.get('RC_PROCESS_RUN_ID')}/"
    )

    ENVIRONMENT = (
        "robocloud"
        if not variables.get("environment") and os.environ.get("RC_PROCESS_RUN_ID")
        else variables.get("environment", "local")
    )


CONFIG = Config()
