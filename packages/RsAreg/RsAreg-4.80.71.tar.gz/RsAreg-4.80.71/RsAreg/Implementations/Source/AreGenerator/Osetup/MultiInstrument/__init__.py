from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiInstrumentCls:
	"""MultiInstrument commands group definition. 5 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("multiInstrument", core, parent)

	@property
	def connect(self):
		"""connect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_connect'):
			from .Connect import ConnectCls
			self._connect = ConnectCls(self._core, self._cmd_group)
		return self._connect

	@property
	def remove(self):
		"""remove commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_remove'):
			from .Remove import RemoveCls
			self._remove = RemoveCls(self._core, self._cmd_group)
		return self._remove

	@property
	def secondary(self):
		"""secondary commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_secondary'):
			from .Secondary import SecondaryCls
			self._secondary = SecondaryCls(self._core, self._cmd_group)
		return self._secondary

	def clone(self) -> 'MultiInstrumentCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiInstrumentCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
