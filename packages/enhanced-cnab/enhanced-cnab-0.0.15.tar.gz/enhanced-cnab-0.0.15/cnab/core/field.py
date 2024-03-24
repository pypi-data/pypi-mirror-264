from typing import Union, List, Optional, Callable, TYPE_CHECKING
from decimal import Decimal
from datetime import date, time, datetime
from enum import Enum
from . import validators, formatter, exceptions

if TYPE_CHECKING:
    from cnab.base.registro_remessa import RegistroRemessa

class CNABFieldType(Enum):
    Decimal = 'decimal'
    Int = 'int'
    Alfa = 'alfa'
    Alfa2 = 'alfa2'
    Date = 'date'
    Time = 'time'
    DateReverse = 'dateReverse'

class CNABFieldValueError(Exception):
    pass

CNABFieldValueType = Union[str, date, time, datetime, int, float, Decimal]

class CNABField:
    name: str = ''
    length: int = 0
    validation: CNABFieldType
    default: Union[CNABFieldValueType, Callable[[], CNABFieldValueType]]
    required: bool
    validators: List = []
    precision: int = 0
    formatter = None
    
    registro: Optional["RegistroRemessa"] = None

    def get_real_length(self):
        # TODO: document here or change this?
        if self.validation == CNABFieldType.Decimal:
            return self.length + self.precision
        return self.length

    def __init__(
        self,
        length: int,
        validation: CNABFieldType,
        default: Union[CNABFieldValueType, Callable[[], CNABFieldValueType]],
        required: Optional[bool] = False,
        precision: Optional[int] = 0,
    ):
        self.length = length
        self.validation = validation
        self.default = default
        self.required = required
        self.precision = precision
        self.formatter = None

        self.registro = None

        self.validators = []
        if self.required:
            self.validators += [validators.validate_required]
        
        if self.validation == CNABFieldType.Int:
            self.validators += [validators.validate_integer]
            self.formatter = formatter.FormatterInteger(self)

        if self.validation == CNABFieldType.Decimal:
            self.validators += [validators.validate_decimal]
            self.formatter = formatter.FormatterDecimal(self)

        if self.validation == CNABFieldType.Alfa:
            self.formatter = formatter.FormatterAlfa(self)
            
        if self.validation == CNABFieldType.Alfa2:
            self.formatter = formatter.FormatterAlfa2(self)

        if self.validation == CNABFieldType.Date:
            self.validators += [validators.validate_date]
            self.formatter = formatter.FormatterDate(self)

        if self.validation == CNABFieldType.Time:
            self.validators += [validators.validate_date]
            self.formatter = formatter.FormatterTime(self)

        if not self.formatter:
            raise exceptions.CNABFieldTypeNotSupportedError(self.validation)
        
    def validate_value(self, value: CNABFieldValueType):
        for validator in self.validators:
            value = validator(value, self)
        return value

    def format_value(self, value: CNABFieldValueType):
        value = self.validate_value(value)
        return self.formatter.to_file(value)
    
    def value_from_file(self, value: str) -> CNABFieldValueType:
        return self.formatter.from_file(value)

class CNABCreatedDateField(CNABField):
    def __init__(
        self,
        length: int,
        validation: CNABFieldType,
        required: Optional[bool] = False,
        precision: Optional[int] = 2,
    ):
        super().__init__(
            length=length,
            validation=validation,
            required=required,
            precision=precision,
            default=lambda: datetime.now()
        )
