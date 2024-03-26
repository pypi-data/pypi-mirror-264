from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImportPyCls:
	"""ImportPy commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("importPy", core, parent)

	@property
	def predefined(self):
		"""predefined commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_predefined'):
			from .Predefined import PredefinedCls
			self._predefined = PredefinedCls(self._core, self._cmd_group)
		return self._predefined

	def set(self, import_filename: str, channel=repcap.Channel.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:CFE<CH>:ANTenna:CUSTom:IMPort \n
		Snippet: driver.source.areGenerator.frontend.cfe.antenna.custom.importPy.set(import_filename = 'abc', channel = repcap.Channel.Default) \n
		Imports an external list with file extension *.txt from a directory. The file format is a text file as comma-separated
		list with the list elements frequency, RX gain and TX gain. \n
			:param import_filename: string
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfe')
		"""
		param = Conversions.value_to_quoted_str(import_filename)
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:CFE{channel_cmd_val}:ANTenna:CUSTom:IMPort {param}')

	def clone(self) -> 'ImportPyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ImportPyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
