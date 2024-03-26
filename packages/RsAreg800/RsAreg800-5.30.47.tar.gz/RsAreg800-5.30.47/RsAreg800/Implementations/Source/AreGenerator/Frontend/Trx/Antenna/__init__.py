from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AntennaCls:
	"""Antenna commands group definition. 16 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("antenna", core, parent)

	@property
	def custom(self):
		"""custom commands group. 7 Sub-classes, 1 commands."""
		if not hasattr(self, '_custom'):
			from .Custom import CustomCls
			self._custom = CustomCls(self._core, self._cmd_group)
		return self._custom

	@property
	def gain(self):
		"""gain commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gain'):
			from .Gain import GainCls
			self._gain = GainCls(self._core, self._cmd_group)
		return self._gain

	def clone(self) -> 'AntennaCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AntennaCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
