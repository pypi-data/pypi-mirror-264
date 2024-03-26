from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PortCls:
	"""Port commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("port", core, parent)

	def set(self, port: enums.AregMeasPort, trxFrontent=repcap.TrxFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:EIRP:PORT \n
		Snippet: driver.source.areGenerator.frontend.trx.eirp.port.set(port = enums.AregMeasPort.AUX, trxFrontent = repcap.TrxFrontent.Default) \n
		Selects the port of the connected R&S NRP power sensor for calculating the EIRP. \n
			:param port: POW| AUX POW The R&S NRP power sensor is connected to the 'RX power' port of the frontend. AUX The R&S NRP power sensor is connected to the 'Aux IF Out' port of the R&S AREG800A.
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
		"""
		param = Conversions.enum_scalar_to_str(port, enums.AregMeasPort)
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:EIRP:PORT {param}')

	# noinspection PyTypeChecker
	def get(self, trxFrontent=repcap.TrxFrontent.Default) -> enums.AregMeasPort:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:EIRP:PORT \n
		Snippet: value: enums.AregMeasPort = driver.source.areGenerator.frontend.trx.eirp.port.get(trxFrontent = repcap.TrxFrontent.Default) \n
		Selects the port of the connected R&S NRP power sensor for calculating the EIRP. \n
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:return: port: POW| AUX POW The R&S NRP power sensor is connected to the 'RX power' port of the frontend. AUX The R&S NRP power sensor is connected to the 'Aux IF Out' port of the R&S AREG800A."""
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:EIRP:PORT?')
		return Conversions.str_to_scalar_enum(response, enums.AregMeasPort)
