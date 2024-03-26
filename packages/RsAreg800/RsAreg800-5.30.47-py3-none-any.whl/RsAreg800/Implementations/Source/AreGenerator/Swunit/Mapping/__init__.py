from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MappingCls:
	"""Mapping commands group definition. 1 total commands, 1 Subgroups, 0 group commands
	Repeated Capability: MappingChannel, default value after init: MappingChannel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mapping", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_mappingChannel_get', 'repcap_mappingChannel_set', repcap.MappingChannel.Nr1)

	def repcap_mappingChannel_set(self, mappingChannel: repcap.MappingChannel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to MappingChannel.Default
		Default value after init: MappingChannel.Nr1"""
		self._cmd_group.set_repcap_enum_value(mappingChannel)

	def repcap_mappingChannel_get(self) -> repcap.MappingChannel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def subChannel(self):
		"""subChannel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_subChannel'):
			from .SubChannel import SubChannelCls
			self._subChannel = SubChannelCls(self._core, self._cmd_group)
		return self._subChannel

	def clone(self) -> 'MappingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MappingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
