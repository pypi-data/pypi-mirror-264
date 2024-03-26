from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LevelCls:
	"""Level commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	def get_measured(self) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:LEVel:MEASured \n
		Snippet: value: float = driver.source.areGenerator.channel.level.get_measured() \n
		No command help available \n
			:return: areg_chan_level: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:CHANnel:LEVel:MEASured?')
		return Conversions.str_to_float(response)
