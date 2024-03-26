from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConnectorCls:
	"""Connector commands group definition. 8 total commands, 2 Subgroups, 0 group commands
	Repeated Capability: Connector, default value after init: Connector.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("connector", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_connector_get', 'repcap_connector_set', repcap.Connector.Nr1)

	def repcap_connector_set(self, connector: repcap.Connector) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Connector.Default
		Default value after init: Connector.Nr1"""
		self._cmd_group.set_repcap_enum_value(connector)

	def repcap_connector_get(self) -> repcap.Connector:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

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

	def clone(self) -> 'ConnectorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ConnectorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
