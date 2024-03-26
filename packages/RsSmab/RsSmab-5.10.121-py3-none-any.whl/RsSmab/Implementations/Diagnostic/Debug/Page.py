from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PageCls:
	"""Page commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("page", core, parent)

	def set(self) -> None:
		"""SCPI: DIAGnostic<HW>:DEBug:PAGE \n
		Snippet: driver.diagnostic.debug.page.set() \n
		No command help available \n
		"""
		self._core.io.write(f'DIAGnostic<HwInstance>:DEBug:PAGE')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: DIAGnostic<HW>:DEBug:PAGE \n
		Snippet: driver.diagnostic.debug.page.set_with_opc() \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmab.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'DIAGnostic<HwInstance>:DEBug:PAGE', opc_timeout_ms)

	def get_catalog(self) -> List[str]:
		"""SCPI: DIAGnostic<HW>:DEBug:PAGE:CATalog \n
		Snippet: value: List[str] = driver.diagnostic.debug.page.get_catalog() \n
		No command help available \n
			:return: diag_debug_page_id_cat: No help available
		"""
		response = self._core.io.query_str('DIAGnostic<HwInstance>:DEBug:PAGE:CATalog?')
		return Conversions.str_to_str_list(response)
