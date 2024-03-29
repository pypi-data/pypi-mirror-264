__version__ = '0.0.1'
from bisect import bisect_left as _bisect_left, bisect_right as _bisect_right

_thirty_three_period = (1, 5, 9, 13, 17, 22, 26, 30)
_leap_remainders = set(_thirty_three_period)
_sh_acc_month_caps = (0, 31, 62, 93, 124, 155, 186, 216, 246, 276, 306, 336)
_g_acc_month_caps = (31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)


def sh_leap_count(sh_year: int) -> int:
    # 150 is the number of leaps from the year -621 SH to 0 SH.
    return (
        (sh_year // 33) * 8
        + _bisect_right(_thirty_three_period, (sh_year % 33))
        + 150
    )


def g_leap_count(g_year: int) -> int:
    return g_year // 4 - g_year // 100 + g_year // 400


def is_sh_leap(sh_year: int) -> bool:
    return (sh_year % 33) in _leap_remainders


def is_g_leap(gyear: int) -> bool:
    return gyear % 4 == 0 and (gyear % 100 != 0 or gyear % 400 == 0)


def g_day_of_year(g_year, g_month, g_day) -> int:
    if g_month == 1:
        return g_day
    if g_month == 2:
        return 31 + g_day
    return g_day + is_g_leap(g_year) + _g_acc_month_caps[g_month - 2]


Date = tuple[int, int, int]


def gregorian_to_solar_hijri(g_year: int, g_month: int, g_day: int) -> Date:
    sh_year = g_year - 622
    sh_day = g_day_of_year(g_year, g_month, g_day)

    last_year_day = g_leap_count(g_year - 1) - sh_leap_count(sh_year - 1) + 10

    dey_cap = 30 - last_year_day
    if sh_day <= dey_cap:
        return sh_year, 10, last_year_day + sh_day
    sh_day -= dey_cap

    if sh_day <= 30:
        return sh_year, 11, sh_day
    sh_day -= 30

    esf_cap = 30 if is_sh_leap(sh_year) else 29
    if sh_day <= esf_cap:
        return sh_year, 12, sh_day
    sh_day -= esf_cap

    sh_month = _bisect_left(_sh_acc_month_caps, sh_day)
    return sh_year + 1, sh_month, sh_day - _sh_acc_month_caps[sh_month - 1]


def sh_day_of_year(sh_month: int, sh_day: int) -> int:
    if sh_month <= 6:
        return (sh_month - 1) * 31 + sh_day
    return (6 * 31) + (sh_month - 7) * 30 + sh_day


_g_acc_month_caps_shifted = (0, 30, 61, 91, 122, 153, 183, 214, 244, 275, 306)


def solar_hijri_to_gregorian(sh_year: int, sh_month: int, sh_day: int) -> Date:
    g_year = sh_year + 621
    g_day = sh_day_of_year(sh_month, sh_day)

    last_year_day = sh_leap_count(sh_year - 1) - g_leap_count(g_year) + 20

    march_cap = 31 - last_year_day
    if g_day <= march_cap:
        return g_year, 3, last_year_day + g_day
    g_day -= march_cap

    month_index = _bisect_left(_g_acc_month_caps_shifted, g_day)

    if month_index < 10:  # before next gregorian year
        return (
            g_year,
            month_index + 3,
            g_day - _g_acc_month_caps_shifted[month_index - 1],
        )

    if month_index == 10:  # January of next gregorian year
        return g_year + 1, 1, g_day - 275

    if g_day <= 334:  # fits into a non-leap Feb.
        return g_year + 1, 2, g_day - 306

    g_day -= is_g_leap(g_year + 1)
    if g_day == 334:
        return g_year + 1, 2, 29

    return g_year + 1, 3, g_day - 334
