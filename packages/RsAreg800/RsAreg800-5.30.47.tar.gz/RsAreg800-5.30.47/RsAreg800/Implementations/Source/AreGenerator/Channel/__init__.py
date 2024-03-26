from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ChannelCls:
	"""Channel commands group definition. 13 total commands, 6 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("channel", core, parent)

	@property
	def condition(self):
		"""condition commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_condition'):
			from .Condition import ConditionCls
			self._condition = ConditionCls(self._core, self._cmd_group)
		return self._condition

	@property
	def inputPy(self):
		"""inputPy commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_inputPy'):
			from .InputPy import InputPyCls
			self._inputPy = InputPyCls(self._core, self._cmd_group)
		return self._inputPy

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .Level import LevelCls
			self._level = LevelCls(self._core, self._cmd_group)
		return self._level

	@property
	def optimization(self):
		"""optimization commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_optimization'):
			from .Optimization import OptimizationCls
			self._optimization = OptimizationCls(self._core, self._cmd_group)
		return self._optimization

	@property
	def output(self):
		"""output commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Output import OutputCls
			self._output = OutputCls(self._core, self._cmd_group)
		return self._output

	@property
	def system(self):
		"""system commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_system'):
			from .System import SystemCls
			self._system = SystemCls(self._core, self._cmd_group)
		return self._system

	# noinspection PyTypeChecker
	def get_bw(self) -> enums.AregCconfigBw:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:BW \n
		Snippet: value: enums.AregCconfigBw = driver.source.areGenerator.channel.get_bw() \n
		Queries the channel bandwidth. The channel bandwidth depends on the installed options. \n
			:return: areg_chan_bw: BW1G| BW2G| BW5G BW1G Bandwidth = 1 GHz BW1G2 Bandwidth = 2 GHz BW5G Bandwidth = 5 GHz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:CHANnel:BW?')
		return Conversions.str_to_scalar_enum(response, enums.AregCconfigBw)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:CATalog \n
		Snippet: value: List[str] = driver.source.areGenerator.channel.get_catalog() \n
		Queries the available channels and lists the respective channel IDs. \n
			:return: areg_cconf_cat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:CHANnel:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_id(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:ID \n
		Snippet: value: str = driver.source.areGenerator.channel.get_id() \n
		Displays the identification name of the radar channel. The radar channel is designated with a letter and a number, e.g.
		'A1'. \n
			:return: areg_chan_id: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:CHANnel:ID?')
		return trim_str_response(response)

	def get_name(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:NAME \n
		Snippet: value: str = driver.source.areGenerator.channel.get_name() \n
		Sets the alias of the radar channel, that is the channel name. \n
			:return: areg_channel_name: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:CHANnel:NAME?')
		return trim_str_response(response)

	def set_name(self, areg_channel_name: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:NAME \n
		Snippet: driver.source.areGenerator.channel.set_name(areg_channel_name = 'abc') \n
		Sets the alias of the radar channel, that is the channel name. \n
			:param areg_channel_name: string
		"""
		param = Conversions.value_to_quoted_str(areg_channel_name)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:CHANnel:NAME {param}')

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:[STATe] \n
		Snippet: value: bool = driver.source.areGenerator.channel.get_state() \n
		Acitvates the radar channel. \n
			:return: areg_chan_state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:CHANnel:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, areg_chan_state: bool) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:[STATe] \n
		Snippet: driver.source.areGenerator.channel.set_state(areg_chan_state = False) \n
		Acitvates the radar channel. \n
			:param areg_chan_state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(areg_chan_state)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:CHANnel:STATe {param}')

	def clone(self) -> 'ChannelCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ChannelCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
