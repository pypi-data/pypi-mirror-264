from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BwCls:
	"""Bw commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bw", core, parent)

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Apply import ApplyCls
			self._apply = ApplyCls(self._core, self._cmd_group)
		return self._apply

	# noinspection PyTypeChecker
	def get_value(self) -> enums.OsetupBw:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:BW \n
		Snippet: value: enums.OsetupBw = driver.source.areGenerator.osetup.bw.get_value() \n
		Sets the bandwidth of the IF output channel frequencies. \n
			:return: areg_osetup_bw: BW1G| BW2G| BW5G BW1G Sets the bandwidth to 1 MHz. BW2G Sets the bandwidth to 2 MHz. BW5G Sets the bandwidth to 5 MHz.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:BW?')
		return Conversions.str_to_scalar_enum(response, enums.OsetupBw)

	def set_value(self, areg_osetup_bw: enums.OsetupBw) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:BW \n
		Snippet: driver.source.areGenerator.osetup.bw.set_value(areg_osetup_bw = enums.OsetupBw.BW1G) \n
		Sets the bandwidth of the IF output channel frequencies. \n
			:param areg_osetup_bw: BW1G| BW2G| BW5G BW1G Sets the bandwidth to 1 MHz. BW2G Sets the bandwidth to 2 MHz. BW5G Sets the bandwidth to 5 MHz.
		"""
		param = Conversions.enum_scalar_to_str(areg_osetup_bw, enums.OsetupBw)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:BW {param}')

	def clone(self) -> 'BwCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BwCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
