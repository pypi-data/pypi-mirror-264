from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConnectionCls:
	"""Connection commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("connection", core, parent)

	# noinspection PyTypeChecker
	def get_state(self) -> enums.AregMultiInstCnctStatus:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MULTiinstrument:SECondary:CONNection:[STATe] \n
		Snippet: value: enums.AregMultiInstCnctStatus = driver.source.areGenerator.osetup.multiInstrument.secondary.connection.get_state() \n
		Queries the connection state of the secondary instrument. If you remove a secondary instrument, the connection state of
		this secondary instrument is DISConnected. \n
			:return: conn_state: DISConnected| CONNected| TCONnencting| TDISconnecting| CERRor DISConnected The secondary instrument is disconnected. DISConnected The secondary instrument is connected. TDISconnecting Triggers disconnecting the secondary instrument. CERRor Connection error.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:MULTiinstrument:SECondary:CONNection:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.AregMultiInstCnctStatus)
