from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AddCls:
	"""Add commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("add", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MULTiinstrument:SECondary:ADD \n
		Snippet: driver.source.areGenerator.osetup.multiInstrument.secondary.add.set() \n
		Adds the configuration of the secondary instrument. Also triggers connecting the primary instrument for control the
		secondary instrument. You can add previous secondary instruments configurations without specifying the hostname again.
		The firmware saves hostname of the secondary instrument for correct mapping. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:MULTiinstrument:SECondary:ADD')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MULTiinstrument:SECondary:ADD \n
		Snippet: driver.source.areGenerator.osetup.multiInstrument.secondary.add.set_with_opc() \n
		Adds the configuration of the secondary instrument. Also triggers connecting the primary instrument for control the
		secondary instrument. You can add previous secondary instruments configurations without specifying the hostname again.
		The firmware saves hostname of the secondary instrument for correct mapping. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsAreg800.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:AREGenerator:OSETup:MULTiinstrument:SECondary:ADD', opc_timeout_ms)
