from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModeCls:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def set(self, areg_fe_trx_an_cust: enums.AregFconfUseCustAntAreg800, trxFrontent=repcap.TrxFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:ANTenna:CUSTom:[MODE] \n
		Snippet: driver.source.areGenerator.frontend.trx.antenna.custom.mode.set(areg_fe_trx_an_cust = enums.AregFconfUseCustAntAreg800.LIST, trxFrontent = repcap.TrxFrontent.Default) \n
		Sets the source for defining the antenna gain. \n
			:param areg_fe_trx_an_cust: NONe| LIST NONe The antenna gain for TX and RX is defined by the antenna mounted on the R&S AREG800A. LIST The antenna gain is defined in a list. Define frequency points manually in a table or import an external file with file extension *.csv or *.txt from a directory.
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
		"""
		param = Conversions.enum_scalar_to_str(areg_fe_trx_an_cust, enums.AregFconfUseCustAntAreg800)
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:ANTenna:CUSTom:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, trxFrontent=repcap.TrxFrontent.Default) -> enums.AregFconfUseCustAntAreg800:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:ANTenna:CUSTom:[MODE] \n
		Snippet: value: enums.AregFconfUseCustAntAreg800 = driver.source.areGenerator.frontend.trx.antenna.custom.mode.get(trxFrontent = repcap.TrxFrontent.Default) \n
		Sets the source for defining the antenna gain. \n
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:return: areg_fe_trx_an_cust: NONe| LIST NONe The antenna gain for TX and RX is defined by the antenna mounted on the R&S AREG800A. LIST The antenna gain is defined in a list. Define frequency points manually in a table or import an external file with file extension *.csv or *.txt from a directory."""
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:ANTenna:CUSTom:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AregFconfUseCustAntAreg800)
