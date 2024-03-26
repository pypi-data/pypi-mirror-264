from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PredefinedCls:
	"""Predefined commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("predefined", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:ANTenna:CUSTom:IMPort:PREDefined:CATalog \n
		Snippet: value: List[str] = driver.source.areGenerator.frontend.antenna.custom.importPy.predefined.get_catalog() \n
		Queries all predefined files for standard antennas stored on the R&S AREG800A. \n
			:return: areg_fconf_antenna_gain_file_predefined_cat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:FRONtend:ANTenna:CUSTom:IMPort:PREDefined:CATalog?')
		return Conversions.str_to_str_list(response)
