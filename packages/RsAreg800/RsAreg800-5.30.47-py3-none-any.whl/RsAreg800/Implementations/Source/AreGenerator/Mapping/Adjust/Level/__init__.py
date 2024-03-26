from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LevelCls:
	"""Level commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	@property
	def digHeadroom(self):
		"""digHeadroom commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_digHeadroom'):
			from .DigHeadroom import DigHeadroomCls
			self._digHeadroom = DigHeadroomCls(self._core, self._cmd_group)
		return self._digHeadroom

	@property
	def otime(self):
		"""otime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_otime'):
			from .Otime import OtimeCls
			self._otime = OtimeCls(self._core, self._cmd_group)
		return self._otime

	def clone(self) -> 'LevelCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LevelCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
