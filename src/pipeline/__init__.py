# ./src/pipeline/__init__.py

"""
Pipeline package for orchestrating and running scraping pipelines.

This package provides the main classes for managing data scraping pipelines:
- `PipelineRunner`: Executes the pipeline steps sequentially.
- `PipelineOrchestrator`: Coordinates multiple pipelines, manages scheduling,
  and handles orchestration logic.

Modules:
    runner: Contains `PipelineRunner` for executing individual pipelines.
    orchestrator: Contains `PipelineOrchestrator` for coordinating pipelines.
"""

from .runner import PipelineRunner
from .orchestrator import PipelineOrchestrator

__all__ = ["PipelineRunner", "PipelineOrchestrator"]
