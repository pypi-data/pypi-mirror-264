# ##################################################################
#
# Copyright 2023 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Pradeep Garre(pradeep.garre@teradata.com)
# Secondary Owner: Adithya Avvaru(adithya.avvaru@teradata.com)
#
#
# Version: 1.0
#
# ##################################################################
from sqlalchemy import func, literal_column, literal
from teradatamlspk.sql.column import Column
from teradataml.dataframe.sql import _SQLColumnExpression
from teradatasqlalchemy.types import INTEGER, DATE

# Suppressing the Validation in teradataml.
# Suppress the validation. PySpark accepts the columns in the form of a
# standalone Columns, i.e.,
# >>> from PySpark.sql.functions import col, sum
# >>> column_1 = col('x')
# >>> column_2 = col('y')
# >>> df.withColumn('new_column', sum(column1+column2).over(WindowSpec)
# Note that the above expression accepts Columns which are not bounded to
# any table. Since compilation is at run time in PySpark, if columns does not exist,
# the expression fails - BUT AT RUN TIME. On the other side, teradataml
# validates every thing before running it. To enable this behaviour,
# we are suppressing the validation.
from teradataml.common.utils import _Validators
from teradataml.dataframe.sql_functions import to_numeric
_Validators.skip_all = True
from sqlalchemy import literal_column, func, case, literal

_get_sqlalchemy_expr = lambda col: literal_column(col) if isinstance(col, str) else literal(col)
_get_tdml_col = lambda col: _SQLColumnExpression(_get_sqlalchemy_expr(col)) if isinstance(col, (str, int, float)) else col._tdml_column


class _TeradatamlspkFunction:
    """ Internal Base class for teradatamlspk Functions. """
    def __init__(self, *cols, **kwargs):
        self._params = {}
        self._params["cols"] = cols
        self._params["window_"] = None
        self._spark_vantage_function_mapper = {
            "pow": "power",
            "variance": "var",
            "var_pop": "var",
            "var_samp": "var",
            "stddev": "stddev_samp",
            "stddev_pop": "std",
            "first": "first_value",
            "last": "last_value",
            "any_value": "first_value",
            "count_distinct": "count",
            "sum_distinct": "sum",
            "sumDistinct": "sum"
        }
        self.alias_name = None

    def alias(self, *alias, **kwargs):
        self.alias_name = alias[0]
        return self

    def over(self, window_spec):
        self._params["window_"] = window_spec
        return self

    def get_window_params(self):
        return self._params["window_"].get_params()

    def is_window_aggregate(self):
        return self._params["window_"] is not None

    def get_columns(self):
        return self._params["cols"]

    def get_function_name(self):
        return self._spark_vantage_function_mapper.get(self.__class__.__name__, self.__class__.__name__)

    def get_func_expression(self, tdml_df):

        if self.is_window_aggregate():
            return self._get_tdml_column_expression(tdml_df)

        cols = []
        func_name = self.get_function_name()

        if isinstance(self._params["cols"][0], str):
            tdml_dataframe_column = tdml_df[self._params["cols"][0]]
        else:
            tdml_dataframe_column = self._params["cols"][0]._tdml_column

        if getattr(tdml_dataframe_column, func_name, None):
            return getattr(tdml_dataframe_column, func_name)(*(c._tdml_column if isinstance(c, Column) else c for c in self._params["cols"][1:]))

        for val in self._params["cols"]:
            if isinstance(val, Column):
                cols.append(literal_column(val.name))
            elif isinstance(val, (int, float)):
                cols.append(literal(val))
            else:
                cols.append(val)

        return getattr(func, func_name)(*cols)

    def _get_tdml_column_expression(self, tdml_df):
        """
        Function to get the teradataml DataFrame ColumnExpression for
        the corresponding window aggregates.
        """

        window_params = self.get_window_params()

        # Convert teradatamlspk ColumnExpression to teradataml ColumnExpression.
        if window_params["partition_columns"]:
            window_params["partition_columns"] = [col._tdml_column if isinstance(col, Column) else col
                                                  for col in window_params["partition_columns"]]

        if window_params["order_columns"]:
            window_params["order_columns"] = [col._tdml_column if isinstance(col, Column) else col
                                              for col in window_params["order_columns"]]

        columns_ = self.get_columns()

        # Get the column.
        # some functions do not have any column to act. In such cases, choose any column.
        col_s_ = columns_[0] if columns_ else tdml_df.columns[0]

        # Convert column to Column Expression
        col = tdml_df[col_s_] if isinstance(col_s_, str) else (col_s_._tdml_column if isinstance(col_s_, Column) else col_s_)

        # Window Aggregates Call.
        _window_obj = getattr(col, "window")(**window_params)
        return getattr(_window_obj, self.get_function_name())(*(c._tdml_column if isinstance(c, Column) else c for c in columns_[1:]))

