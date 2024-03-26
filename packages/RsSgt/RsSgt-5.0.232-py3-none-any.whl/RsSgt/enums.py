from enum import Enum


# noinspection SpellCheckingInspection
class AttMode(Enum):
	"""3 Members, APASsive ... FIXed"""
	APASsive = 0
	AUTO = 1
	FIXed = 2


# noinspection SpellCheckingInspection
class BbSystemConfiguration(Enum):
	"""2 Members, AFETracking ... STANdard"""
	AFETracking = 0
	STANdard = 1


# noinspection SpellCheckingInspection
class CalPowDetAtt(Enum):
	"""4 Members, HIGH ... OFF"""
	HIGH = 0
	LOW = 1
	MED = 2
	OFF = 3


# noinspection SpellCheckingInspection
class FreqStepMode(Enum):
	"""2 Members, DECimal ... USER"""
	DECimal = 0
	USER = 1


# noinspection SpellCheckingInspection
class ImpG50G10K(Enum):
	"""2 Members, G10K ... G50"""
	G10K = 0
	G50 = 1


# noinspection SpellCheckingInspection
class InclExcl(Enum):
	"""2 Members, EXCLude ... INCLude"""
	EXCLude = 0
	INCLude = 1


# noinspection SpellCheckingInspection
class InputImpRf(Enum):
	"""3 Members, G10K ... G50"""
	G10K = 0
	G1K = 1
	G50 = 2


# noinspection SpellCheckingInspection
class IqMode(Enum):
	"""2 Members, ANALog ... BASeband"""
	ANALog = 0
	BASeband = 1


# noinspection SpellCheckingInspection
class OpMode(Enum):
	"""2 Members, BBBYpass ... NORMal"""
	BBBYpass = 0
	NORMal = 1


# noinspection SpellCheckingInspection
class PowAlcState(Enum):
	"""4 Members, _1 ... ON"""
	_1 = 0
	AUTO = 1
	OFF = 2
	ON = 3


# noinspection SpellCheckingInspection
class PowLevBehaviour(Enum):
	"""6 Members, AUTO ... USER"""
	AUTO = 0
	CVSWr = 1
	CWSWr = 2
	MONotone = 3
	UNINterrupted = 4
	USER = 5


# noinspection SpellCheckingInspection
class PowLevMode(Enum):
	"""4 Members, LOWDistortion ... USER"""
	LOWDistortion = 0
	LOWNoise = 1
	NORMal = 2
	USER = 3


# noinspection SpellCheckingInspection
class PowOutpPonMode(Enum):
	"""2 Members, OFF ... UNCHanged"""
	OFF = 0
	UNCHanged = 1


# noinspection SpellCheckingInspection
class PowRfOffMode(Enum):
	"""2 Members, FIXed ... MAX"""
	FIXed = 0
	MAX = 1


# noinspection SpellCheckingInspection
class PowSensWithUndef(Enum):
	"""9 Members, SENS1 ... UNDefined"""
	SENS1 = 0
	SENS2 = 1
	SENS3 = 2
	SENS4 = 3
	SENSor1 = 4
	SENSor2 = 5
	SENSor3 = 6
	SENSor4 = 7
	UNDefined = 8


# noinspection SpellCheckingInspection
class RefLoOutput(Enum):
	"""3 Members, LO ... REF"""
	LO = 0
	OFF = 1
	REF = 2


# noinspection SpellCheckingInspection
class RoscFreqExt(Enum):
	"""4 Members, _1000MHZ ... _13MHZ"""
	_1000MHZ = 0
	_100MHZ = 1
	_10MHZ = 2
	_13MHZ = 3


# noinspection SpellCheckingInspection
class SlopeType(Enum):
	"""2 Members, NEGative ... POSitive"""
	NEGative = 0
	POSitive = 1


# noinspection SpellCheckingInspection
class SourceInt(Enum):
	"""2 Members, EXTernal ... INTernal"""
	EXTernal = 0
	INTernal = 1


# noinspection SpellCheckingInspection
class Test(Enum):
	"""4 Members, _0 ... STOPped"""
	_0 = 0
	_1 = 1
	RUNning = 2
	STOPped = 3


# noinspection SpellCheckingInspection
class UserPlug(Enum):
	"""18 Members, CIN ... TRIGger"""
	CIN = 0
	COUT = 1
	HIGH = 2
	LOW = 3
	MARRived = 4
	MKR1 = 5
	MKR2 = 6
	MLATency = 7
	NEXT = 8
	PEMSource = 9
	PETRigger = 10
	PVOut = 11
	SIN = 12
	SNValid = 13
	SOUT = 14
	SVALid = 15
	TOUT = 16
	TRIGger = 17
