from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CustomCls:
	"""Custom commands group definition. 1 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("custom", core, parent)

	@property
	def importPy(self):
		"""importPy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_importPy'):
			from .ImportPy import ImportPyCls
			self._importPy = ImportPyCls(self._core, self._cmd_group)
		return self._importPy

	def clone(self) -> 'CustomCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CustomCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