col = lambda col: Column(tdml_column=_SQLColumnExpression(col))

column = lambda col: Column(tdml_column=_SQLColumnExpression(col))
lit = lambda col: Column(tdml_column=_SQLColumnExpression(literal(col)))
broadcast = lambda df: df
def coalesce(*cols):

    # cols can be a name of column or ColumnExpression. Prepare tdml column first.
    cols = [_SQLColumnExpression(col).expression if isinstance(col, str) else col._tdml_column.expression for col in cols]
    return Column(tdml_column=_SQLColumnExpression(func.coalesce(*cols)))

def input_file_name():
    raise NotImplementedError

isnan = lambda col: Column(tdml_column=(_SQLColumnExpression(col) if isinstance(col, str) else col._tdml_column).isna())
isnull = lambda col: Column(tdml_column=(_SQLColumnExpression(col) if isinstance(col, str) else col._tdml_column).isna())
monotonically_increasing_id = lambda : Column(tdml_column=_SQLColumnExpression('sum(1) over( rows unbounded preceding )'))
def named_struct(*cols):
    raise NotImplementedError
nanvl = lambda col1, col2: Column(tdml_column=_SQLColumnExpression(func.nvl(_get_tdml_col(col1).expression, _get_tdml_col(col2).expression)))
rand = lambda seed=0: Column(tdml_column=_SQLColumnExpression("cast(random(0,999999999) as float)/1000000000 (format '9.999999999')"))
randn = lambda seed=0: Column(tdml_column=_SQLColumnExpression("cast(random(0,999999999) as float)/1000000000 (format '9.999999999')"))
spark_partition_id = lambda: Column(tdml_column=_SQLColumnExpression("0"))
when = lambda condition, value: Column(tdml_column=_SQLColumnExpression(case((_get_tdml_col(condition).expression, value))))
bitwise_not = lambda col: Column(tdml_column=col._tdml_column.bitwise_not() if isinstance(col, Column) else _SQLColumnExpression(col).bitwise_not())
bitwiseNOT = lambda col: Column(tdml_column=col._tdml_column.bitwise_not() if isinstance(col, Column) else _SQLColumnExpression(col).bitwise_not())
expr = lambda str: Column(tdml_column=_SQLColumnExpression(str))
greatest = lambda *cols: Column(tdml_column=_get_tdml_col(cols[0]).greatest(*[_get_tdml_col(col) for col in cols[1:]]))
least = lambda *cols: Column(tdml_column=_get_tdml_col(cols[0]).least(*[_get_tdml_col(col) for col in cols[1:]]))
sqrt = lambda col: Column(tdml_column=_get_tdml_col(col).sqrt())
abs = lambda col: Column(tdml_column=_get_tdml_col(col).abs())
acos = lambda col: Column(tdml_column=_get_tdml_col(col).acos())
asin = lambda col: Column(tdml_column=_get_tdml_col(col).asin())
asinh = lambda col: Column(tdml_column=_get_tdml_col(col).asinh())
atan = lambda col: Column(tdml_column=_get_tdml_col(col).atan())
atanh = lambda col: Column(tdml_column=_get_tdml_col(col).atanh())
atan2 = lambda col1, col2: Column(tdml_column=_get_tdml_col(col2).atan2(_get_tdml_col(col1)))
bin = lambda col: Column(tdml_column=_get_tdml_col(col).to_byte().from_byte('base2'))
cbrt = lambda col: Column(tdml_column=_get_tdml_col(col).cbrt())
ceil = lambda col: Column(tdml_column=_get_tdml_col(col).ceil())
ceiling = lambda col: Column(tdml_column=_get_tdml_col(col).ceiling())
def conv(col):
    raise NotImplementedError
