from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PauseCls:
	"""Pause commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pause", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:PAUSe \n
		Snippet: driver.source.areGenerator.scenario.pause.set() \n
		Pauses the player. After pausing, you can resume playing by [:SOURce<hw>]:AREGenerator:SCENario:STARt. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SCENario:PAUSe')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:PAUSe \n
		Snippet: driver.source.areGenerator.scenario.pause.set_with_opc() \n
		Pauses the player. After pausing, you can resume playing by [:SOURce<hw>]:AREGenerator:SCENario:STARt. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsAreg800.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:AREGenerator:SCENario:PAUSe', opc_timeout_ms)
