from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InfoCls:
	"""Info commands group definition. 4 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("info", core, parent)

	@property
	def otime(self):
		"""otime commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_otime'):
			from .Otime import OtimeCls
			self._otime = OtimeCls(self._core, self._cmd_group)
		return self._otime

	@property
	def poCount(self):
		"""poCount commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_poCount'):
			from .PoCount import PoCountCls
			self._poCount = PoCountCls(self._core, self._cmd_group)
		return self._poCount

	def clone(self) -> 'InfoCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InfoCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