cos = lambda col: Column(tdml_column=_get_tdml_col(col).cos())
cosh = lambda col: Column(tdml_column=_get_tdml_col(col).cosh())
cot = lambda col: Column(tdml_column=(1/_get_tdml_col(col).tan()))
csc = lambda col: Column(tdml_column=(1/_get_tdml_col(col).sin()))
e = lambda: Column(tdml_column=_SQLColumnExpression(literal(2.718281828459045)))
exp = lambda col: Column(tdml_column=_get_tdml_col(col).exp())
expm1 = lambda col: Column(tdml_column=_get_tdml_col(col).exp()-1)
def factorial(col):
    raise NotImplementedError
floor = lambda col: Column(tdml_column=_get_tdml_col(col).floor())
hex = lambda col: Column(tdml_column=_get_tdml_col(col).floor().cast(INTEGER()).hex())
unhex = lambda col: Column(tdml_column=_get_tdml_col(col).unhex())
hypot = lambda col1, col2: Column(tdml_column=_get_tdml_col(col1).hypot(_get_tdml_col(col2)))
ln = lambda col: Column(tdml_column=_get_tdml_col(col).ln())
def log(arg1):
    raise NotImplementedError
log10 = lambda col: Column(tdml_column=_get_tdml_col(col).log10())
log1p = lambda col: Column(tdml_column=_get_tdml_col(col+1).ln())
log2 = log
negate = lambda col: Column(tdml_column=_get_tdml_col(col)*-1)
negative = lambda col: Column(tdml_column=_get_tdml_col(col)*-1)
pi = lambda: Column(tdml_column=_SQLColumnExpression(literal(3.141592653589793)))
pmod = lambda dividend, divisor: Column(tdml_column=(_get_tdml_col(dividend)) % (_get_tdml_col(divisor)))
positive = lambda col: Column(tdml_column=_get_tdml_col(col)*1)
pow = lambda col1, col2: Column(tdml_column=_get_tdml_col(col1).pow(_get_tdml_col(col2)))
power = lambda col1, col2: Column(tdml_column=_get_tdml_col(col1).pow(_get_tdml_col(col2)))
rint = lambda col: Column(tdml_column=_get_tdml_col(col).round(0))
round = lambda col, scale=0: Column(tdml_column=_get_tdml_col(col).round(scale) if scale >= 0 else _get_tdml_col(col).trunc())
bround = lambda col, scale=0: Column(tdml_column=_get_tdml_col(col).round(scale) if scale >= 0 else _get_tdml_col(col).trunc())
shiftleft = lambda col, numBits: Column(tdml_column=_get_tdml_col(col).shiftleft(numBits))
shiftright = lambda col, numBits: Column(tdml_column=_get_tdml_col(col).shiftright(numBits))
def shiftrightunsigned(col, numBits):
    raise NotImplementedError
sign = lambda col: Column(tdml_column=_SQLColumnExpression(case((_get_tdml_col(col).expression>=0, 1), else_=-1)))
signum = lambda col: Column(tdml_column=_SQLColumnExpression(case((_get_tdml_col(col).expression>=0, 1), else_=-1)))
sin = lambda col: Column(tdml_column=_get_tdml_col(col).sin())
sinh = lambda col: Column(tdml_column=_get_tdml_col(col).sinh())
tan = lambda col: Column(tdml_column=_get_tdml_col(col).tan())
tanh = lambda col: Column(tdml_column=_get_tdml_col(col).tanh())
toDegrees = lambda col: Column(tdml_column=_get_tdml_col(col).degrees())

