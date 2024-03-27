from abc import ABC, abstractmethod
from typing import List


class IProcessor(ABC):
  """
  Interface for a generic Processor with a nested class for processor details.
  """
  class ProcessorDetails(ABC):
    version: str
    description: str
    dependencies: List[str]

  @property
  @abstractmethod
  def processor_details(self) -> 'IProcessor.ProcessorDetails':
    """
    Property to get processor details.
    """
    pass

  @abstractmethod
  def run(self, *args, **kwargs) -> None:
    """
    The main method to run the processor's task.
    """
    pass
