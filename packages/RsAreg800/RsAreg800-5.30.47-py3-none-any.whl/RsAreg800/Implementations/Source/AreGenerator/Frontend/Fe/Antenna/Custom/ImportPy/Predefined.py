from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PredefinedCls:
	"""Predefined commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("predefined", core, parent)

	def set(self, import_filename: str, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:FE<CH>:ANTenna:CUSTom:IMPort:PREDefined \n
		Snippet: driver.source.areGenerator.frontend.fe.antenna.custom.importPy.predefined.set(import_filename = 'abc', channel = repcap.Channel.Default) \n
		Imports a predefined file for standard antennas, stored on the R&S AREG800A. \n
			:param import_filename: string
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fe')
		"""
		param = Conversions.value_to_quoted_str(import_filename)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:FE{channel_cmd_val}:ANTenna:CUSTom:IMPort:PREDefined {param}')
