from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SensorCls:
	"""Sensor commands group definition. 11 total commands, 11 Subgroups, 0 group commands
	Repeated Capability: Sensor, default value after init: Sensor.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sensor", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_sensor_get', 'repcap_sensor_set', repcap.Sensor.Nr1)

	def repcap_sensor_set(self, sensor: repcap.Sensor) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Sensor.Default
		Default value after init: Sensor.Nr1"""
		self._cmd_group.set_repcap_enum_value(sensor)

	def repcap_sensor_get(self) -> repcap.Sensor:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def add(self):
		"""add commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_add'):
			from .Add import AddCls
			self._add = AddCls(self._core, self._cmd_group)
		return self._add

	@property
	def alias(self):
		"""alias commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alias'):
			from .Alias import AliasCls
			self._alias = AliasCls(self._core, self._cmd_group)
		return self._alias

	@property
	def angle(self):
		"""angle commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_angle'):
			from .Angle import AngleCls
			self._angle = AngleCls(self._core, self._cmd_group)
		return self._angle

	@property
	def bw(self):
		"""bw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bw'):
			from .Bw import BwCls
			self._bw = BwCls(self._core, self._cmd_group)
		return self._bw

	@property
	def center(self):
		"""center commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_center'):
			from .Center import CenterCls
			self._center = CenterCls(self._core, self._cmd_group)
		return self._center

	@property
	def cfactor(self):
		"""cfactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cfactor'):
			from .Cfactor import CfactorCls
			self._cfactor = CfactorCls(self._core, self._cmd_group)
		return self._cfactor

	@property
	def count(self):
		"""count commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_count'):
			from .Count import CountCls
			self._count = CountCls(self._core, self._cmd_group)
		return self._count

	@property
	def distance(self):
		"""distance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_distance'):
			from .Distance import DistanceCls
			self._distance = DistanceCls(self._core, self._cmd_group)
		return self._distance

	@property
	def dynamic(self):
		"""dynamic commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dynamic'):
			from .Dynamic import DynamicCls
			self._dynamic = DynamicCls(self._core, self._cmd_group)
		return self._dynamic

	@property
	def id(self):
		"""id commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_id'):
			from .Id import IdCls
			self._id = IdCls(self._core, self._cmd_group)
		return self._id

	@property
	def rmv(self):
		"""rmv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rmv'):
			from .Rmv import RmvCls
			self._rmv = RmvCls(self._core, self._cmd_group)
		return self._rmv

	def clone(self) -> 'SensorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SensorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
