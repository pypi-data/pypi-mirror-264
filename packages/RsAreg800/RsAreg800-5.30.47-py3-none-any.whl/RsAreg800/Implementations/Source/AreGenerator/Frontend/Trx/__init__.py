from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TrxCls:
	"""Trx commands group definition. 38 total commands, 14 Subgroups, 0 group commands
	Repeated Capability: TrxFrontent, default value after init: TrxFrontent.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trx", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_trxFrontent_get', 'repcap_trxFrontent_set', repcap.TrxFrontent.Nr1)

	def repcap_trxFrontent_set(self, trxFrontent: repcap.TrxFrontent) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TrxFrontent.Default
		Default value after init: TrxFrontent.Nr1"""
		self._cmd_group.set_repcap_enum_value(trxFrontent)

	def repcap_trxFrontent_get(self) -> repcap.TrxFrontent:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def alias(self):
		"""alias commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alias'):
			from .Alias import AliasCls
			self._alias = AliasCls(self._core, self._cmd_group)
		return self._alias

	@property
	def antenna(self):
		"""antenna commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_antenna'):
			from .Antenna import AntennaCls
			self._antenna = AntennaCls(self._core, self._cmd_group)
		return self._antenna

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
	def eirp(self):
		"""eirp commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_eirp'):
			from .Eirp import EirpCls
			self._eirp = EirpCls(self._core, self._cmd_group)
		return self._eirp

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .Gain import GainCls
			self._gain = GainCls(self._core, self._cmd_group)
		return self._gain

	@property
	def id(self):
		"""id commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_id'):
			from .Id import IdCls
			self._id = IdCls(self._core, self._cmd_group)
		return self._id

	@property
	def name(self):
		"""name commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_name'):
			from .Name import NameCls
			self._name = NameCls(self._core, self._cmd_group)
		return self._name

	@property
	def ota(self):
		"""ota commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ota'):
			from .Ota import OtaCls
			self._ota = OtaCls(self._core, self._cmd_group)
		return self._ota

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
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	def clone(self) -> 'TrxCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TrxCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
