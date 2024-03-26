from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UpdateCls:
	"""Update commands group definition. 4 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("update", core, parent)

	@property
	def check(self):
		"""check commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_check'):
			from .Check import CheckCls
			self._check = CheckCls(self._core, self._cmd_group)
		return self._check

	@property
	def needed(self):
		"""needed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_needed'):
			from .Needed import NeededCls
			self._needed = NeededCls(self._core, self._cmd_group)
		return self._needed

	@property
	def tselected(self):
		"""tselected commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_tselected'):
			from .Tselected import TselectedCls
			self._tselected = TselectedCls(self._core, self._cmd_group)
		return self._tselected

	def clone(self) -> 'UpdateCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UpdateCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
