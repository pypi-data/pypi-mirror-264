from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SwunitCls:
	"""Swunit commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("swunit", core, parent)

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:SWUNit:[STATe] \n
		Snippet: value: bool = driver.source.areGenerator.osetup.swunit.get_state() \n
		Activates using a switching unit in the test setup, e.g. R&S OSP open switch and control platform. A switching unit in
		the test setup allows you to connect up to eight QAT channels to less than eight R&S AREG800A IF ports. \n
			:return: areg_oset_sw_unit: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:SWUNit:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, areg_oset_sw_unit: bool) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:SWUNit:[STATe] \n
		Snippet: driver.source.areGenerator.osetup.swunit.set_state(areg_oset_sw_unit = False) \n
		Activates using a switching unit in the test setup, e.g. R&S OSP open switch and control platform. A switching unit in
		the test setup allows you to connect up to eight QAT channels to less than eight R&S AREG800A IF ports. \n
			:param areg_oset_sw_unit: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(areg_oset_sw_unit)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:SWUNit:STATe {param}')
