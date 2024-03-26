from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SystemCls:
	"""System commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("system", core, parent)

	# noinspection PyTypeChecker
	def get_alignment(self) -> enums.AregCconfigSystAlign:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:SYSTem:ALIGnment \n
		Snippet: value: enums.AregCconfigSystAlign = driver.source.areGenerator.channel.system.get_alignment() \n
		Enables the system alignment If the required option is available in the pre-configured system. \n
			:return: syst_align: OFF| TABLe| ON OFF Default state. No option installed. System alignment is not used. ON Requires R&S AREG8 -B97. System alignment is executed. All frontends included in the test setup are mapped according to the factory alignment. TABLe Requires R&S AREG8 -B98. System alignment is executed. Same mapping as for state'ON'. In addition, you can define a table of certain center frequencies and bandwidths for an additional alignment procedure which has an increased level linearity. The definitions in the table limit the possible settings for the radar sensor settings in the 'Sensor/DUT Config' dialog. The frontend center frequency is set read-only and selected according to the configured radar sensor frequency..
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:CHANnel:SYSTem:ALIGnment?')
		return Conversions.str_to_scalar_enum(response, enums.AregCconfigSystAlign)

	def set_alignment(self, syst_align: enums.AregCconfigSystAlign) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:CHANnel:SYSTem:ALIGnment \n
		Snippet: driver.source.areGenerator.channel.system.set_alignment(syst_align = enums.AregCconfigSystAlign.OFF) \n
		Enables the system alignment If the required option is available in the pre-configured system. \n
			:param syst_align: OFF| TABLe| ON OFF Default state. No option installed. System alignment is not used. ON Requires R&S AREG8 -B97. System alignment is executed. All frontends included in the test setup are mapped according to the factory alignment. TABLe Requires R&S AREG8 -B98. System alignment is executed. Same mapping as for state'ON'. In addition, you can define a table of certain center frequencies and bandwidths for an additional alignment procedure which has an increased level linearity. The definitions in the table limit the possible settings for the radar sensor settings in the 'Sensor/DUT Config' dialog. The frontend center frequency is set read-only and selected according to the configured radar sensor frequency..
		"""
		param = Conversions.enum_scalar_to_str(syst_align, enums.AregCconfigSystAlign)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:CHANnel:SYSTem:ALIGnment {param}')
