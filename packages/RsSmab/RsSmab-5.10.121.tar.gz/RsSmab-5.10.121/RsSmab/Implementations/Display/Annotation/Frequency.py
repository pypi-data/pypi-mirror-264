from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrequencyCls:
	"""Frequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def set(self, sec_pass_word: str, state: bool) -> None:
		"""SCPI: DISPlay:ANNotation:FREQuency \n
		Snippet: driver.display.annotation.frequency.set(sec_pass_word = 'abc', state = False) \n
		Indicates asterisks instead of the frequency values in the status bar. \n
			:param sec_pass_word: No help available
			:param state: 1| ON| 0| OFF
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sec_pass_word', sec_pass_word, DataType.String), ArgSingle('state', state, DataType.Boolean))
		self._core.io.write(f'DISPlay:ANNotation:FREQuency {param}'.rstrip())

	# noinspection PyTypeChecker
	class FrequencyStruct(StructBase):
		"""Response structure. Fields: \n
			- Sec_Pass_Word: str: No parameter help available
			- State: bool: 1| ON| 0| OFF"""
		__meta_args_list = [
			ArgStruct.scalar_str('Sec_Pass_Word'),
			ArgStruct.scalar_bool('State')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sec_Pass_Word: str = None
			self.State: bool = None

	def get(self) -> FrequencyStruct:
		"""SCPI: DISPlay:ANNotation:FREQuency \n
		Snippet: value: FrequencyStruct = driver.display.annotation.frequency.get() \n
		Indicates asterisks instead of the frequency values in the status bar. \n
			:return: structure: for return value, see the help for FrequencyStruct structure arguments."""
		return self._core.io.query_struct(f'DISPlay:ANNotation:FREQuency?', self.__class__.FrequencyStruct())
