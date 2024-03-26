from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RemoveCls:
	"""Remove commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("remove", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MULTiinstrument:SECondary:REMove \n
		Snippet: driver.source.areGenerator.osetup.multiInstrument.secondary.remove.set() \n
		Removes the secondary instrument from connected R&S AREG800A instruments that are listed in the primary instrument. Also,
		this command terminates the control connection between primary instrument and the secondary instrument. The firmware
		saves hostname of the secondary instrument for correct mapping. For example, if you want to add the secondary instrument
		again. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:MULTiinstrument:SECondary:REMove')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MULTiinstrument:SECondary:REMove \n
		Snippet: driver.source.areGenerator.osetup.multiInstrument.secondary.remove.set_with_opc() \n
		Removes the secondary instrument from connected R&S AREG800A instruments that are listed in the primary instrument. Also,
		this command terminates the control connection between primary instrument and the secondary instrument. The firmware
		saves hostname of the secondary instrument for correct mapping. For example, if you want to add the secondary instrument
		again. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsAreg800.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:AREGenerator:OSETup:MULTiinstrument:SECondary:REMove', opc_timeout_ms)
