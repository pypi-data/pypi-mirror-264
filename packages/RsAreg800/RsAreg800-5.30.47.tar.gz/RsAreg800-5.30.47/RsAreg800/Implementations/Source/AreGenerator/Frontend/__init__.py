from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrontendCls:
	"""Frontend commands group definition. 134 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frontend", core, parent)

	@property
	def antenna(self):
		"""antenna commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_antenna'):
			from .Antenna import AntennaCls
			self._antenna = AntennaCls(self._core, self._cmd_group)
		return self._antenna

	@property
	def cfe(self):
		"""cfe commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_cfe'):
			from .Cfe import CfeCls
			self._cfe = CfeCls(self._core, self._cmd_group)
		return self._cfe

	@property
	def fe(self):
		"""fe commands group. 16 Sub-classes, 0 commands."""
		if not hasattr(self, '_fe'):
			from .Fe import FeCls
			self._fe = FeCls(self._core, self._cmd_group)
		return self._fe

	@property
	def last(self):
		"""last commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_last'):
			from .Last import LastCls
			self._last = LastCls(self._core, self._cmd_group)
		return self._last

	@property
	def qat(self):
		"""qat commands group. 21 Sub-classes, 0 commands."""
		if not hasattr(self, '_qat'):
			from .Qat import QatCls
			self._qat = QatCls(self._core, self._cmd_group)
		return self._qat

	@property
	def trx(self):
		"""trx commands group. 14 Sub-classes, 0 commands."""
		if not hasattr(self, '_trx'):
			from .Trx import TrxCls
			self._trx = TrxCls(self._core, self._cmd_group)
		return self._trx

	def clone(self) -> 'FrontendCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrontendCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
