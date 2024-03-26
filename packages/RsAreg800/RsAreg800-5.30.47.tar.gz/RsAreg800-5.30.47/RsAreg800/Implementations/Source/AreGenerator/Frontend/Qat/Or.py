from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OrCls:
	"""Or commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("or", core, parent)

	def set(self, areg_fe_orient: enums.AregFeQatOrientation, qatFrontent=repcap.QatFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:OR \n
		Snippet: driver.source.areGenerator.frontend.qat.or.set(areg_fe_orient = enums.AregFeQatOrientation.HORizontal, qatFrontent = repcap.QatFrontent.Default) \n
		Sets the orientation parameter of the QAT in the test setup. \n
			:param areg_fe_orient: VERTical| HORizontal VERTical The QAT is placed vertically in the test setup. HORizontal The QAT is placed horizontally in the test setup.
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
		"""
		param = Conversions.enum_scalar_to_str(areg_fe_orient, enums.AregFeQatOrientation)
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:OR {param}')

	# noinspection PyTypeChecker
	def get(self, qatFrontent=repcap.QatFrontent.Default) -> enums.AregFeQatOrientation:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:OR \n
		Snippet: value: enums.AregFeQatOrientation = driver.source.areGenerator.frontend.qat.or.get(qatFrontent = repcap.QatFrontent.Default) \n
		Sets the orientation parameter of the QAT in the test setup. \n
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
			:return: areg_fe_orient: VERTical| HORizontal VERTical The QAT is placed vertically in the test setup. HORizontal The QAT is placed horizontally in the test setup."""
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:OR?')
		return Conversions.str_to_scalar_enum(response, enums.AregFeQatOrientation)
