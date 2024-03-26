from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SecondaryCls:
	"""Secondary commands group definition. 6 total commands, 4 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("secondary", core, parent)

	@property
	def add(self):
		"""add commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_add'):
			from .Add import AddCls
			self._add = AddCls(self._core, self._cmd_group)
		return self._add

	@property
	def connection(self):
		"""connection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_connection'):
			from .Connection import ConnectionCls
			self._connection = ConnectionCls(self._core, self._cmd_group)
		return self._connection

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Execute import ExecuteCls
			self._execute = ExecuteCls(self._core, self._cmd_group)
		return self._execute

	@property
	def remove(self):
		"""remove commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_remove'):
			from .Remove import RemoveCls
			self._remove = RemoveCls(self._core, self._cmd_group)
		return self._remove

	def get_hostname(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MULTiinstrument:SECondary:HOSTname \n
		Snippet: value: str = driver.source.areGenerator.osetup.multiInstrument.secondary.get_hostname() \n
		Sets the IP address or hostname of the secondary instrument. If you remove the secondary instrument, the firmware saves
		hostname of the secondary instrument for correct mapping. For example, if you want to add the secondary instrument again. \n
			:return: hostname: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:MULTiinstrument:SECondary:HOSTname?')
		return trim_str_response(response)

	def set_hostname(self, hostname: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MULTiinstrument:SECondary:HOSTname \n
		Snippet: driver.source.areGenerator.osetup.multiInstrument.secondary.set_hostname(hostname = 'abc') \n
		Sets the IP address or hostname of the secondary instrument. If you remove the secondary instrument, the firmware saves
		hostname of the secondary instrument for correct mapping. For example, if you want to add the secondary instrument again. \n
			:param hostname: string
		"""
		param = Conversions.value_to_quoted_str(hostname)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:MULTiinstrument:SECondary:HOSTname {param}')

	def get_value(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MULTiinstrument:SECondary \n
		Snippet: value: str = driver.source.areGenerator.osetup.multiInstrument.secondary.get_value() \n
		No command help available \n
			:return: sec_addr: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:MULTiinstrument:SECondary?')
		return trim_str_response(response)

	def set_value(self, sec_addr: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MULTiinstrument:SECondary \n
		Snippet: driver.source.areGenerator.osetup.multiInstrument.secondary.set_value(sec_addr = 'abc') \n
		No command help available \n
			:param sec_addr: No help available
		"""
		param = Conversions.value_to_quoted_str(sec_addr)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:MULTiinstrument:SECondary {param}')

	def clone(self) -> 'SecondaryCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SecondaryCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
