from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EepromCls:
	"""Eeprom commands group definition. 4 total commands, 3 Subgroups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("eeprom", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def repcap_channel_set(self, channel: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._cmd_group.set_repcap_enum_value(channel)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def bidentifier(self):
		"""bidentifier commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_bidentifier'):
			from .Bidentifier import BidentifierCls
			self._bidentifier = BidentifierCls(self._core, self._cmd_group)
		return self._bidentifier

	@property
	def customize(self):
		"""customize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_customize'):
			from .Customize import CustomizeCls
			self._customize = CustomizeCls(self._core, self._cmd_group)
		return self._customize

	@property
	def data(self):
		"""data commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	def delete(self, channel=repcap.Channel.Default) -> None:
		"""SCPI: DIAGnostic<HW>:EEPRom<CH>:DELete \n
		Snippet: driver.diagnostic.eeprom.delete(channel = repcap.Channel.Default) \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eeprom')
		"""
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'DIAGnostic<HwInstance>:EEPRom{channel_cmd_val}:DELete')

	def delete_with_opc(self, channel=repcap.Channel.Default, opc_timeout_ms: int = -1) -> None:
		channel_cmd_val = self._cmd_group.get_repcap_cmd_value(channel, repcap.Channel)
		"""SCPI: DIAGnostic<HW>:EEPRom<CH>:DELete \n
		Snippet: driver.diagnostic.eeprom.delete_with_opc(channel = repcap.Channel.Default) \n
		No command help available \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsAreg.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eeprom')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'DIAGnostic<HwInstance>:EEPRom{channel_cmd_val}:DELete', opc_timeout_ms)

	def clone(self) -> 'EepromCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EepromCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
