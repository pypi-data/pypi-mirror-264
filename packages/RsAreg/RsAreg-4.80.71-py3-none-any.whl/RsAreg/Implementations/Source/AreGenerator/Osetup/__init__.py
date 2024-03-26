from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OsetupCls:
	"""Osetup commands group definition. 5 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("osetup", core, parent)

	@property
	def multiInstrument(self):
		"""multiInstrument commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_multiInstrument'):
			from .MultiInstrument import MultiInstrumentCls
			self._multiInstrument = MultiInstrumentCls(self._core, self._cmd_group)
		return self._multiInstrument

	def clone(self) -> 'OsetupCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OsetupCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
