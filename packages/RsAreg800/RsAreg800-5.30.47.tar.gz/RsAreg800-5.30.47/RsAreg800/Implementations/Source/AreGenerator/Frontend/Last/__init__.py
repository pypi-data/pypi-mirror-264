from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LastCls:
	"""Last commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("last", core, parent)

	@property
	def fe(self):
		"""fe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fe'):
			from .Fe import FeCls
			self._fe = FeCls(self._core, self._cmd_group)
		return self._fe

	@property
	def qat(self):
		"""qat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_qat'):
			from .Qat import QatCls
			self._qat = QatCls(self._core, self._cmd_group)
		return self._qat

	def get_cfe(self) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:LAST:CFE \n
		Snippet: value: int = driver.source.areGenerator.frontend.last.get_cfe() \n
		Queries the last added QAT-type, FE-type or custom frontend. Displays the number included in the frontend ID, e.g.
		'3' for QAT-type frontend ID 'Q3'. \n
			:return: areg_fe_last_add_qa: integer Range: 0 to 8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:FRONtend:LAST:CFE?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'LastCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LastCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
