from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SensorCls:
	"""Sensor commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sensor", core, parent)

	def set(self, areg_pow_sen_selec: enums.AregPowSens, trxFrontent=repcap.TrxFrontent.Default) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:EIRP:SENSor \n
		Snippet: driver.source.areGenerator.frontend.trx.eirp.sensor.set(areg_pow_sen_selec = enums.AregPowSens.SEN1, trxFrontent = repcap.TrxFrontent.Default) \n
		Selects the R&S NRP power sensor connected to the TRX-type frontend for calculating the EIRP value. \n
			:param areg_pow_sen_selec: SEN4| SEN3| SEN2| SEN1| UDEFined SEN4|SEN3|SEN2|SEN1 Selects the respective R&S NRP power sensor for the TRX-type frontend. UDEFined No R&S NRP power sensor is connected to the TRX-type frontend.
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
		"""
		param = Conversions.enum_scalar_to_str(areg_pow_sen_selec, enums.AregPowSens)
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:EIRP:SENSor {param}')

	# noinspection PyTypeChecker
	def get(self, trxFrontent=repcap.TrxFrontent.Default) -> enums.AregPowSens:
		"""SCPI: [SOURce<HW>]:AREGenerator:FRONtend:TRX<CH>:EIRP:SENSor \n
		Snippet: value: enums.AregPowSens = driver.source.areGenerator.frontend.trx.eirp.sensor.get(trxFrontent = repcap.TrxFrontent.Default) \n
		Selects the R&S NRP power sensor connected to the TRX-type frontend for calculating the EIRP value. \n
			:param trxFrontent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trx')
			:return: areg_pow_sen_selec: SEN4| SEN3| SEN2| SEN1| UDEFined SEN4|SEN3|SEN2|SEN1 Selects the respective R&S NRP power sensor for the TRX-type frontend. UDEFined No R&S NRP power sensor is connected to the TRX-type frontend."""
		trxFrontent_cmd_val = self._cmd_group.get_repcap_cmd_value(trxFrontent, repcap.TrxFrontent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AREGenerator:FRONtend:TRX{trxFrontent_cmd_val}:EIRP:SENSor?')
		return Conversions.str_to_scalar_enum(response, enums.AregPowSens)
