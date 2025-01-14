"""
;;; GOOTS CANNON ;;;

This tool syncs all the goots on record with the target Slack workspace
regardless of whether the workspace is on Slack Enterprise or not. For this
reason, it has to use an unstable API that mirror what the app / website
hits.

The Goots Cannon is idempotent and each run will attempt to push
each goots emoji to the Slack workspace under the name they are saved
as under `./goots`.
"""

import requests

import pathlib
import json
import dataclasses
import sys
import time
import typing
import logging

logger = logging.getLogger("goots-cannon")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s: %(message)s",
)


@dataclasses.dataclass
class Config:
    """
    Configuration schema for the file that sets up the Goots Cannon(tm)

    This avoids having to include tokens in the shell, which might include
    them in shell history or environment variables.
    """

    # Slack workspace host
    api_host: str
    # xoxd token extracted from session cookies when using the app
    xoxd: str
    # xoxc token extracted from LocalStorage configuration when using the app
    xoxc: str
    # Where the emoji assets live
    assets_root: str = "./goots"
    # Maximum number of times to retry an upload for non-critical errors
    max_retries: int = 5


@dataclasses.dataclass
class Report:
    """
    Summary data describing the outcome of an import run.
    """

    successes: int = 0
    failures: dict[str, str] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class SlackAPIResponse:
    ok: str
    error: typing.Optional[str] = None

    _retryable_errors = ["ratelimited"]

    @property
    def retryable(self) -> bool:
        return not self.ok and self.error in self._retryable_errors


def bold(s: str) -> str:
    """Bolds the selected text."""
    return f"\033[1m{s}\033[0m"


def load_configuration(path: pathlib.Path) -> Config:
    """
    Loads a configuration file into memory

    This assumes that the file exists and that it contains valid
    json, explicitly letting the caller to decide (or not) to handle
    exceptions.
    """
    with open(path, "r", encoding="utf8") as conf_file:
        config = Config(**json.load(conf_file))

    return config


def upload_emoji(
    *, conf: Config, source: pathlib.Path, name: str, retry: int = 0
) -> SlackAPIResponse:
    """
    Uploads a single emoji to the Slack workspace pointer to by conf.api_host.

    The emoji is filed using its name as an emoji identifier.

    Because the API enforces rate limiting, this retries up to conf.max_retries
    if a retryable error is encountered. If the error is not retryable, the one upload
    is deemed a failure.
    """
    with open(source, "rb") as source_file:
        response = requests.post(
            f"https://{conf.api_host}/api/emoji.add",
            cookies={"d": conf.xoxd},
            headers={},
            data={
                "token": conf.xoxc,
                "name": source.stem,
                "mode": "data",
            },
            files={"image": source_file.read()},
        )

    api_response = SlackAPIResponse(**response.json())

    if api_response.retryable and retry < conf.max_retry:
        time.sleep(0.1 * (1 + retry))
        api_response = upload_emoji(
            conf=conf, source=source, name=name, retry=retry + 1
        )

    return api_response


def upload_emojis(
    *,
    conf: Config,
    goots_root: pathlib.Path,
) -> Report:
    """
    Uploads all the emojis listed under `goots_root`. Each upload is tried in isolation
    and can fail independently.
    """
    report = Report()

    for goot in goots_root.iterdir():
        emoji_name = goot.stem
        response = upload_emoji(conf=conf, source=goot, name=emoji_name)

        if response.ok:
            report.successes += 1
        else:
            report.failures[emoji_name] = response.error

    return report


if __name__ == "__main__":
    conf_path = pathlib.Path(sys.argv[1])
    conf = load_configuration(conf_path)
    assets_root = pathlib.Path(conf.assets_root)

    logger.info(f"Preparing to sync {bold(len(list(assets_root.iterdir())))} goots!\n")

    report = upload_emojis(conf=conf, goots_root=assets_root)

    logger.info(
        f"{report.successes} new goots uploaded, {len(report.failures)} failures.\n"
    )
    logger.info("=== Failure breakdown ===")
    for name, reason in report.failures.items():
        logger.info(f"{name}: {reason}")