# TODO: Ideal way is to write user defined function for all try-<arthimatic function> type functions.
try_add = lambda left, right: Column(tdml_column=_get_tdml_col(left) + _get_tdml_col(right))
try_avg = lambda col: Column(tdml_column=_get_tdml_col(col).avg())
try_divide = lambda left, right: Column(tdml_column=_get_tdml_col(left) / _get_tdml_col(right))
try_multiply = lambda left, right: Column(tdml_column=_get_tdml_col(left) * _get_tdml_col(right))
try_subtract = lambda left, right: Column(tdml_column=_get_tdml_col(left) - _get_tdml_col(right))
try_sum = lambda left: Column(tdml_column=_get_tdml_col(left).sum())

try_to_number = lambda col, format=None: Column(tdml_column=to_numeric(_get_tdml_col(col), format_ = format))
degrees = toDegrees
toRadians = lambda col: Column(tdml_column=_get_tdml_col(col).radians())
radians = toRadians
width_bucket = lambda v, min, max, numBucket: Column(tdml_column=_SQLColumnExpression(func.width_bucket(
    _get_tdml_col(v).expression, _get_tdml_col(min).expression, _get_tdml_col(max).expression, _get_tdml_col(numBucket).expression)))
add_months = lambda start, months: Column(tdml_column=_get_tdml_col(start).add_months(_get_tdml_col(months)))
def not_implemented(*args, **kwargs):
    raise NotImplementedError
def unknown(*args, **kwargs):
    raise NotImplementedError
convert_timezone = not_implemented
curdate = lambda : Column(tdml_column=_SQLColumnExpression(func.CURRENT_DATE()))
current_date = lambda : Column(tdml_column=_SQLColumnExpression(func.CURRENT_DATE()))
current_timestamp = lambda : Column(tdml_column=_SQLColumnExpression(func.CURRENT_TIMESTAMP()))
current_timezone = not_implemented
date_add = lambda start, days: Column(tdml_column=_SQLColumnExpression(literal_column("({}) + (nvl({}, 0)  * interval '1' DAY)".format(_get_tdml_col(start).compile(), _get_tdml_col(days).compile()))))
date_diff = lambda end, start: Column(tdml_column=_get_tdml_col(end) - _get_tdml_col(start))
date_format = lambda date, format: Column(tdml_column=_get_tdml_col(date).to_char(format))
date_from_unix_date = unknown
date_trunc = lambda format, timestamp: Column(tdml_column=_get_tdml_col(timestamp).trunc(formatter=format))
dateadd = date_add
datediff = date_diff
day = lambda col: Column(tdml_column=_get_tdml_col(col).day_of_month())
date_part = unknown
datepart = date_part
dayofmonth = lambda col: Column(tdml_column=_get_tdml_col(col).day_of_month())
dayofweek = lambda col: Column(tdml_column=_get_tdml_col(col).day_of_week())
dayofyear = lambda col: Column(tdml_column=_get_tdml_col(col).day_of_year())
extract = unknown
second = lambda col: Column(tdml_column=_get_tdml_col(col).second())
weekofyear = lambda col: Column(tdml_column=_get_tdml_col(col).week_of_year()+1)
year = lambda col: Column(tdml_column=_get_tdml_col(col).year())
quarter = lambda col: Column(tdml_column=_get_tdml_col(col).quarter_of_year())
month = lambda col: Column(tdml_column=_get_tdml_col(col).month_of_year())
last_day = lambda col: Column(tdml_column=_get_tdml_col(col).month_end())
localtimestamp = lambda: Column(tdml_column=_SQLColumnExpression(literal_column('CURRENT_TIMESTAMP AT LOCAL')))
make_dt_interval = unknown
make_interval = unknown
make_timestamp = unknown
make_timestamp_ltz = unknown
make_timestamp_ntz = unknown
make_ym_interval = unknown
minute = lambda col: Column(tdml_column=_get_tdml_col(col).minute())
months_between = lambda date1, date2, roundOff=True : Column(tdml_column=_get_tdml_col(date1).months_between(_get_tdml_col(date2))) \
    if not roundOff else Column(tdml_column=_get_tdml_col(date1).months_between(_get_tdml_col(date2)).round(8))
