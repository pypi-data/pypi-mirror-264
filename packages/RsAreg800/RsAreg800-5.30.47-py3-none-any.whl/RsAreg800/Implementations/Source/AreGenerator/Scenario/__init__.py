from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScenarioCls:
	"""Scenario commands group definition. 12 total commands, 4 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scenario", core, parent)

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_file'):
			from .File import FileCls
			self._file = FileCls(self._core, self._cmd_group)
		return self._file

	@property
	def pause(self):
		"""pause commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pause'):
			from .Pause import PauseCls
			self._pause = PauseCls(self._core, self._cmd_group)
		return self._pause

	@property
	def position(self):
		"""position commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_position'):
			from .Position import PositionCls
			self._position = PositionCls(self._core, self._cmd_group)
		return self._position

	@property
	def replay(self):
		"""replay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_replay'):
			from .Replay import ReplayCls
			self._replay = ReplayCls(self._core, self._cmd_group)
		return self._replay

	def get_progress(self) -> float:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:PROGress \n
		Snippet: value: float = driver.source.areGenerator.scenario.get_progress() \n
		Queries the current position in time while playing the file.
		Query the current position via [:SOURce<hw>]:AREGenerator:SCENario:PROGress?. \n
			:return: scenario_progres: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:SCENario:PROGress?')
		return Conversions.str_to_float(response)

	def set_progress(self, scenario_progres: float) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:PROGress \n
		Snippet: driver.source.areGenerator.scenario.set_progress(scenario_progres = 1.0) \n
		Queries the current position in time while playing the file.
		Query the current position via [:SOURce<hw>]:AREGenerator:SCENario:PROGress?. \n
			:param scenario_progres: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(scenario_progres)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SCENario:PROGress {param}')

	def reset(self) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:RESet \n
		Snippet: driver.source.areGenerator.scenario.reset() \n
		Resets the Start, Stop and Position parameters of the replayed scenario. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SCENario:RESet')

	def reset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:RESet \n
		Snippet: driver.source.areGenerator.scenario.reset_with_opc() \n
		Resets the Start, Stop and Position parameters of the replayed scenario. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsAreg800.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:AREGenerator:SCENario:RESet', opc_timeout_ms)

	def start(self) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:STARt \n
		Snippet: driver.source.areGenerator.scenario.start() \n
		Starts the player. Plays the scenario file from the beginning. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SCENario:STARt')

	def start_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:STARt \n
		Snippet: driver.source.areGenerator.scenario.start_with_opc() \n
		Starts the player. Plays the scenario file from the beginning. \n
		Same as start, but waits for the operation to complete before continuing further. Use the RsAreg800.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:AREGenerator:SCENario:STARt', opc_timeout_ms)

	# noinspection PyTypeChecker
	def get_status(self) -> enums.ScenarioStatus:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:STATus \n
		Snippet: value: enums.ScenarioStatus = driver.source.areGenerator.scenario.get_status() \n
		Queries the status of the played scenario file. \n
			:return: scenario_status: RUNNing| STOPped RUNNing The replay of the scenario is ongoing. STOPped The replay of the scenario is stopped.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AREGenerator:SCENario:STATus?')
		return Conversions.str_to_scalar_enum(response, enums.ScenarioStatus)

	def set_status(self, scenario_status: enums.ScenarioStatus) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:STATus \n
		Snippet: driver.source.areGenerator.scenario.set_status(scenario_status = enums.ScenarioStatus.RUNNing) \n
		Queries the status of the played scenario file. \n
			:param scenario_status: RUNNing| STOPped RUNNing The replay of the scenario is ongoing. STOPped The replay of the scenario is stopped.
		"""
		param = Conversions.enum_scalar_to_str(scenario_status, enums.ScenarioStatus)
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SCENario:STATus {param}')

	def stop(self) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:STOP \n
		Snippet: driver.source.areGenerator.scenario.stop() \n
		Stops the player. After stopping, you can resume playing by [:SOURce<hw>]:AREGenerator:SCENario:STARt. The file plays
		from the start position. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:AREGenerator:SCENario:STOP')

	def stop_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:AREGenerator:SCENario:STOP \n
		Snippet: driver.source.areGenerator.scenario.stop_with_opc() \n
		Stops the player. After stopping, you can resume playing by [:SOURce<hw>]:AREGenerator:SCENario:STARt. The file plays
		from the start position. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsAreg800.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:AREGenerator:SCENario:STOP', opc_timeout_ms)

	def clone(self) -> 'ScenarioCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ScenarioCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
