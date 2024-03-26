from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ShutdownCls:
	"""Shutdown commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("shutdown", core, parent)

	def get_state(self) -> bool:
		"""SCPI: CALibration:DELay:SHUTdown:[STATe] \n
		Snippet: value: bool = driver.calibration.delay.shutdown.get_state() \n
		Enables the instrument to shut down automatically after calibration. \n
			:return: shutdown: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('CALibration:DELay:SHUTdown:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, shutdown: bool) -> None:
		"""SCPI: CALibration:DELay:SHUTdown:[STATe] \n
		Snippet: driver.calibration.delay.shutdown.set_state(shutdown = False) \n
		Enables the instrument to shut down automatically after calibration. \n
			:param shutdown: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(shutdown)
		self._core.io.write(f'CALibration:DELay:SHUTdown:STATe {param}')
