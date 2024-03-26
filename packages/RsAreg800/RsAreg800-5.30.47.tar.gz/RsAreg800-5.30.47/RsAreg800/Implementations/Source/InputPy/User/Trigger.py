from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TriggerCls:
	"""Trigger commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trigger", core, parent)

	# noinspection PyTypeChecker
	def get_impedance(self) -> enums.ImpG50G1KcoerceG10K:
		"""SCPI: [SOURce]:INPut:USER:TRIGger:IMPedance \n
		Snippet: value: enums.ImpG50G1KcoerceG10K = driver.source.inputPy.user.trigger.get_impedance() \n
		No command help available \n
			:return: impedance: No help available
		"""
		response = self._core.io.query_str('SOURce:INPut:USER:TRIGger:IMPedance?')
		return Conversions.str_to_scalar_enum(response, enums.ImpG50G1KcoerceG10K)

	def set_impedance(self, impedance: enums.ImpG50G1KcoerceG10K) -> None:
		"""SCPI: [SOURce]:INPut:USER:TRIGger:IMPedance \n
		Snippet: driver.source.inputPy.user.trigger.set_impedance(impedance = enums.ImpG50G1KcoerceG10K.G1K) \n
		No command help available \n
			:param impedance: No help available
		"""
		param = Conversions.enum_scalar_to_str(impedance, enums.ImpG50G1KcoerceG10K)
		self._core.io.write(f'SOURce:INPut:USER:TRIGger:IMPedance {param}')

	def get_level(self) -> float:
		"""SCPI: [SOURce]:INPut:USER:TRIGger:LEVel \n
		Snippet: value: float = driver.source.inputPy.user.trigger.get_level() \n
		No command help available \n
			:return: level: No help available
		"""
		response = self._core.io.query_str('SOURce:INPut:USER:TRIGger:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""SCPI: [SOURce]:INPut:USER:TRIGger:LEVel \n
		Snippet: driver.source.inputPy.user.trigger.set_level(level = 1.0) \n
		No command help available \n
			:param level: No help available
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce:INPut:USER:TRIGger:LEVel {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SlopeType:
		"""SCPI: [SOURce]:INPut:USER:TRIGger:SLOPe \n
		Snippet: value: enums.SlopeType = driver.source.inputPy.user.trigger.get_slope() \n
		No command help available \n
			:return: slope: No help available
		"""
		response = self._core.io.query_str('SOURce:INPut:USER:TRIGger:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SlopeType)

	def set_slope(self, slope: enums.SlopeType) -> None:
		"""SCPI: [SOURce]:INPut:USER:TRIGger:SLOPe \n
		Snippet: driver.source.inputPy.user.trigger.set_slope(slope = enums.SlopeType.NEGative) \n
		No command help available \n
			:param slope: No help available
		"""
		param = Conversions.enum_scalar_to_str(slope, enums.SlopeType)
		self._core.io.write(f'SOURce:INPut:USER:TRIGger:SLOPe {param}')
