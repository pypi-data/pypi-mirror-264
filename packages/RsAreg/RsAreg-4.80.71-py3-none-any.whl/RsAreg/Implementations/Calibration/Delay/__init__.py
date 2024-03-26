from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DelayCls:
	"""Delay commands group definition. 3 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delay", core, parent)

	@property
	def shutdown(self):
		"""shutdown commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_shutdown'):
			from .Shutdown import ShutdownCls
			self._shutdown = ShutdownCls(self._core, self._cmd_group)
		return self._shutdown

	def get_minutes(self) -> int:
		"""SCPI: CALibration:DELay:MINutes \n
		Snippet: value: int = driver.calibration.delay.get_minutes() \n
		No command help available \n
			:return: minutes: No help available
		"""
		response = self._core.io.query_str('CALibration:DELay:MINutes?')
		return Conversions.str_to_int(response)

	def set_minutes(self, minutes: int) -> None:
		"""SCPI: CALibration:DELay:MINutes \n
		Snippet: driver.calibration.delay.set_minutes(minutes = 1) \n
		No command help available \n
			:param minutes: No help available
		"""
		param = Conversions.decimal_value_to_str(minutes)
		self._core.io.write(f'CALibration:DELay:MINutes {param}')

	def get_measure(self) -> bool:
		"""SCPI: CALibration:DELay:[MEASure] \n
		Snippet: value: bool = driver.calibration.delay.get_measure() \n
		No command help available \n
			:return: error: No help available
		"""
		response = self._core.io.query_str('CALibration:DELay:MEASure?')
		return Conversions.str_to_bool(response)

	def clone(self) -> 'DelayCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DelayCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
