from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConnectCls:
	"""Connect commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("connect", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MULTiinstrument:CONNect \n
		Snippet: driver.source.areGenerator.osetup.multiInstrument.connect.set() \n
		Triggers connection to all secondary instruments by establishing a control connection via LAN. The R&S AREG800A connects
		all secondary instruments as configured by their IP address or hostname.
		See [:SOURce<hw>]:AREGenerator:OSETup:MULTiinstrument:SECondary<st>:HOSTname. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:MULTiinstrument:CONNect')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MULTiinstrument:CONNect \n
		Snippet: driver.source.areGenerator.osetup.multiInstrument.connect.set_with_opc() \n
		Triggers connection to all secondary instruments by establishing a control connection via LAN. The R&S AREG800A connects
		all secondary instruments as configured by their IP address or hostname.
		See [:SOURce<hw>]:AREGenerator:OSETup:MULTiinstrument:SECondary<st>:HOSTname. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsAreg800.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:AREGenerator:OSETup:MULTiinstrument:CONNect', opc_timeout_ms)
