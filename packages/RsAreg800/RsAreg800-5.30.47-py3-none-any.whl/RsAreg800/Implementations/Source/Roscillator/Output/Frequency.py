from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.RoscOutpFreqModeSmbb:
		"""SCPI: [SOURce]:ROSCillator:OUTPut:FREQuency:MODE \n
		Snippet: value: enums.RoscOutpFreqModeSmbb = driver.source.roscillator.output.frequency.get_mode() \n
		Selects the mode for the output reference frequency. \n
			:return: outp_freq_mode: DER10M| OFF DER10M Sets the output reference frequency to 10 MHz. The reference frequency is derived from the internal reference frequency. OFF Disables the output.
		"""
		response = self._core.io.query_str('SOURce:ROSCillator:OUTPut:FREQuency:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.RoscOutpFreqModeSmbb)

	def set_mode(self, outp_freq_mode: enums.RoscOutpFreqModeSmbb) -> None:
		"""SCPI: [SOURce]:ROSCillator:OUTPut:FREQuency:MODE \n
		Snippet: driver.source.roscillator.output.frequency.set_mode(outp_freq_mode = enums.RoscOutpFreqModeSmbb.DER10M) \n
		Selects the mode for the output reference frequency. \n
			:param outp_freq_mode: DER10M| OFF DER10M Sets the output reference frequency to 10 MHz. The reference frequency is derived from the internal reference frequency. OFF Disables the output.
		"""
		param = Conversions.enum_scalar_to_str(outp_freq_mode, enums.RoscOutpFreqModeSmbb)
		self._core.io.write(f'SOURce:ROSCillator:OUTPut:FREQuency:MODE {param}')
