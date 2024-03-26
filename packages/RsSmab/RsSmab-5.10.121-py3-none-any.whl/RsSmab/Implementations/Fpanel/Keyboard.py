from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class KeyboardCls:
	"""Keyboard commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("keyboard", core, parent)

	# noinspection PyTypeChecker
	def get_layout(self) -> enums.FrontPanelLayout:
		"""SCPI: FPANel:KEYBoard:LAYout \n
		Snippet: value: enums.FrontPanelLayout = driver.fpanel.keyboard.get_layout() \n
		No command help available \n
			:return: layout: No help available
		"""
		response = self._core.io.query_str('FPANel:KEYBoard:LAYout?')
		return Conversions.str_to_scalar_enum(response, enums.FrontPanelLayout)

	def set_layout(self, layout: enums.FrontPanelLayout) -> None:
		"""SCPI: FPANel:KEYBoard:LAYout \n
		Snippet: driver.fpanel.keyboard.set_layout(layout = enums.FrontPanelLayout.DIGits) \n
		No command help available \n
			:param layout: No help available
		"""
		param = Conversions.enum_scalar_to_str(layout, enums.FrontPanelLayout)
		self._core.io.write(f'FPANel:KEYBoard:LAYout {param}')
