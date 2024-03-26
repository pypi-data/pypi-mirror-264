from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FormatPyCls:
	"""FormatPy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("formatPy", core, parent)

	def set(self, areg_fe_trx_an_form: enums.CustAntFormat, trxFrontent=repcap.TrxFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:ANTenna:CUSTom:FORMat \n
		Snippet: driver.source.areGenerator.frontend.trx.antenna.custom.formatPy.set(areg_fe_trx_an_form = enums.CustAntFormat.CSV, trxFrontent = repcap.TrxFrontent.Default) \n
		No command help available \n
			:param areg_fe_trx_an_form: No help available
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
		"""
		param = Conversions.enum_scalar_to_str(areg_fe_trx_an_form, enums.CustAntFormat)
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:ANTenna:CUSTom:FORMat {param}')

	# noinspection PyTypeChecker
	def get(self, trxFrontent=repcap.TrxFrontent.Default) -> enums.CustAntFormat:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:ANTenna:CUSTom:FORMat \n
		Snippet: value: enums.CustAntFormat = driver.source.areGenerator.frontend.trx.antenna.custom.formatPy.get(trxFrontent = repcap.TrxFrontent.Default) \n
		No command help available \n
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:return: areg_fe_trx_an_form: No help available"""
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:ANTenna:CUSTom:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.CustAntFormat)
