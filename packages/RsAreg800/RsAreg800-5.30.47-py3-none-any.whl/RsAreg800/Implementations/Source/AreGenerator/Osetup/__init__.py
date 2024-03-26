from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OsetupCls:
	"""Osetup commands group definition. 24 total commands, 5 Subgroups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("osetup", core, parent)

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Apply import ApplyCls
			self._apply = ApplyCls(self._core, self._cmd_group)
		return self._apply

	@property
	def bw(self):
		"""bw commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_bw'):
			from .Bw import BwCls
			self._bw = BwCls(self._core, self._cmd_group)
		return self._bw

	@property
	def hil(self):
		"""hil commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hil'):
			from .Hil import HilCls
			self._hil = HilCls(self._core, self._cmd_group)
		return self._hil

	@property
	def multiInstrument(self):
		"""multiInstrument commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_multiInstrument'):
			from .MultiInstrument import MultiInstrumentCls
			self._multiInstrument = MultiInstrumentCls(self._core, self._cmd_group)
		return self._multiInstrument

	@property
	def swunit(self):
		"""swunit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_swunit'):
			from .Swunit import SwunitCls
			self._swunit = SwunitCls(self._core, self._cmd_group)
		return self._swunit

	# noinspection PyTypeChecker
	def get_config(self) -> enums.OsetupConfiguration:
		"""SCPI: SOURce<HW>:AREGenerator:OSETup:CONFig \n
		Snippet: value: enums.OsetupConfiguration = driver.source.areGenerator.osetup.get_config() \n
		Sets the configuration mode of the IF output channel. \n
			:return: mode_llm: STD| NR STD The IF output channel works in standard mode. NR Requires R&S AREG8-K814. The IF output channel works in FMCW near range mode. This setting provides low latency at the IF output and allows you to simulate minimum distances between frontend and DUT of the length of the air gap.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:CONFig?')
		return Conversions.str_to_scalar_enum(response, enums.OsetupConfiguration)

	def set_config(self, mode_llm: enums.OsetupConfiguration) -> None:
		"""SCPI: SOURce<HW>:AREGenerator:OSETup:CONFig \n
		Snippet: driver.source.areGenerator.osetup.set_config(mode_llm = enums.OsetupConfiguration.NR) \n
		Sets the configuration mode of the IF output channel. \n
			:param mode_llm: STD| NR STD The IF output channel works in standard mode. NR Requires R&S AREG8-K814. The IF output channel works in FMCW near range mode. This setting provides low latency at the IF output and allows you to simulate minimum distances between frontend and DUT of the length of the air gap.
		"""
		param = Conversions.enum_scalar_to_str(mode_llm, enums.OsetupConfiguration)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:CONFig {param}')

	def get_hostname(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:HOSTname \n
		Snippet: value: str = driver.source.areGenerator.osetup.get_hostname() \n
		Requires 'Data Source > HiL/ViL'. Sets the hostname of the R&S AREG800A for the hardware in the loop (HiL) or vehicle in
		the loop (ViL) scenario controller. \n
			:return: areg_osetup_ip_address: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:HOSTname?')
		return trim_str_response(response)

	def set_hostname(self, areg_osetup_ip_address: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:HOSTname \n
		Snippet: driver.source.areGenerator.osetup.set_hostname(areg_osetup_ip_address = 'abc') \n
		Requires 'Data Source > HiL/ViL'. Sets the hostname of the R&S AREG800A for the hardware in the loop (HiL) or vehicle in
		the loop (ViL) scenario controller. \n
			:param areg_osetup_ip_address: No help available
		"""
		param = Conversions.value_to_quoted_str(areg_osetup_ip_address)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:HOSTname {param}')

	def get_ip_address(self) -> str:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:IPADdress \n
		Snippet: value: str = driver.source.areGenerator.osetup.get_ip_address() \n
		Requires 'Data Source > HiL/ViL'. Sets the IP address of the R&S AREG800A for the hardware in the loop (HiL) or vehicle
		in the loop (ViL) scenario controller. \n
			:return: areg_osetup_ip_address: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:IPADdress?')
		return trim_str_response(response)

	def set_ip_address(self, areg_osetup_ip_address: str) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:IPADdress \n
		Snippet: driver.source.areGenerator.osetup.set_ip_address(areg_osetup_ip_address = 'abc') \n
		Requires 'Data Source > HiL/ViL'. Sets the IP address of the R&S AREG800A for the hardware in the loop (HiL) or vehicle
		in the loop (ViL) scenario controller. \n
			:param areg_osetup_ip_address: string Range: 0.0.0.0. to ff.ff.ff.ff
		"""
		param = Conversions.value_to_quoted_str(areg_osetup_ip_address)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:IPADdress {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.OsetupMode:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MODE \n
		Snippet: value: enums.OsetupMode = driver.source.areGenerator.osetup.get_mode() \n
		Define the operation setup mode. \n
			:return: areg_oset_mode: STATic| DYNamic STATic Simulates static radar objects. DYNamic Simulates dynamic radar objects.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.OsetupMode)

	def set_mode(self, areg_oset_mode: enums.OsetupMode) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:MODE \n
		Snippet: driver.source.areGenerator.osetup.set_mode(areg_oset_mode = enums.OsetupMode.DYNamic) \n
		Define the operation setup mode. \n
			:param areg_oset_mode: STATic| DYNamic STATic Simulates static radar objects. DYNamic Simulates dynamic radar objects.
		"""
		param = Conversions.enum_scalar_to_str(areg_oset_mode, enums.OsetupMode)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:MODE {param}')

	def get_port(self) -> int:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:PORT \n
		Snippet: value: int = driver.source.areGenerator.osetup.get_port() \n
		Requires 'Data Source > HiL/ViL'. Sets the host port of the instrument for the hardware in the loop (HiL) or vehicle in
		the loop (ViL) scenario controller. \n
			:return: areg_oset_port: integer Range: 0 to 64000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:PORT?')
		return Conversions.str_to_int(response)

	def set_port(self, areg_oset_port: int) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:PORT \n
		Snippet: driver.source.areGenerator.osetup.set_port(areg_oset_port = 1) \n
		Requires 'Data Source > HiL/ViL'. Sets the host port of the instrument for the hardware in the loop (HiL) or vehicle in
		the loop (ViL) scenario controller. \n
			:param areg_oset_port: integer Range: 0 to 64000
		"""
		param = Conversions.decimal_value_to_str(areg_oset_port)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:PORT {param}')

	# noinspection PyTypeChecker
	def get_protocol(self) -> enums.OsetupHilProtocol:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:PROTocol \n
		Snippet: value: enums.OsetupHilProtocol = driver.source.areGenerator.osetup.get_protocol() \n
		Sets the protocol type for protocol data of hardware in the loop (HiL) or vehicle in the loop (ViL) scenarios. \n
			:return: areg_oset_protocol: ZMQ| DCP| UDP| UDPR ZMQ Zero message queue (ZMQ) asynchronous messaging library. The expected payload is the SensorData defined in the open simulation interface (OSI) . DCP Distributed co-simulation protocol (DCP) . The expected payload is the SensorData defined in the open simulation interface (OSI) . UDP User datagram protocol (UDP) . The expected payload is the SensorData defined in the open simulation interface (OSI) . UDPR User datagram protocol (UDP) raw data. Raw is a Rohde & Schwarz proprietary format.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:PROTocol?')
		return Conversions.str_to_scalar_enum(response, enums.OsetupHilProtocol)

	def set_protocol(self, areg_oset_protocol: enums.OsetupHilProtocol) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:PROTocol \n
		Snippet: driver.source.areGenerator.osetup.set_protocol(areg_oset_protocol = enums.OsetupHilProtocol.DCP) \n
		Sets the protocol type for protocol data of hardware in the loop (HiL) or vehicle in the loop (ViL) scenarios. \n
			:param areg_oset_protocol: ZMQ| DCP| UDP| UDPR ZMQ Zero message queue (ZMQ) asynchronous messaging library. The expected payload is the SensorData defined in the open simulation interface (OSI) . DCP Distributed co-simulation protocol (DCP) . The expected payload is the SensorData defined in the open simulation interface (OSI) . UDP User datagram protocol (UDP) . The expected payload is the SensorData defined in the open simulation interface (OSI) . UDPR User datagram protocol (UDP) raw data. Raw is a Rohde & Schwarz proprietary format.
		"""
		param = Conversions.enum_scalar_to_str(areg_oset_protocol, enums.OsetupHilProtocol)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:PROTocol {param}')

	# noinspection PyTypeChecker
	def get_reference(self) -> enums.OsetupObjRef:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:REFerence \n
		Snippet: value: enums.OsetupObjRef = driver.source.areGenerator.osetup.get_reference() \n
		Sets the object reference. \n
			:return: areg_osetup_ref: ORIGin| MAPPed ORIGin Sets the object reference to the origin in the polar coordinates map. MAPPed Sets a mapped sensor as object reference.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:REFerence?')
		return Conversions.str_to_scalar_enum(response, enums.OsetupObjRef)

	def set_reference(self, areg_osetup_ref: enums.OsetupObjRef) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:REFerence \n
		Snippet: driver.source.areGenerator.osetup.set_reference(areg_osetup_ref = enums.OsetupObjRef.MAPPed) \n
		Sets the object reference. \n
			:param areg_osetup_ref: ORIGin| MAPPed ORIGin Sets the object reference to the origin in the polar coordinates map. MAPPed Sets a mapped sensor as object reference.
		"""
		param = Conversions.enum_scalar_to_str(areg_osetup_ref, enums.OsetupObjRef)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:REFerence {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.OsetupDataSource:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:SOURce \n
		Snippet: value: enums.OsetupDataSource = driver.source.areGenerator.osetup.get_source() \n
		Requires [:SOURce<hw>]:AREGenerator:OSETup:MODE DYNamic. Sets the data source for the dynamic operation. \n
			:return: areg_oset_source: SCENario| HIL SCENario Sets for dynamic radar object simulation scenarios. HIL Sets the data source to hardware in the loop (HiL) or vehicle in the loop (ViL) scenarios.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.OsetupDataSource)

	def set_source(self, areg_oset_source: enums.OsetupDataSource) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:SOURce \n
		Snippet: driver.source.areGenerator.osetup.set_source(areg_oset_source = enums.OsetupDataSource.HIL) \n
		Requires [:SOURce<hw>]:AREGenerator:OSETup:MODE DYNamic. Sets the data source for the dynamic operation. \n
			:param areg_oset_source: SCENario| HIL SCENario Sets for dynamic radar object simulation scenarios. HIL Sets the data source to hardware in the loop (HiL) or vehicle in the loop (ViL) scenarios.
		"""
		param = Conversions.enum_scalar_to_str(areg_oset_source, enums.OsetupDataSource)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:SOURce {param}')

	# noinspection PyTypeChecker
	def get_tbase(self) -> enums.AregSetupTimeBase:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:TBASe \n
		Snippet: value: enums.AregSetupTimeBase = driver.source.areGenerator.osetup.get_tbase() \n
		Sets the time base of the logged data. \n
			:return: setup_time_base: SYSTem| SIMulation SYSTem The system time from the setup menu serves as time base. SIMulation The time stamp from the used scenario, e.g. from an OSI message, serves as time base.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:OSETup:TBASe?')
		return Conversions.str_to_scalar_enum(response, enums.AregSetupTimeBase)

	def set_tbase(self, setup_time_base: enums.AregSetupTimeBase) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:OSETup:TBASe \n
		Snippet: driver.source.areGenerator.osetup.set_tbase(setup_time_base = enums.AregSetupTimeBase.SIMulation) \n
		Sets the time base of the logged data. \n
			:param setup_time_base: SYSTem| SIMulation SYSTem The system time from the setup menu serves as time base. SIMulation The time stamp from the used scenario, e.g. from an OSI message, serves as time base.
		"""
		param = Conversions.enum_scalar_to_str(setup_time_base, enums.AregSetupTimeBase)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:OSETup:TBASe {param}')

	def clone(self) -> 'OsetupCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OsetupCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
