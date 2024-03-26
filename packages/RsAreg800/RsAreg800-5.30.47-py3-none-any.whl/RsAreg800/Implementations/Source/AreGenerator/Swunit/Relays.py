from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RelaysCls:
	"""Relays commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("relays", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:AREGenerator:SWUNit:RELays:CATalog \n
		Snippet: value: List[str] = driver.source.areGenerator.swunit.relays.get_catalog() \n
		Requires [:SOURce<hw>]:AREGenerator:OSETup:SWUNit[:STATe] 1. Queries all available relays of the switching unit. Lists
		all available relays as a comma-separated list. \n
			:return: areg_ext_sw_chan_rx_tx_cat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:SWUNit:RELays:CATalog?')
		return Conversions.str_to_str_list(response)
