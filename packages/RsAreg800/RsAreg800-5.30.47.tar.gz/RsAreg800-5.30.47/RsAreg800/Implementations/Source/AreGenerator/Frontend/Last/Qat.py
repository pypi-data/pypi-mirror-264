from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class QatCls:
	"""Qat commands group definition. 1 total commands, 0 Subgroups, 1 group commands
	Repeated Capability: QatFrontent, default value after init: QatFrontent.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("qat", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_qatFrontent_get', 'repcap_qatFrontent_set', repcap.QatFrontent.Nr1)

	def repcap_qatFrontent_set(self, qatFrontent: repcap.QatFrontent) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to QatFrontent.Default
		Default value after init: QatFrontent.Nr1"""
		self._cmd_group.set_repcap_enum_value(qatFrontent)

	def repcap_qatFrontent_get(self) -> repcap.QatFrontent:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	def get(self, qatFrontent=repcap.QatFrontent.Default) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:LAST:QAT<CH> \n
		Snippet: value: int = driver.source.areGenerator.frontend.last.qat.get(qatFrontent = repcap.QatFrontent.Default) \n
		Queries the last added QAT-type, FE-type or custom frontend. Displays the number included in the frontend ID, e.g.
		'3' for QAT-type frontend ID 'Q3'. \n
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
			:return: areg_fe_last_add_qa: integer Range: 0 to 8"""
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:LAST:QAT{qatFrontent_cmd_val}?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'QatCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = QatCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
