import enum
from dataclasses import dataclass, field

from hydra.core.config_store import ConfigStore
from hydra.core.config_search_path import ConfigSearchPath
from hydra.plugins.search_path_plugin import SearchPathPlugin


class FalconTask(enum.Enum):
    r"""
        Enumerates the tasks that the Falcon challenge supports.
    """
    h1 = "falcon_h1_7d"
    h2 = "falcon_h2_writing"
    m1 = "falcon_m1_finger"
    m2 = "falcon_m2_reach"

@dataclass
class FalconConfig:
    r"""
        User is responsible for copying this appropriately,
        since ultimately these values are to help user to inform decoder what outputs are expected.
    """
    # falcon_h1, falcon_h2_writing, falcon_m1_finger, falcon_m2_reach
    task: FalconTask = FalconTask.h1
    # n_channels: int = 176
    bin_size_ms: int = 20
    dataset_handles: list[str] = field(default_factory=lambda: []) # Compute with evaluator.get_eval_handles

    @property
    def n_channels(self):
        if self.task == FalconTask.h1:
            return 176
        elif self.task == FalconTask.m1:
            return 96
        elif self.task == FalconTask.m2:
            return 96
        raise NotImplementedError(f"Task {self.task} not implemented.")

    @property
    def out_dim(self):
        if self.task == FalconTask.h1:
            return 7
        elif self.task == FalconTask.h2:
            return 28
        elif self.task == FalconTask.m1:
            return 16
        elif self.task == FalconTask.m2:
            return 2

cs = ConfigStore.instance()
cs.store(name="falcon_config", node=FalconConfig)