from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CustomCls:
	"""Custom commands group definition. 14 total commands, 7 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("custom", core, parent)

	@property
	def flist(self):
		"""flist commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_flist'):
			from .Flist import FlistCls
			self._flist = FlistCls(self._core, self._cmd_group)
		return self._flist

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .FormatPy import FormatPyCls
			self._formatPy = FormatPyCls(self._core, self._cmd_group)
		return self._formatPy

	@property
	def fpoints(self):
		"""fpoints commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fpoints'):
			from .Fpoints import FpointsCls
			self._fpoints = FpointsCls(self._core, self._cmd_group)
		return self._fpoints

	@property
	def importPy(self):
		"""importPy commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_importPy'):
			from .ImportPy import ImportPyCls
			self._importPy = ImportPyCls(self._core, self._cmd_group)
		return self._importPy

	@property
	def rx(self):
		"""rx commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_rx'):
			from .Rx import RxCls
			self._rx = RxCls(self._core, self._cmd_group)
		return self._rx

	@property
	def tx(self):
		"""tx commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tx'):
			from .Tx import TxCls
			self._tx = TxCls(self._core, self._cmd_group)
		return self._tx

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	def export_file(self, export_filename: str, trxFrontent=repcap.TrxFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:ANTenna:CUSTom:EXPort \n
		Snippet: driver.source.areGenerator.frontend.trx.antenna.custom.export_file(export_filename = 'abc', trxFrontent = repcap.TrxFrontent.Default) \n
		Exports the defined frequency table to an external list file with file extension *.txt in a directory. \n
			:param export_filename: string
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
		"""
		param = Conversions.value_to_quoted_str(export_filename)
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:ANTenna:CUSTom:EXPort {param}')

	def clone(self) -> 'CustomCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CustomCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
