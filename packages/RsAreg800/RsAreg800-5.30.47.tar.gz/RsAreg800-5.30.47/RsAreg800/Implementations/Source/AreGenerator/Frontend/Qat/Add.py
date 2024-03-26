from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AddCls:
	"""Add commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("add", core, parent)

	def set(self, qatFrontent=repcap.QatFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:ADD \n
		Snippet: driver.source.areGenerator.frontend.qat.add.set(qatFrontent = repcap.QatFrontent.Default) \n
		Adds a configuration for a QAT-type frontend. A line with contiguous numeration is added. \n
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
		"""
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:ADD')

	def set_with_opc(self, qatFrontent=repcap.QatFrontent.Default, opc_timeout_ms: int = -1) -> None:
		qatFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(qatFrontent, repcap.QatFrontent)
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:QAT<CH>:ADD \n
		Snippet: driver.source.areGenerator.frontend.qat.add.set_with_opc(qatFrontent = repcap.QatFrontent.Default) \n
		Adds a configuration for a QAT-type frontend. A line with contiguous numeration is added. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsAreg800.utilities.opc_timeout_set() to set the timeout value. \n
			:param qatFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qat')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:AREGenerator:FRONtend:QAT{qatFrontent_cmd_val}:ADD', opc_timeout_ms)
