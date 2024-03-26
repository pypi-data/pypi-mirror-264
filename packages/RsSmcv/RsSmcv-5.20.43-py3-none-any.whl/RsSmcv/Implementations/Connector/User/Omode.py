from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OmodeCls:
	"""Omode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("omode", core, parent)

	def set(self, omode: enums.SgtUserPlug, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: CONNector:USER<CH>:OMODe \n
		Snippet: driver.connector.user.omode.set(omode = enums.SgtUserPlug.CIN, userIx = repcap.UserIx.Default) \n
		No command help available \n
			:param omode: No help available
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.enum_scalar_to_str(omode, enums.SgtUserPlug)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'CONNector:USER{userIx_cmd_val}:OMODe {param}')

	# noinspection PyTypeChecker
	def get(self, userIx=repcap.UserIx.Default) -> enums.SgtUserPlug:
		"""SCPI: CONNector:USER<CH>:OMODe \n
		Snippet: value: enums.SgtUserPlug = driver.connector.user.omode.get(userIx = repcap.UserIx.Default) \n
		No command help available \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: omode: No help available"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'CONNector:USER{userIx_cmd_val}:OMODe?')
		return Conversions.str_to_scalar_enum(response, enums.SgtUserPlug)
