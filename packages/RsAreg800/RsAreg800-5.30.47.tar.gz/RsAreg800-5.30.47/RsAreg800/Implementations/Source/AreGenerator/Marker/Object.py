from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ObjectCls:
	"""Object commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("object", core, parent)

	def get_delay(self) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:MARKer:OBJect:DELay \n
		Snippet: value: int = driver.source.areGenerator.marker.object.get_delay() \n
		Sets a delay time for the start of the object marker. The delay time delays the marker signal at the marker output
		relative to the signal generation start. \n
			:return: obj_marker_delay: integer Range: -150000 to 150000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:MARKer:OBJect:DELay?')
		return Conversions.str_to_int(response)

	def set_delay(self, obj_marker_delay: int) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:MARKer:OBJect:DELay \n
		Snippet: driver.source.areGenerator.marker.object.set_delay(obj_marker_delay = 1) \n
		Sets a delay time for the start of the object marker. The delay time delays the marker signal at the marker output
		relative to the signal generation start. \n
			:param obj_marker_delay: integer Range: -150000 to 150000
		"""
		param = Conversions.decimal_value_to_str(obj_marker_delay)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:MARKer:OBJect:DELay {param}')

	def get_ontime(self) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:MARKer:OBJect:ONTime \n
		Snippet: value: float = driver.source.areGenerator.marker.object.get_ontime() \n
		Sets the on time (pulse width) of the object marker. \n
			:return: obj_marker_on_time: float Range: 10 to 150000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:MARKer:OBJect:ONTime?')
		return Conversions.str_to_float(response)

	def set_ontime(self, obj_marker_on_time: float) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:MARKer:OBJect:ONTime \n
		Snippet: driver.source.areGenerator.marker.object.set_ontime(obj_marker_on_time = 1.0) \n
		Sets the on time (pulse width) of the object marker. \n
			:param obj_marker_on_time: float Range: 10 to 150000
		"""
		param = Conversions.decimal_value_to_str(obj_marker_on_time)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:MARKer:OBJect:ONTime {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.AregObjMarkSource:
		"""SCPI: [SOURce<HW>]:AREGenerator:MARKer:OBJect:SOURce \n
		Snippet: value: enums.AregObjMarkSource = driver.source.areGenerator.marker.object.get_source() \n
		Sets the marker source used in the test setup. \n
			:return: obj_marker_source: SETTing| SCENario| HIL SETTing Sets the object marker after a change in the radar object settings. SCENario Requires: [:SOURcehw]:AREGenerator:OSETup:MODE DYNamic and [:SOURcehw]:AREGenerator:OSETup:SOURce SCENario. Sets the object marker at the restart of the replayed scenario. HIL Requires: [:SOURcehw]:AREGenerator:OSETup:MODE DYNamic. For [:SOURcehw]:AREGenerator:OSETup:SOURce HIL: requires [:SOURcehw]:AREGenerator:OSETup:PROTocol ZMQ|DCP|UDP. Sets the object marker according to a timestamp defined in the open simulation interface (OSI) protocol.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:MARKer:OBJect:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.AregObjMarkSource)

	def set_source(self, obj_marker_source: enums.AregObjMarkSource) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:MARKer:OBJect:SOURce \n
		Snippet: driver.source.areGenerator.marker.object.set_source(obj_marker_source = enums.AregObjMarkSource.HIL) \n
		Sets the marker source used in the test setup. \n
			:param obj_marker_source: SETTing| SCENario| HIL SETTing Sets the object marker after a change in the radar object settings. SCENario Requires: [:SOURcehw]:AREGenerator:OSETup:MODE DYNamic and [:SOURcehw]:AREGenerator:OSETup:SOURce SCENario. Sets the object marker at the restart of the replayed scenario. HIL Requires: [:SOURcehw]:AREGenerator:OSETup:MODE DYNamic. For [:SOURcehw]:AREGenerator:OSETup:SOURce HIL: requires [:SOURcehw]:AREGenerator:OSETup:PROTocol ZMQ|DCP|UDP. Sets the object marker according to a timestamp defined in the open simulation interface (OSI) protocol.
		"""
		param = Conversions.enum_scalar_to_str(obj_marker_source, enums.AregObjMarkSource)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:MARKer:OBJect:SOURce {param}')
