from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxCls:
	"""Rx commands group definition. 3 total commands, 2 Subgroups, 0 group commands
	Repeated Capability: RxIndex, default value after init: RxIndex.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rx", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_rxIndex_get', 'repcap_rxIndex_set', repcap.RxIndex.Nr1)

	def repcap_rxIndex_set(self, rxIndex: repcap.RxIndex) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to RxIndex.Default
		Default value after init: RxIndex.Nr1"""
		self._cmd_group.set_repcap_enum_value(rxIndex)

	def repcap_rxIndex_get(self) -> repcap.RxIndex:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_file'):
			from .File import FileCls
			self._file = FileCls(self._core, self._cmd_group)
		return self._file

	@property
	def glist(self):
		"""glist commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_glist'):
			from .Glist import GlistCls
			self._glist = GlistCls(self._core, self._cmd_group)
		return self._glist

	def clone(self) -> 'RxCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RxCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
