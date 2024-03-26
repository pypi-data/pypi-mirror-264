from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiInstrumentCls:
	"""MultiInstrument commands group definition. 10 total commands, 3 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("multiInstrument", core, parent)

	@property
	def connect(self):
		"""connect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_connect'):
			from .Connect import ConnectCls
			self._connect = ConnectCls(self._core, self._cmd_group)
		return self._connect

	@property
	def remove(self):
		"""remove commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_remove'):
			from .Remove import RemoveCls
			self._remove = RemoveCls(self._core, self._cmd_group)
		return self._remove

	@property
	def secondary(self):
		"""secondary commands group. 4 Sub-classes, 2 commands."""
		if not hasattr(self, '_secondary'):
			from .Secondary import SecondaryCls
			self._secondary = SecondaryCls(self._core, self._cmd_group)
		return self._secondary

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AregMultiInstMode:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MULTiinstrument:MODE \n
		Snippet: value: enums.AregMultiInstMode = driver.source.areGenerator.osetup.multiInstrument.get_mode() \n
		Defines the operation mode of the R&S AREG800A in a multi-instrument setup. \n
			:return: mode: PRIMary| OFF| SECondary PRIMary The R&S AREG800A operates as a primary instrument. In this mode, the R&S AREG800A controls several R&S AREG800A instruments. OFF The R&S AREG800A operates in a standalone mode. SECondary Requires a control connection between this R&S AREG800A instrument and a primary R&S AREG800A instrument. The R&S AREG800A operates as a secondary instrument. In this mode, the R&S AREG800A is controlled by a primary R&S AREG800A instrument.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:MULTiinstrument:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AregMultiInstMode)

	def set_mode(self, mode: enums.AregMultiInstMode) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MULTiinstrument:MODE \n
		Snippet: driver.source.areGenerator.osetup.multiInstrument.set_mode(mode = enums.AregMultiInstMode.OFF) \n
		Defines the operation mode of the R&S AREG800A in a multi-instrument setup. \n
			:param mode: PRIMary| OFF| SECondary PRIMary The R&S AREG800A operates as a primary instrument. In this mode, the R&S AREG800A controls several R&S AREG800A instruments. OFF The R&S AREG800A operates in a standalone mode. SECondary Requires a control connection between this R&S AREG800A instrument and a primary R&S AREG800A instrument. The R&S AREG800A operates as a secondary instrument. In this mode, the R&S AREG800A is controlled by a primary R&S AREG800A instrument.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AregMultiInstMode)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:MULTiinstrument:MODE {param}')

	def get_primary(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MULTiinstrument:PRIMary \n
		Snippet: value: str = driver.source.areGenerator.osetup.multiInstrument.get_primary() \n
		No command help available \n
			:return: prim_syst_ctrl_add: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:MULTiinstrument:PRIMary?')
		return trim_str_response(response)

	def set_primary(self, prim_syst_ctrl_add: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MULTiinstrument:PRIMary \n
		Snippet: driver.source.areGenerator.osetup.multiInstrument.set_primary(prim_syst_ctrl_add = 'abc') \n
		No command help available \n
			:param prim_syst_ctrl_add: No help available
		"""
		param = Conversions.value_to_quoted_str(prim_syst_ctrl_add)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:MULTiinstrument:PRIMary {param}')

	def clone(self) -> 'MultiInstrumentCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiInstrumentCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
