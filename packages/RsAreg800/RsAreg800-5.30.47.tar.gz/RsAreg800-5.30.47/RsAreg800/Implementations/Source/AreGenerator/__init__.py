from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AreGeneratorCls:
	"""AreGenerator commands group definition. 258 total commands, 17 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("areGenerator", core, parent)

	@property
	def osetup(self):
		"""osetup commands group. 5 Sub-classes, 9 commands."""
		if not hasattr(self, '_osetup'):
			from .Osetup import OsetupCls
			self._osetup = OsetupCls(self._core, self._cmd_group)
		return self._osetup

	@property
	def channel(self):
		"""channel commands group. 6 Sub-classes, 5 commands."""
		if not hasattr(self, '_channel'):
			from .Channel import ChannelCls
			self._channel = ChannelCls(self._core, self._cmd_group)
		return self._channel

	@property
	def dlogging(self):
		"""dlogging commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_dlogging'):
			from .Dlogging import DloggingCls
			self._dlogging = DloggingCls(self._core, self._cmd_group)
		return self._dlogging

	@property
	def frontend(self):
		"""frontend commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_frontend'):
			from .Frontend import FrontendCls
			self._frontend = FrontendCls(self._core, self._cmd_group)
		return self._frontend

	@property
	def hil(self):
		"""hil commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_hil'):
			from .Hil import HilCls
			self._hil = HilCls(self._core, self._cmd_group)
		return self._hil

	@property
	def last(self):
		"""last commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_last'):
			from .Last import LastCls
			self._last = LastCls(self._core, self._cmd_group)
		return self._last

	@property
	def mapping(self):
		"""mapping commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_mapping'):
			from .Mapping import MappingCls
			self._mapping = MappingCls(self._core, self._cmd_group)
		return self._mapping

	@property
	def marker(self):
		"""marker commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import MarkerCls
			self._marker = MarkerCls(self._core, self._cmd_group)
		return self._marker

	@property
	def measurement(self):
		"""measurement commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_measurement'):
			from .Measurement import MeasurementCls
			self._measurement = MeasurementCls(self._core, self._cmd_group)
		return self._measurement

	@property
	def object(self):
		"""object commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_object'):
			from .Object import ObjectCls
			self._object = ObjectCls(self._core, self._cmd_group)
		return self._object

	@property
	def objects(self):
		"""objects commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_objects'):
			from .Objects import ObjectsCls
			self._objects = ObjectsCls(self._core, self._cmd_group)
		return self._objects

	@property
	def omonitoring(self):
		"""omonitoring commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_omonitoring'):
			from .Omonitoring import OmonitoringCls
			self._omonitoring = OmonitoringCls(self._core, self._cmd_group)
		return self._omonitoring

	@property
	def radar(self):
		"""radar commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_radar'):
			from .Radar import RadarCls
			self._radar = RadarCls(self._core, self._cmd_group)
		return self._radar

	@property
	def scenario(self):
		"""scenario commands group. 4 Sub-classes, 5 commands."""
		if not hasattr(self, '_scenario'):
			from .Scenario import ScenarioCls
			self._scenario = ScenarioCls(self._core, self._cmd_group)
		return self._scenario

	@property
	def sensor(self):
		"""sensor commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_sensor'):
			from .Sensor import SensorCls
			self._sensor = SensorCls(self._core, self._cmd_group)
		return self._sensor

	@property
	def swunit(self):
		"""swunit commands group. 5 Sub-classes, 4 commands."""
		if not hasattr(self, '_swunit'):
			from .Swunit import SwunitCls
			self._swunit = SwunitCls(self._core, self._cmd_group)
		return self._swunit

	@property
	def units(self):
		"""units commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_units'):
			from .Units import UnitsCls
			self._units = UnitsCls(self._core, self._cmd_group)
		return self._units

	def clone(self) -> 'AreGeneratorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AreGeneratorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
