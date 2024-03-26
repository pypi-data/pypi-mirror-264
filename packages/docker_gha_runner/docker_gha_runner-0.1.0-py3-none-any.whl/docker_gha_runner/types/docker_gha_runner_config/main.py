from pydantic import BaseModel, ConfigDict

from . import GitHubConfig, DockerConfig, RunnerConfig

from typing import Optional

class DockerGhaRunnerConfig(BaseModel):
    model_config = ConfigDict(strict=True)

    github: GitHubConfig
    docker: DockerConfig = DockerConfig()
    runner: RunnerConfig = RunnerConfig()

    config_version: str = "0.1.0"
