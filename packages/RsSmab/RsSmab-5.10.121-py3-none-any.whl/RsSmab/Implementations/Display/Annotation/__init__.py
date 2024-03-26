from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AnnotationCls:
	"""Annotation commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("annotation", core, parent)

	@property
	def amplitude(self):
		"""amplitude commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_amplitude'):
			from .Amplitude import AmplitudeCls
			self._amplitude = AmplitudeCls(self._core, self._cmd_group)
		return self._amplitude

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	def get_all(self) -> bool:
		"""SCPI: DISPlay:ANNotation:[ALL] \n
		Snippet: value: bool = driver.display.annotation.get_all() \n
		Displays asterisks instead of the level and frequency values in the status bar of the instrument. We recommend that you
		use this mode if you operate the instrument in remote control. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('DISPlay:ANNotation:ALL?')
		return Conversions.str_to_bool(response)

	def set_all(self, state: bool) -> None:
		"""SCPI: DISPlay:ANNotation:[ALL] \n
		Snippet: driver.display.annotation.set_all(state = False) \n
		Displays asterisks instead of the level and frequency values in the status bar of the instrument. We recommend that you
		use this mode if you operate the instrument in remote control. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'DISPlay:ANNotation:ALL {param}')

	def clone(self) -> 'AnnotationCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AnnotationCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
