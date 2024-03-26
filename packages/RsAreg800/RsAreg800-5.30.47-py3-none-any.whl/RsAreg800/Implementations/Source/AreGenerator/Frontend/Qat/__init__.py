from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class QatCls:
	"""Qat commands group definition. 28 total commands, 21 Subgroups, 0 group commands
	Repeated Capability: QatFrontent, default value after init: QatFrontent.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("qat", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_qatFrontent_get', 'repcap_qatFrontent_set', repcap.QatFrontent.Nr1)

	def repcap_qatFrontent_set(self, qatFrontent: repcap.QatFrontent) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to QatFrontent.Default
		Default value after init: QatFrontent.Nr1"""
		self._cmd_group.set_repcap_enum_value(qatFrontent)

	def repcap_qatFrontent_get(self) -> repcap.QatFrontent:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def add(self):
		"""add commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_add'):
			from .Add import AddCls
			self._add = AddCls(self._core, self._cmd_group)
		return self._add

	@property
	def alias(self):
		"""alias commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alias'):
			from .Alias import AliasCls
			self._alias = AliasCls(self._core, self._cmd_group)
		return self._alias

	@property
	def ats(self):
		"""ats commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ats'):
			from .Ats import AtsCls
			self._ats = AtsCls(self._core, self._cmd_group)
		return self._ats

	@property
	def bw(self):
		"""bw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bw'):
			from .Bw import BwCls
			self._bw = BwCls(self._core, self._cmd_group)
		return self._bw

	@property
	def cableCorr(self):
		"""cableCorr commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cableCorr'):
			from .CableCorr import CableCorrCls
			self._cableCorr = CableCorrCls(self._core, self._cmd_group)
		return self._cableCorr

	@property
	def center(self):
		"""center commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_center'):
			from .Center import CenterCls
			self._center = CenterCls(self._core, self._cmd_group)
		return self._center

	@property
	def channels(self):
		"""channels commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_channels'):
			from .Channels import ChannelsCls
			self._channels = ChannelsCls(self._core, self._cmd_group)
		return self._channels

	@property
	def connect(self):
		"""connect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_connect'):
			from .Connect import ConnectCls
			self._connect = ConnectCls(self._core, self._cmd_group)
		return self._connect

	@property
	def disconnect(self):
		"""disconnect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_disconnect'):
			from .Disconnect import DisconnectCls
			self._disconnect = DisconnectCls(self._core, self._cmd_group)
		return self._disconnect

	@property
	def hostname(self):
		"""hostname commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hostname'):
			from .Hostname import HostnameCls
			self._hostname = HostnameCls(self._core, self._cmd_group)
		return self._hostname

	@property
	def id(self):
		"""id commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_id'):
			from .Id import IdCls
			self._id = IdCls(self._core, self._cmd_group)
		return self._id

	@property
	def ipAddress(self):
		"""ipAddress commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ipAddress'):
			from .IpAddress import IpAddressCls
			self._ipAddress = IpAddressCls(self._core, self._cmd_group)
		return self._ipAddress

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def name(self):
		"""name commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_name'):
			from .Name import NameCls
			self._name = NameCls(self._core, self._cmd_group)
		return self._name

	@property
	def or(self):
		"""or commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_or'):
			from .Or import OrCls
			self._or = OrCls(self._core, self._cmd_group)
		return self._or

	@property
	def ota(self):
		"""ota commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ota'):
			from .Ota import OtaCls
			self._ota = OtaCls(self._core, self._cmd_group)
		return self._ota

	@property
	def rmv(self):
		"""rmv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rmv'):
			from .Rmv import RmvCls
			self._rmv = RmvCls(self._core, self._cmd_group)
		return self._rmv

	@property
	def rts(self):
		"""rts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rts'):
			from .Rts import RtsCls
			self._rts = RtsCls(self._core, self._cmd_group)
		return self._rts

	@property
	def snumber(self):
		"""snumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_snumber'):
			from .Snumber import SnumberCls
			self._snumber = SnumberCls(self._core, self._cmd_group)
		return self._snumber

	@property
	def status(self):
		"""status commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_status'):
			from .Status import StatusCls
			self._status = StatusCls(self._core, self._cmd_group)
		return self._status

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	def clone(self) -> 'QatCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = QatCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
