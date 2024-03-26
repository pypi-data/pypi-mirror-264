from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OptimizationCls:
	"""Optimization commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("optimization", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AregCconfigOptMode:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:OPTimization:MODE \n
		Snippet: value: enums.AregCconfigOptMode = driver.source.areGenerator.channel.optimization.get_mode() \n
		Selects the optimization mode of the radar channel. \n
			:return: areg_chan_mode: FAST| QHIG FAST Fast optimization mode This mode compensates I/Q skews and is suitable in time sensitive environments and for narrowband signals. QHIG High-quality optimization mode This mode compensates I/Q skews and uses frequency response correction data. The mode generates flat signals over large bandwidth but requires longer setting time and leads to signal interruption.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:CHANnel:OPTimization:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AregCconfigOptMode)

	def set_mode(self, areg_chan_mode: enums.AregCconfigOptMode) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:OPTimization:MODE \n
		Snippet: driver.source.areGenerator.channel.optimization.set_mode(areg_chan_mode = enums.AregCconfigOptMode.FAST) \n
		Selects the optimization mode of the radar channel. \n
			:param areg_chan_mode: FAST| QHIG FAST Fast optimization mode This mode compensates I/Q skews and is suitable in time sensitive environments and for narrowband signals. QHIG High-quality optimization mode This mode compensates I/Q skews and uses frequency response correction data. The mode generates flat signals over large bandwidth but requires longer setting time and leads to signal interruption.
		"""
		param = Conversions.enum_scalar_to_str(areg_chan_mode, enums.AregCconfigOptMode)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:CHANnel:OPTimization:MODE {param}')
