from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FlistCls:
	"""Flist commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("flist", core, parent)

	@property
	def row(self):
		"""row commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_row'):
			from .Row import RowCls
			self._row = RowCls(self._core, self._cmd_group)
		return self._row

	def set(self, areg_fconf_use_cust_ant_freq_list: List[float], trxFrontent=repcap.TrxFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:ANTenna:CUSTom:FLISt \n
		Snippet: driver.source.areGenerator.frontend.trx.antenna.custom.flist.set(areg_fconf_use_cust_ant_freq_list = [1.1, 2.2, 3.3], trxFrontent = repcap.TrxFrontent.Default) \n
		For TRX-type frontend: Requires [:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>:ANTenna:CUSTom[:MODE] LIST. Sets the values
		for frequency in the list. Enter all values of the list separated by comma. \n
			:param areg_fconf_use_cust_ant_freq_list: No help available
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
		"""
		param = Conversions.list_to_csv_str(areg_fconf_use_cust_ant_freq_list)
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:ANTenna:CUSTom:FLISt {param}')

	def get(self, trxFrontent=repcap.TrxFrontent.Default) -> List[float]:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:ANTenna:CUSTom:FLISt \n
		Snippet: value: List[float] = driver.source.areGenerator.frontend.trx.antenna.custom.flist.get(trxFrontent = repcap.TrxFrontent.Default) \n
		For TRX-type frontend: Requires [:SOURce<hw>]:AREGenerator:FRONtend:TRX<ch>:ANTenna:CUSTom[:MODE] LIST. Sets the values
		for frequency in the list. Enter all values of the list separated by comma. \n
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:return: areg_fconf_use_cust_ant_freq_list: No help available"""
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		response = self._core.io.query_bin_or_ascii_float_list(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:ANTenna:CUSTom:FLISt?')
		return response

	def clone(self) -> 'FlistCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FlistCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