_day_names = {"Mon": "MONDAY", "Tue": "TUESDAY", "Wed": "WEDNESDAY", "Thu": "THURSDAY", "Fri": "FRIDAY", "Sat": "SATURDAY", "Sun": "SUNDAY"}
next_day = lambda date, dayOfWeek: Column(tdml_column=_get_tdml_col(date).next_day(_day_names[dayOfWeek]))
hour = lambda col: Column(tdml_column=_get_tdml_col(col).hour())
make_date = unknown
now = localtimestamp
from_unixtime = unknown
unix_timestamp = unknown
to_unix_timestamp = unknown
to_timestamp = unknown
to_timestamp_ltz = unknown
to_timestamp_ntz = unknown
to_date = lambda col, format=None: Column(tdml_column=_get_tdml_col(col).to_date(format)) if format else Column(tdml_column=_get_tdml_col(col).cast(DATE))
trunc = lambda date, format: Column(tdml_column=_get_tdml_col(date).trunc(formatter=format))
from_utc_timestamp = unknown
to_utc_timestamp = unknown
weekday = lambda col: Column(tdml_column=_get_tdml_col(col).day_of_week()-2)
window = unknown
session_window = unknown
timestamp_micros = unknown
timestamp_millis = unknown
timestamp_seconds = unknown
try_to_timestamp = unknown
unix_date = lambda col: Column(tdml_column=_SQLColumnExpression(_get_tdml_col(col).expression-func.to_date("1970-01-01", 'YYYY-MM-DD')))
unix_micros = unknown
unix_millis = unknown
unix_micros = unknown
window_time = unknown
array = not_implemented
array_contains = not_implemented
arrays_overlap = not_implemented
array_join = not_implemented
create_map = not_implemented
slice = not_implemented
concat = lambda *cols: Column(tdml_column=_get_tdml_col(cols[0]).concat("", *cols[1:]))
array_position = not_implemented
element_at = not_implemented
array_append = not_implemented
array_size = not_implemented
array_sort = not_implemented
array_insert = not_implemented
array_remove = not_implemented
array_prepend = not_implemented
array_distinct = not_implemented
array_intersect = not_implemented
array_union = not_implemented
array_except = not_implemented
array_compact = not_implemented
transform = not_implemented
exists = not_implemented
forall = not_implemented
filter = not_implemented
aggregate = not_implemented
zip_with = not_implemented
transform_keys = not_implemented
transform_values = not_implemented
map_filter = not_implemented
map_from_arrays = not_implemented
map_zip_with = not_implemented
explode = not_implemented
explode_outer = not_implemented
posexplode = not_implemented
posexplode_outer = not_implemented
inline = not_implemented
inline_outer = not_implemented
get = not_implemented
get_json_object = not_implemented
json_tuple = not_implemented
from_json = not_implemented
schema_of_json = not_implemented
to_json = not_implemented
json_array_length = not_implemented
json_object_keys = not_implemented
size = not_implemented
cardinality = not_implemented
struct = not_implemented
sort_array = not_implemented
array_max = not_implemented
array_min = not_implemented
shuffle = not_implemented
reverse = not_implemented
flatten = not_implemented
sequence = not_implemented
array_repeat = not_implemented
map_contains_key = not_implemented
map_keys = not_implemented
map_values = not_implemented
map_entries = not_implemented
map_from_entries = not_implemented
arrays_zip = not_implemented
map_concat = not_implemented
from_csv = not_implemented
schema_of_csv = not_implemented
str_to_map = not_implemented
to_csv = not_implemented
try_element_at = not_implemented
years = not_implemented
months = not_implemented
days = not_implemented
hours = not_implemented
bucket = not_implemented



def asc(col):

    # col can be a string or Column Object.
    if isinstance(col, str):
        return Column(tdml_column=_SQLColumnExpression(col).asc().nulls_first())
    return Column(tdml_column=col._tdml_column.asc().nulls_first())

asc_nulls_first = lambda col: asc(col)

