from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubChannelCls:
	"""SubChannel commands group definition. 7 total commands, 6 Subgroups, 0 group commands
	Repeated Capability: Subchannel, default value after init: Subchannel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("subChannel", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_subchannel_get', 'repcap_subchannel_set', repcap.Subchannel.Nr1)

	def repcap_subchannel_set(self, subchannel: repcap.Subchannel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Subchannel.Default
		Default value after init: Subchannel.Nr1"""
		self._cmd_group.set_repcap_enum_value(subchannel)

	def repcap_subchannel_get(self) -> repcap.Subchannel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def angle(self):
		"""angle commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_angle'):
			from .Angle import AngleCls
			self._angle = AngleCls(self._core, self._cmd_group)
		return self._angle

	@property
	def attenuation(self):
		"""attenuation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_attenuation'):
			from .Attenuation import AttenuationCls
			self._attenuation = AttenuationCls(self._core, self._cmd_group)
		return self._attenuation

	@property
	def doppler(self):
		"""doppler commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_doppler'):
			from .Doppler import DopplerCls
			self._doppler = DopplerCls(self._core, self._cmd_group)
		return self._doppler

	@property
	def range(self):
		"""range commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_range'):
			from .Range import RangeCls
			self._range = RangeCls(self._core, self._cmd_group)
		return self._range

	@property
	def rcs(self):
		"""rcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rcs'):
			from .Rcs import RcsCls
			self._rcs = RcsCls(self._core, self._cmd_group)
		return self._rcs

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'SubChannelCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SubChannelCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
