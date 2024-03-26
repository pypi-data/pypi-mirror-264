from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ObjectsCls:
	"""Objects commands group definition. 4 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("objects", core, parent)

	@property
	def invalid(self):
		"""invalid commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_invalid'):
			from .Invalid import InvalidCls
			self._invalid = InvalidCls(self._core, self._cmd_group)
		return self._invalid

	@property
	def valid(self):
		"""valid commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_valid'):
			from .Valid import ValidCls
			self._valid = ValidCls(self._core, self._cmd_group)
		return self._valid

	def clone(self) -> 'ObjectsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ObjectsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
