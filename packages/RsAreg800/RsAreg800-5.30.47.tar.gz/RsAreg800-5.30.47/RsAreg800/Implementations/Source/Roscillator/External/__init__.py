from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExternalCls:
	"""External commands group definition. 3 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("external", core, parent)

	@property
	def rfOff(self):
		"""rfOff commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rfOff'):
			from .RfOff import RfOffCls
			self._rfOff = RfOffCls(self._core, self._cmd_group)
		return self._rfOff

	# noinspection PyTypeChecker
	def get_frequency(self) -> enums.RoscFreqExtAreg800A:
		"""SCPI: [SOURce]:ROSCillator:EXTernal:FREQuency \n
		Snippet: value: enums.RoscFreqExtAreg800A = driver.source.roscillator.external.get_frequency() \n
		Sets the frequency of the external reference. \n
			:return: frequency: 10MHZ| 3200MHZ
		"""
		response = self._core.io.query_str('SOURce:ROSCillator:EXTernal:FREQuency?')
		return Conversions.str_to_scalar_enum(response, enums.RoscFreqExtAreg800A)

	def set_frequency(self, frequency: enums.RoscFreqExtAreg800A) -> None:
		"""SCPI: [SOURce]:ROSCillator:EXTernal:FREQuency \n
		Snippet: driver.source.roscillator.external.set_frequency(frequency = enums.RoscFreqExtAreg800A._10MHZ) \n
		Sets the frequency of the external reference. \n
			:param frequency: 10MHZ| 3200MHZ
		"""
		param = Conversions.enum_scalar_to_str(frequency, enums.RoscFreqExtAreg800A)
		self._core.io.write(f'SOURce:ROSCillator:EXTernal:FREQuency {param}')

	# noinspection PyTypeChecker
	def get_sbandwidth(self) -> enums.RoscBandWidtExt:
		"""SCPI: [SOURce]:ROSCillator:EXTernal:SBANdwidth \n
		Snippet: value: enums.RoscBandWidtExt = driver.source.roscillator.external.get_sbandwidth() \n
		Selects the synchronization bandwidth for the external reference signal. See [:SOURce]:ROSCillator:SOURce > External.
		Depending on the RF hardware version, and the installed options, the synchronization bandwidth varies.
		For more information, see data sheet. \n
			:return: sbandwidth: WIDE| NARRow NARRow The synchronization bandwidth is a few Hz. WIDE Uses the widest possible synchronization bandwidth.
		"""
		response = self._core.io.query_str('SOURce:ROSCillator:EXTernal:SBANdwidth?')
		return Conversions.str_to_scalar_enum(response, enums.RoscBandWidtExt)

	def set_sbandwidth(self, sbandwidth: enums.RoscBandWidtExt) -> None:
		"""SCPI: [SOURce]:ROSCillator:EXTernal:SBANdwidth \n
		Snippet: driver.source.roscillator.external.set_sbandwidth(sbandwidth = enums.RoscBandWidtExt.NARRow) \n
		Selects the synchronization bandwidth for the external reference signal. See [:SOURce]:ROSCillator:SOURce > External.
		Depending on the RF hardware version, and the installed options, the synchronization bandwidth varies.
		For more information, see data sheet. \n
			:param sbandwidth: WIDE| NARRow NARRow The synchronization bandwidth is a few Hz. WIDE Uses the widest possible synchronization bandwidth.
		"""
		param = Conversions.enum_scalar_to_str(sbandwidth, enums.RoscBandWidtExt)
		self._core.io.write(f'SOURce:ROSCillator:EXTernal:SBANdwidth {param}')

	def clone(self) -> 'ExternalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ExternalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
