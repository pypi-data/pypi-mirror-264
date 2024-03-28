from typing import Any, List, Dict
from pydantic import BaseModel, EmailStr, HttpUrl, PrivateAttr
from enum import Enum

class IAzioneEnum(str, Enum):
    ESEGUI = "ESEGUI"
    CARICO = "CARICO"
    
class ISmistamentoEnum(str, Enum):
    CONOSCENZA = "CONOSCENZA"
    COMPETENZA = "COMPETENZA"

    
class IConfig(BaseModel):
    wsUrl: str
    wsUser: str
    wsEnte: str
    wsPassword: str
    FAKE: bool = False
    FAKE_ERROR: str = ""
    
class BaseRet(BaseModel):
    lngErrNumber: int = 0
    strErrString: str = ''

class ILoginRet(BaseRet):
    strDST: str | None
    
class IResult(BaseRet):
    lngNumPG: int = 0
    lngAnnoPG: int = 0
    strDataPG: str = ''
    lngDocID: int = 0

    
class IPersona(BaseModel):
    IndirizzoTelematico: str
    Denominazione: str | None = None
    Nome: str | None = None
    Cognome: str | None = None
    TitoloDitta: str | None = None
    CodiceFiscaleDitta: str | None = None
    IndirizzoTelematicoDitta: str | None = None
    TipoMittente: str | None = None
    CodiceFiscale: str
    Titolo: str | None = None

class IDocumento(BaseModel):
    id: int | None
    descrizione: str
    tipo: str
    nome: str
    content: Any
    size: int
    mimetype: str
    ext: str


class IUser(BaseModel):
    username: str
    password: str

class IAmministrazione(BaseModel):
    Denominazione: str
    CodiceAOO: str
    CodiceEnte: str
    IndirizzoTelematico: EmailStr

class IFascicolo(BaseModel):
    numero: str
    anno:str
    
class IParametro(BaseModel):
    nome: str
    valore: str

class IProtocolloBase(BaseModel):
    Soggetto: List[IPersona]
    Flusso: str = 'E'
    Oggetto: str | None
    Titolario: str | None
    UO: str   | None
    Fascicolo: IFascicolo | None
    NumeroRegistrazione: str = '0'
    DataRegistrazione: str = '0'
    Parametri: List[IParametro]

class IProtocollo(IProtocolloBase):
    Amministrazione: IAmministrazione
    Principale: IDocumento
    Allegati: List[IDocumento]
    Applicativo: str = 'AGSPR'


class IMessageData(BaseModel):
    pass


