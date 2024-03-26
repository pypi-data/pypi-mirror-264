from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DiscardCls:
	"""Discard commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("discard", core, parent)

	def set(self) -> None:
		"""SCPI: SYSTem:SCRPt:DISCard \n
		Snippet: driver.system.scrpt.discard.set() \n
		No command help available \n
		"""
		self._core.io.write(f'SYSTem:SCRPt:DISCard')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SYSTem:SCRPt:DISCard \n
		Snippet: driver.system.scrpt.discard.set_with_opc() \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsAreg800.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYSTem:SCRPt:DISCard', opc_timeout_ms)
