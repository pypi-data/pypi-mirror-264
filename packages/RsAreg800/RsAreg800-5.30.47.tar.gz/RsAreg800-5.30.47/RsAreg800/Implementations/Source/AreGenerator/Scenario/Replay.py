from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReplayCls:
	"""Replay commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("replay", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ScenarioReplyMode:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:REPLay:[MODE] \n
		Snippet: value: enums.ScenarioReplyMode = driver.source.areGenerator.scenario.replay.get_mode() \n
		Defines, if the files are played once or continuously. Files are replayed within the defined start position and stop
		position. \n
			:return: scen_reply_mode: SINGle| LOOP SINGle Files are played once within the defined positions in the file. LOOP Files are played continuously within the defined positions in the file.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:SCENario:REPLay:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ScenarioReplyMode)

	def set_mode(self, scen_reply_mode: enums.ScenarioReplyMode) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:REPLay:[MODE] \n
		Snippet: driver.source.areGenerator.scenario.replay.set_mode(scen_reply_mode = enums.ScenarioReplyMode.LOOP) \n
		Defines, if the files are played once or continuously. Files are replayed within the defined start position and stop
		position. \n
			:param scen_reply_mode: SINGle| LOOP SINGle Files are played once within the defined positions in the file. LOOP Files are played continuously within the defined positions in the file.
		"""
		param = Conversions.enum_scalar_to_str(scen_reply_mode, enums.ScenarioReplyMode)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SCENario:REPLay:MODE {param}')