def asc_nulls_last(col):
    # col can be a string or Column Object.
    if isinstance(col, str):
        return Column(tdml_column=_SQLColumnExpression(col).asc().nulls_last())
    return Column(tdml_column=col._tdml_column.asc().nulls_last())


def desc(col):

    # col can be a string or Column Object.
    if isinstance(col, str):
        return Column(tdml_column=_SQLColumnExpression(col).desc().nulls_last())
    return Column(tdml_column=col._tdml_column.desc().nulls_last())

def desc_nulls_first(col):

    # col can be a string or Column Object.
    if isinstance(col, str):
        return Column(tdml_column=_SQLColumnExpression(col).desc().nulls_first())
    return Column(tdml_column=col._tdml_column.desc().nulls_first())

desc_nulls_last = lambda col: desc(col)

avg = type("avg", (_TeradatamlspkFunction, ), {})
any_value = type("any_value", (_TeradatamlspkFunction, ), {})
row_number = type("row_number", (_TeradatamlspkFunction, ), {})
count = type("count", (_TeradatamlspkFunction, ), {})
rank = type("rank", (_TeradatamlspkFunction, ), {})
cume_dist = type("cume_dist", (_TeradatamlspkFunction, ), {})
dense_rank = type("dense_rank", (_TeradatamlspkFunction, ), {})
percent_rank = type("percent_rank", (_TeradatamlspkFunction, ), {})
max = type("max", (_TeradatamlspkFunction, ), {})
mean = type("mean", (_TeradatamlspkFunction, ), {})
min = type("min", (_TeradatamlspkFunction, ), {})
sum = type("sum", (_TeradatamlspkFunction, ), {})

class std(_TeradatamlspkFunction):
    def __init__(self, col):
        super().__init__(col, False, False)

stddev = std
stddev_samp = std

class stddev_pop(_TeradatamlspkFunction):
    def __init__(self, col):
        super().__init__(col, False, True)

class var_pop(_TeradatamlspkFunction):
    def __init__(self, col):
        super().__init__(col, False, True)

class var_samp(_TeradatamlspkFunction):
    def __init__(self, col):
        super().__init__(col, False, False)

variance = var_samp

class lag(_TeradatamlspkFunction):
    def __init__(self, col, offset=1, default=None):
        super().__init__(col, offset, default)

class lead(_TeradatamlspkFunction):
    def __init__(self, col, offset=1, default=None):
        super().__init__(col, offset, default)

class count_distinct(_TeradatamlspkFunction):
    def __init__(self, col, *cols):
        super().__init__(col, True)

countDistinct = count_distinct

class corr(_TeradatamlspkFunction):
    def __init__(self, col1, col2):
        super().__init__(col1, col2)

class covar_pop(_TeradatamlspkFunction):
    def __init__(self, col1, col2):
        super().__init__(col1, col2)

class covar_samp(_TeradatamlspkFunction):
    def __init__(self, col1, col2):
        super().__init__(col1, col2)

class first(_TeradatamlspkFunction):
    def __init__(self, col, ignorenulls=False):
        super().__init__(col)

class first_value(_TeradatamlspkFunction):
    def __init__(self, col, ignorenulls=False):
        super().__init__(col)

class last(_TeradatamlspkFunction):
    def __init__(self, col, ignorenulls=False):
        super().__init__(col)

class last_value(_TeradatamlspkFunction):
    def __init__(self, col, ignorenulls=False):
        super().__init__(col)

class regr_avgx(_TeradatamlspkFunction):
    def __init__(self, y, x):
        super().__init__(y, x)

class regr_avgy(_TeradatamlspkFunction):
    def __init__(self, y, x):
        super().__init__(y, x)

class regr_count(_TeradatamlspkFunction):
    def __init__(self, y, x):
        super().__init__(y, x)

class regr_intercept(_TeradatamlspkFunction):
    def __init__(self, y, x):
        super().__init__(y, x)

class regr_r2(_TeradatamlspkFunction):
    def __init__(self, y, x):
        super().__init__(y, x)

class regr_slope(_TeradatamlspkFunction):
    def __init__(self, y, x):
        super().__init__(y, x)

