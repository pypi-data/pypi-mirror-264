from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HilCls:
	"""Hil commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hil", core, parent)

	# noinspection PyTypeChecker
	def get_upd(self) -> enums.AregHilUpdateMode:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:HIL:UPD \n
		Snippet: value: enums.AregHilUpdateMode = driver.source.areGenerator.osetup.hil.get_upd() \n
		Sets the update mode for the HiL interface. The timestamp is an optional part of the OSI packets. \n
			:return: upd_mode: IMMediate| TIMestamp IMMediate Updates the simulated objects immediately on arrival of the OSI packet. If there is a timestamp in the OSI packet, the timestamp is not regarded. TIMestamp Updates the simulated objetcts when the system time reaches the timestamp of the OSI packet.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:HIL:UPD?')
		return Conversions.str_to_scalar_enum(response, enums.AregHilUpdateMode)

	def set_upd(self, upd_mode: enums.AregHilUpdateMode) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:HIL:UPD \n
		Snippet: driver.source.areGenerator.osetup.hil.set_upd(upd_mode = enums.AregHilUpdateMode.IMMediate) \n
		Sets the update mode for the HiL interface. The timestamp is an optional part of the OSI packets. \n
			:param upd_mode: IMMediate| TIMestamp IMMediate Updates the simulated objects immediately on arrival of the OSI packet. If there is a timestamp in the OSI packet, the timestamp is not regarded. TIMestamp Updates the simulated objetcts when the system time reaches the timestamp of the OSI packet.
		"""
		param = Conversions.enum_scalar_to_str(upd_mode, enums.AregHilUpdateMode)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:HIL:UPD {param}')
