from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, sec_pass_word: str, ftp_state: bool) -> None:
		"""SCPI: SYSTem:SECurity:NETWork:FTP:[STATe] \n
		Snippet: driver.system.security.network.ftp.state.set(sec_pass_word = 'abc', ftp_state = False) \n
		Disables FTP protocol for file transfer between the instrument and host. \n
			:param sec_pass_word: string Current security password.
			:param ftp_state: 1| ON| 0| OFF
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sec_pass_word', sec_pass_word, DataType.String), ArgSingle('ftp_state', ftp_state, DataType.Boolean))
		self._core.io.write(f'SYSTem:SECurity:NETWork:FTP:STATe {param}'.rstrip())

	def get(self) -> bool:
		"""SCPI: SYSTem:SECurity:NETWork:FTP:[STATe] \n
		Snippet: value: bool = driver.system.security.network.ftp.state.get() \n
		Disables FTP protocol for file transfer between the instrument and host. \n
			:return: ftp_state: 1| ON| 0| OFF"""
		response = self._core.io.query_str(f'SYSTem:SECurity:NETWork:FTP:STATe?')
		return Conversions.str_to_bool(response)