class regr_sxx(_TeradatamlspkFunction):
    def __init__(self, y, x):
        super().__init__(y, x)

class regr_sxy(_TeradatamlspkFunction):
    def __init__(self, y, x):
        super().__init__(y, x)

class regr_syy(_TeradatamlspkFunction):
    def __init__(self, y, x):
        super().__init__(y, x)

class sum_distinct(_TeradatamlspkFunction):
    def __init__(self, col):
        super().__init__(col, True)

class sumDistinct(_TeradatamlspkFunction):
    def __init__(self, col):
        super().__init__(col, True)

ascii = lambda col: Column(tdml_column=_get_tdml_col(col).substr(1,1).ascii())
base64 = unknown
btrim = lambda str, trim=lit(" "): Column(tdml_column=_get_tdml_col(str).trim(_get_tdml_col(trim)))
char = lambda col: Column(tdml_column=_get_tdml_col(col).char())
character_length = lambda str: Column(tdml_column=_get_tdml_col(str).character_length())
char_length = character_length
concat_ws = lambda sep, *cols: Column(tdml_column=_get_tdml_col(cols[0]).concat(sep, *cols[1:]))
contains = lambda left, right: Column(tdml_column=_get_tdml_col(left).str.contains(_get_tdml_col(right)))
decode = not_implemented
elt = unknown
encode = unknown
endswith = lambda str, suffix: Column(tdml_column=_SQLColumnExpression(case((_get_tdml_col(str).endswith(_get_tdml_col(suffix)).expression, 1), else_=0)))
find_in_set = unknown
format_number = lambda col, d: Column(tdml_column=_get_tdml_col(col).format("z"*19 if d ==0 else "z"*19+"."+"z"*d))
format_string = unknown
ilike = lambda str, pattern, escapeChar=None: Column(tdml_column=_SQLColumnExpression(case((_get_tdml_col(str).ilike(pattern).expression, 1), else_=0)))
initcap = lambda col: Column(tdml_column=_get_tdml_col(col).initcap())
instr = lambda str, substr: Column(tdml_column=_get_tdml_col(str).instr(substr, 1, 1))
lcase = lambda str: Column(tdml_column=_get_tdml_col(str).lower())
length = lambda col: Column(tdml_column=_get_tdml_col(col).length())
like = lambda str, pattern, escapeChar=None: Column(tdml_column=_SQLColumnExpression(case((_get_tdml_col(str).like(pattern).expression, 1), else_=0)))
lower = lcase
left = lambda str, len: Column(tdml_column=_get_tdml_col(str).left(_get_tdml_col(len)))
levenshtein = lambda left, right, threshold=None: Column(tdml_column=_get_tdml_col(left).edit_distance(_get_tdml_col(right)))
locate = lambda substr, str, pos = 1: Column(tdml_column=_get_tdml_col(str).instr(substr, pos))
lpad = lambda col, len, pad: Column(tdml_column=_get_tdml_col(col).lpad(len, pad))
ltrim = lambda col: Column(tdml_column=_get_tdml_col(col).ltrim())
mask = unknown
octet_length = unknown
parse_url = unknown
position = lambda substr, str, start = 1: Column(tdml_column=_get_tdml_col(str).instr(_get_tdml_col(substr), _get_tdml_col(start)))
printf = unknown
rlike = unknown
regexp = unknown
regexp_like = unknown
regexp_count = unknown
regexp_extract = unknown
regexp_extract_all = unknown
regexp_replace = lambda string, pattern, replacement: Column(tdml_column=_get_tdml_col(string).regexp_replace(pattern, replacement))
regexp_substr = lambda str, regexp: Column(tdml_column=_get_tdml_col(str).regexp_substr(regexp))
regexp_instr = lambda str, regexp, idx = 1: Column(tdml_column=_get_tdml_col(str).regexp_instr(regexp, idx))
replace = lambda src, search, replace='': Column(tdml_column=_get_tdml_col(src).oreplace(_get_tdml_col(search), _get_tdml_col(replace)))
right = lambda str, len: Column(tdml_column=_get_tdml_col(str).right(_get_tdml_col(len)))
ucase = lambda str: Column(tdml_column=_get_tdml_col(str).upper())
unbase64 = unknown
rpad = lambda col, len, pad: Column(tdml_column=_get_tdml_col(col).rpad(len, pad))
repeat = lambda col, n: Column(tdml_column=_get_tdml_col(col).concat("", *[_get_tdml_col(col) for i in range(n-1)]))
rtrim = lambda col: Column(tdml_column=_get_tdml_col(col).rtrim())
soundex = lambda col: Column(tdml_column=_get_tdml_col(col).soundex())
split = not_implemented
split_part = not_implemented
startswith = lambda str, prefix: Column(tdml_column=_SQLColumnExpression(case((_get_tdml_col(str).startswith(_get_tdml_col(prefix)).expression, 1), else_=0)))
substr = lambda str, pos, len=1:Column(tdml_column=_get_tdml_col(str).substr(pos, len))
substring = substr
substring_index = unknown
overlay = unknown
sentences = not_implemented
to_binary = unknown
to_char = lambda col, format: Column(tdml_column=_get_tdml_col(col).to_char(format))
to_number = lambda col, format: Column(tdml_column=_SQLColumnExpression(func.to_number(_get_tdml_col(col).expression, format)))
to_varchar = unknown
translate = lambda srcCol, matching, replace: Column(tdml_column=_get_tdml_col(srcCol).translate(matching, replace))
trim = lambda col: Column(tdml_column=_get_tdml_col(col).trim())
upper = lambda col: Column(tdml_column=_get_tdml_col(col).upper())
url_decode = unknown
url_encode = unknown
bit_count = unknown
bit_get = unknown
getbit = unknown
call_function = unknown
call_udf = unknown
pandas_udf = unknown
udf = unknown
udtf = unknown
unwrap_udt = unknown
aes_decrypt = unknown
aes_encrypt = unknown
bitmap_bit_position = unknown
bitmap_bucket_number = unknown
bitmap_construct_agg = unknown
bitmap_count = unknown
bitmap_or_agg = unknown
current_catalog = not_implemented
current_database = lambda : Column(tdml_column=_SQLColumnExpression(literal_column("USER")))
current_schema = lambda : Column(tdml_column=_SQLColumnExpression(literal_column("DATABASE")))
current_user = lambda : Column(tdml_column=_SQLColumnExpression(literal_column("USER")))
input_file_block_length = not_implemented
input_file_block_start = not_implemented
md5 = unknown
sha = unknown
sha1 = unknown
sha2 = unknown
crc32 = unknown
hash = unknown
xxhash64 = unknown
assert_true = unknown
raise_error = unknown
reflect = unknown
hll_sketch_estimate = unknown
hll_union = unknown
java_method = unknown
stack = unknown
try_aes_decrypt = unknown
typeof = unknown
user = lambda : Column(tdml_column=_SQLColumnExpression(literal_column("USER")))
version = unknown
equal_null = unknown
ifnull = lambda col1, col2: nanvl(col1, col2)
isnotnull = lambda col: Column(tdml_column=_get_tdml_col(col).notnull())
nullif = lambda col1, col2: Column(tdml_column=case((_get_tdml_col(col1).expression == _get_tdml_col(col2).expression, None), else_=_get_tdml_col(col1).expression))
nvl = lambda col1, col2: Column(tdml_column=_SQLColumnExpression(func.nvl(_get_tdml_col(col1).expression, _get_tdml_col(col2).expression)))
nvl2 = lambda col1, col2, col3: Column(tdml_column=_SQLColumnExpression(
    func.nvl2(_get_tdml_col(col1).expression, _get_tdml_col(col2).expression, _get_tdml_col(col3).expression)))
xpath = not_implemented
xpath_boolean = not_implemented
xpath_double = not_implemented
xpath_float = not_implemented
xpath_int = not_implemented
xpath_long = not_implemented
xpath_number = not_implemented
xpath_short = not_implemented
xpath_string = not_implemented