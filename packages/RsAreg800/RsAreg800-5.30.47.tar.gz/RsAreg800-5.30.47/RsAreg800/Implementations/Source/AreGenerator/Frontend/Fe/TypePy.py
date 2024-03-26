from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePyCls:
	"""TypePy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("typePy", core, parent)

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.AregFeType:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:FE<CH>:TYPE \n
		Snippet: value: enums.AregFeType = driver.source.areGenerator.frontend.fe.typePy.get(channel = repcap.Channel.Default) \n
		Queries the type of the connected frontend. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fe')
			:return: frontend_type: TRX| QAT| NONE| FE| CFE TRX A TRX-type frontend is connected. QAT A QAT-type frontend is connected. NONE No frontend is connected. FE An FE-type frontend is connected. CFE A custom frontend is connected."""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:FE{channel_cmd_val}:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.AregFeType)
