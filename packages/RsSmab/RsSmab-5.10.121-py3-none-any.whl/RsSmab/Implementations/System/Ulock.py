from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UlockCls:
	"""Ulock commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ulock", core, parent)

	def set(self, sec_pass_word: str, mode: enums.DispKeybLockMode) -> None:
		"""SCPI: SYSTem:ULOCk \n
		Snippet: driver.system.ulock.set(sec_pass_word = 'abc', mode = enums.DispKeybLockMode.DISabled) \n
		Locks or unlocks the user interface of the instrument. \n
			:param sec_pass_word: No help available
			:param mode: ENABled| DONLy| DISabled| TOFF| VNConly ENABled Unlocks the display, the touchscreen and all controls for the manual operation. DONLy Locks the touchscreen and controls for the manual operation of the instrument. The display shows the current settings. VNConly Locks the touchscreen and controls for the manual operation, and enables remote operation over VNC. The display shows the current settings. TOFF Locks the touchscreen for the manual operation of the instrument. The display shows the current settings. DISabled Locks the display, the touchscreen and all controls for the manual operation.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sec_pass_word', sec_pass_word, DataType.String), ArgSingle('mode', mode, DataType.Enum, enums.DispKeybLockMode))
		self._core.io.write(f'SYSTem:ULOCk {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self) -> enums.DispKeybLockMode:
		"""SCPI: SYSTem:ULOCk \n
		Snippet: value: enums.DispKeybLockMode = driver.system.ulock.get() \n
		Locks or unlocks the user interface of the instrument. \n
			:return: mode: ENABled| DONLy| DISabled| TOFF| VNConly ENABled Unlocks the display, the touchscreen and all controls for the manual operation. DONLy Locks the touchscreen and controls for the manual operation of the instrument. The display shows the current settings. VNConly Locks the touchscreen and controls for the manual operation, and enables remote operation over VNC. The display shows the current settings. TOFF Locks the touchscreen for the manual operation of the instrument. The display shows the current settings. DISabled Locks the display, the touchscreen and all controls for the manual operation."""
		response = self._core.io.query_str(f'SYSTem:ULOCk?')
		return Conversions.str_to_scalar_enum(response, enums.DispKeybLockMode)
