from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModeCls:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def set(self, areg_fe_qat_mode: enums.AregFeQatMode, qatFrontent=repcap.QatFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:MODE \n
		Snippet: driver.source.areGenerator.frontend.qat.mode.set(areg_fe_qat_mode = enums.AregFeQatMode.MULTi, qatFrontent = repcap.QatFrontent.Default) \n
		Sets the channel mode including the channel settings for configuration of the channels at the connected QAT-type frontend. \n
			:param areg_fe_qat_mode: SINGle| MULTi SINGle Sets the configuration for single channel mode at the connected QAT-type frontend. MULTi Sets the configuration for multi channel mode at the connected QAT-type frontend.
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
		"""
		param = Conversions.enum_scalar_to_str(areg_fe_qat_mode, enums.AregFeQatMode)
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, qatFrontent=repcap.QatFrontent.Default) -> enums.AregFeQatMode:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:MODE \n
		Snippet: value: enums.AregFeQatMode = driver.source.areGenerator.frontend.qat.mode.get(qatFrontent = repcap.QatFrontent.Default) \n
		Sets the channel mode including the channel settings for configuration of the channels at the connected QAT-type frontend. \n
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
			:return: areg_fe_qat_mode: SINGle| MULTi SINGle Sets the configuration for single channel mode at the connected QAT-type frontend. MULTi Sets the configuration for multi channel mode at the connected QAT-type frontend."""
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AregFeQatMode)
