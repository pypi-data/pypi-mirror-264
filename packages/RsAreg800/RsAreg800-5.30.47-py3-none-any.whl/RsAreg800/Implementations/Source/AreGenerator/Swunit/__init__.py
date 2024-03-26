from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SwunitCls:
	"""Swunit commands group definition. 16 total commands, 5 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("swunit", core, parent)

	@property
	def cableCorr(self):
		"""cableCorr commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cableCorr'):
			from .CableCorr import CableCorrCls
			self._cableCorr = CableCorrCls(self._core, self._cmd_group)
		return self._cableCorr

	@property
	def connect(self):
		"""connect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_connect'):
			from .Connect import ConnectCls
			self._connect = ConnectCls(self._core, self._cmd_group)
		return self._connect

	@property
	def disconnect(self):
		"""disconnect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_disconnect'):
			from .Disconnect import DisconnectCls
			self._disconnect = DisconnectCls(self._core, self._cmd_group)
		return self._disconnect

	@property
	def mapping(self):
		"""mapping commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mapping'):
			from .Mapping import MappingCls
			self._mapping = MappingCls(self._core, self._cmd_group)
		return self._mapping

	@property
	def relays(self):
		"""relays commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_relays'):
			from .Relays import RelaysCls
			self._relays = RelaysCls(self._core, self._cmd_group)
		return self._relays

	def get_hostname(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:SWUNit:HOSTname \n
		Snippet: value: str = driver.source.areGenerator.swunit.get_hostname() \n
		Sets the IP address or hostname of the connected switching unit in the test setup. \n
			:return: areg_swunit_host: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:SWUNit:HOSTname?')
		return trim_str_response(response)

	def set_hostname(self, areg_swunit_host: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SWUNit:HOSTname \n
		Snippet: driver.source.areGenerator.swunit.set_hostname(areg_swunit_host = 'abc') \n
		Sets the IP address or hostname of the connected switching unit in the test setup. \n
			:param areg_swunit_host: string
		"""
		param = Conversions.value_to_quoted_str(areg_swunit_host)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SWUNit:HOSTname {param}')

	def get_rx(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:SWUNit:RX \n
		Snippet: value: str = driver.source.areGenerator.swunit.get_rx() \n
		Requires [:SOURce<hw>]:AREGenerator:OSETup:SWUNit[:STATe] 1. Selects the switching unit connector (relay) of the
		switching unit connected to the RX channel of the R&S AREG800A. Enter the name of the relay of the switching unit to
		connect to the RX channel. \n
			:return: areg_swunit_rx_ch: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:SWUNit:RX?')
		return trim_str_response(response)

	def set_rx(self, areg_swunit_rx_ch: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SWUNit:RX \n
		Snippet: driver.source.areGenerator.swunit.set_rx(areg_swunit_rx_ch = 'abc') \n
		Requires [:SOURce<hw>]:AREGenerator:OSETup:SWUNit[:STATe] 1. Selects the switching unit connector (relay) of the
		switching unit connected to the RX channel of the R&S AREG800A. Enter the name of the relay of the switching unit to
		connect to the RX channel. \n
			:param areg_swunit_rx_ch: string
		"""
		param = Conversions.value_to_quoted_str(areg_swunit_rx_ch)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SWUNit:RX {param}')

	def get_status(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:SWUNit:STATus \n
		Snippet: value: str = driver.source.areGenerator.swunit.get_status() \n
		Queries the status of the switching unit. Displays if the switching unit is connected or disconnected. \n
			:return: areg_sw_unit_status: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:SWUNit:STATus?')
		return trim_str_response(response)

	def get_tx(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:SWUNit:TX \n
		Snippet: value: str = driver.source.areGenerator.swunit.get_tx() \n
		Requires [:SOURce<hw>]:AREGenerator:OSETup:SWUNit[:STATe] 1. Selects the switching unit connector (relay) of the
		switching unit connected to the TX channel of the R&S AREG800A. Enter the name of the relay of the switching unit to
		connect to the TX channel. \n
			:return: areg_swunit_tx_ch: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:SWUNit:TX?')
		return trim_str_response(response)

	def set_tx(self, areg_swunit_tx_ch: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SWUNit:TX \n
		Snippet: driver.source.areGenerator.swunit.set_tx(areg_swunit_tx_ch = 'abc') \n
		Requires [:SOURce<hw>]:AREGenerator:OSETup:SWUNit[:STATe] 1. Selects the switching unit connector (relay) of the
		switching unit connected to the TX channel of the R&S AREG800A. Enter the name of the relay of the switching unit to
		connect to the TX channel. \n
			:param areg_swunit_tx_ch: string
		"""
		param = Conversions.value_to_quoted_str(areg_swunit_tx_ch)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SWUNit:TX {param}')

	def clone(self) -> 'SwunitCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SwunitCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
