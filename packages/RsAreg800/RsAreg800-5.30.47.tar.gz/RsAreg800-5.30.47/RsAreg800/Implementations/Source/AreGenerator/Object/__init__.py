from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ObjectCls:
	"""Object commands group definition. 8 total commands, 2 Subgroups, 0 group commands
	Repeated Capability: ObjectIx, default value after init: ObjectIx.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("object", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_objectIx_get', 'repcap_objectIx_set', repcap.ObjectIx.Nr1)

	def repcap_objectIx_set(self, objectIx: repcap.ObjectIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ObjectIx.Default
		Default value after init: ObjectIx.Nr1"""
		self._cmd_group.set_repcap_enum_value(objectIx)

	def repcap_objectIx_get(self) -> repcap.ObjectIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	@property
	def subChannel(self):
		"""subChannel commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_subChannel'):
			from .SubChannel import SubChannelCls
			self._subChannel = SubChannelCls(self._core, self._cmd_group)
		return self._subChannel

	def clone(self) -> 'ObjectCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ObjectCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
