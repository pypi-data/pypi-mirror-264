from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StatusCls:
	"""Status commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("status", core, parent)

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.AregFeQatConnMode:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:FE<CH>:STATus \n
		Snippet: value: enums.AregFeQatConnMode = driver.source.areGenerator.frontend.fe.status.get(channel = repcap.Channel.Default) \n
		Queries the connection status of the connected QAT-type or FE-type frontend. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fe')
			:return: areg_fe_qat_status: DISConnected| DIALing| CONNected| CERRor| UPDate| UERRor DISConnected Frontend is disconnected. DIALing Tries to establish a frontend connection. CONNected Valid frontend connection is established. CERRor Network connection error. UPDate Update of the network connection is in progress. UERRor Update of the network connection failed."""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:FE{channel_cmd_val}:STATus?')
		return Conversions.str_to_scalar_enum(response, enums.AregFeQatConnMode)
