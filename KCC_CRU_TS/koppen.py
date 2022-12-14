#!python3


class Koppen:
    def __init__(self):
        print("Koppen: init")
        self.KOPPEN_CLASS_NAME = {
            "A": "Tropical",
            "B": "Dry",
            "C": "Temperate",
            "D": "Continental",
            "E": "Polar",
            "H": "Highland",
            "F": "Eternal frost",
            "S": "Steppe",
            "T": "Tundra",
            "W": "Desert",
            "a": "Hot summer",
            "b": "Warm summer",
            "c": "Cold summer",
            "d": "Very cold winter",
            "f": "No dry season",
            "z": "Rainforest",
            "h": "Hot",
            "k": "Cold",
            "m": "Monsoon",
            "s": "Dry summer",
            "w": "Dry winter",
            "?": "Unknown"
        }
        self.KOPPEN_FULL_NAME = {
            "Az": "Tropical rainforest",
            "Am": "Tropical monsoon",
            "As": "Tropical dry-summer savanna",
            "Aw": "Tropical dry-winter savanna",
            "BWh": "Arid hot desert",
            "BWk": "Arid cold desert",
            "BSh": "Semi-arid hot steppe",
            "BSk": "Semi-arid cold steppe",
            "Csa": "Hot-summer Mediterranean",
            "Csb": "Warm-summer Mediterranean",
            "Csc": "Cold-summer Mediterranean",
            "Cwa": "Monsoon subtropical",
            "Cwb": "Subtropical highland",
            "Cwc": "Cold subtropical highland",
            "Cfa": "Humid subtropical",
            "Cfb": "Temperate oceanic",
            "Cfc": "Subpolar oceanic",
            "Dsa": "Mediterranean hot-summer humid continental",
            "Dsb": "Mediterranean warm-summer humid continental",
            "Dsc": "Mediterranean subarctic",
            "Dsd": "Mediterranean extremely cold subarctic",
            "Dwa": "Monsoon hot-summer humid continental",
            "Dwb": "Monsoon warm-summer humid continental",
            "Dwc": "Monsoon subarctic",
            "Dwd": "Monsoon extremely cold subarctic",
            "Dfa": "Hot-summer humid continental",
            "Dfb": "Warm-summer humid continental",
            "Dfc": "Subarctic",
            "Dfd": "Extremely cold subarctic",
            "ET": "Tundra",
            "EF": "Ice cap",
            "H": "Highland"
        }
        self.KOPPEN_INDEX = {
            "Az": 0,
            "Am": 1,
            "As": 2,
            "Aw": 3,
            "BWh": 4,
            "BWk": 5,
            "BSh": 6,
            "BSk": 7,
            "Csa": 8,
            "Csb": 9,
            "Csc": 10,
            "Cwa": 11,
            "Cwb": 12,
            "Cwc": 13,
            "Cfa": 14,
            "Cfb": 15,
            "Cfc": 16,
            "Dsa": 17,
            "Dsb": 18,
            "Dsc": 19,
            "Dsd": 20,
            "Dwa": 21,
            "Dwb": 22,
            "Dwc": 23,
            "Dwd": 24,
            "Dfa": 25,
            "Dfb": 26,
            "Dfc": 27,
            "Dfd": 28,
            "ET": 29,
            "EF": 30,
            "H": 31
        }
        self.KOPPEN_COLOR = {
            "Az": "#0000FF",
            "Am": "#0077FF",
            "As": "#46A9FA",
            "Aw": "#46A9FA",
            "BWh": "#FF0000",
            "BWk": "#FF9695",
            "BSh": "#F5A301",
            "BSk": "#FFDB63",
            "Csa": "#FFFF00",
            "Csb": "#C6C700",
            "Csc": "#969600",
            "Cwa": "#96FF96",
            "Cwb": "#63C764",
            "Cwc": "#329633",
            "Cfa": "#C6FF4E",
            "Cfb": "#66FF33",
            "Cfc": "#33C701",
            "Dsa": "#FF00FF",
            "Dsb": "#C600C7",
            "Dsc": "#963295",
            "Dsd": "#966495",
            "Dwa": "#ABB1FF",
            "Dwb": "#5A77DB",
            "Dwc": "#4C51B5",
            "Dwd": "#320087",
            "Dfa": "#00FFFF",
            "Dfb": "#38C7FF",
            "Dfc": "#007E7D",
            "Dfd": "#00455E",
            "ET": "#B2B2B2",
            "EF": "#686868",
            "H": "#FFFFFF"
        }

    def get_classname(self, symbols):
        classname = ""
        for symbol in symbols:
            if symbol in self.KOPPEN_CLASS_NAME.keys():
                classname += self.KOPPEN_CLASS_NAME[symbol] + " "
        return classname

    def get_fullname(self, symbols: list):
        joined_symbols = "".join(symbols)
        fullname = ""
        if joined_symbols in self.KOPPEN_FULL_NAME.keys():
            fullname = self.KOPPEN_FULL_NAME[joined_symbols]
        return fullname

    def get_index(self, symbols: list):
        joined_symbols = "".join(symbols)
        return self.KOPPEN_INDEX[joined_symbols]

    def get_symbols(self, index: int):
        for key, value in self.KOPPEN_INDEX.items():
            if value == index:
                return key
        return ""

    def get_color(self, symbols):
        color = ""
        if symbols in self.KOPPEN_COLOR.keys():
            color = self.KOPPEN_COLOR[symbols]
        return color

    def compute_symbols(self, tmp: list, pre: list, lat):
        symbols = []
        max_tmp = max(tmp)
        min_tmp = min(tmp)
        avg_tmp_t = sum(tmp) / 12
        # tot_tmp = sum(tmp)
        # max_pre = max(pre)
        min_pre = min(pre)
        # avg_pre = sum(pre) / 12
        tot_pre_r = sum(pre)
        if lat >= 0:
            summer_pre = sum(pre[4:9])
            winter_pre = sum(pre[1:3]) + sum(pre[10:12])
        else:
            summer_pre = sum(pre[1:3]) + sum(pre[10:12])
            winter_pre = sum(pre[4:9])
        # A
        if self.__is_symbol_a(min_tmp):
            symbols.append("A")
            if lat >= 0:
                summer_min_pre = min(pre[4:9])
                winter_min_pre = min(min(pre[10:12]), min(pre[1:3]))
            else:
                summer_min_pre = min(min(pre[10:12]), min(pre[1:3]))
                winter_min_pre = min(pre[4:9])
            if self.__is_symbol_a_f(min_pre):
                symbols.append("z")
            elif self.__is_symbol_a_m(tot_pre_r, min_pre):
                symbols.append("m")
            elif self.__is_symbol_a_s(summer_min_pre):
                symbols.append("s")
            elif self.__is_symbol_a_w(winter_min_pre, tot_pre_r, min_pre):
                symbols.append("w")
            else:
                symbols.append("?")
        # B
        elif self.__is_symbol_b(avg_tmp_t, tot_pre_r, summer_pre, winter_pre):
            symbols.append("B")
            upper_limit = (20 * avg_tmp_t) + 280
            if self.__is_symbol_b_w(tot_pre_r, upper_limit):
                symbols.append("W")
                if self.__is_symbol_b_h(avg_tmp_t):
                    symbols.append("h")
                elif self.__is_symbol_b_k(avg_tmp_t):
                    symbols.append("k")
                else:
                    symbols.append("?")
            elif self.__is_symbol_b_s(tot_pre_r, upper_limit):
                symbols.append("S")
                if self.__is_symbol_b_h(avg_tmp_t):
                    symbols.append("h")
                elif self.__is_symbol_b_k(avg_tmp_t):
                    symbols.append("k")
                else:
                    symbols.append("?")
            else:
                symbols.append("?")
        # C
        elif self.__is_symbol_c(max_tmp, min_tmp):
            symbols.append("C")
            if lat >= 0:
                summer_min_pre = min(pre[4:9])
                summer_max_pre = max(pre[4:9])
                winter_min_pre = min(min(pre[10:12]), min(pre[1:3]))
                winter_max_pre = max(max(pre[10:12]), max(pre[1:3]))
            else:
                summer_min_pre = min(min(pre[10:12]), min(pre[1:3]))
                summer_max_pre = max(max(pre[10:12]), max(pre[1:3]))
                winter_min_pre = min(pre[4:9])
                winter_max_pre = max(pre[4:9])
            more_than_ten_c = 0
            for t in tmp:
                if t >= 10:
                    more_than_ten_c += 1
            if self.__is_symbol_c_s(summer_min_pre, winter_max_pre):
                symbols.append("s")
                if self.__is_symbol_c_a(max_tmp):
                    symbols.append("a")
                elif self.__is_symbol_c_b(more_than_ten_c, max_tmp):
                    symbols.append("b")
                elif self.__is_symbol_c_c(more_than_ten_c, max_tmp):
                    symbols.append("c")
                else:
                    symbols.append("?")
            elif self.__is_symbol_c_w(winter_min_pre, summer_max_pre):
                symbols.append("w")
                if self.__is_symbol_c_a(max_tmp):
                    symbols.append("a")
                elif self.__is_symbol_c_b(more_than_ten_c, max_tmp):
                    symbols.append("b")
                elif self.__is_symbol_c_c(more_than_ten_c, max_tmp):
                    symbols.append("c")
                else:
                    symbols.append("?")
            else:
                symbols.append("f")
                if self.__is_symbol_c_a(max_tmp):
                    symbols.append("a")
                elif self.__is_symbol_c_b(more_than_ten_c, max_tmp):
                    symbols.append("b")
                elif self.__is_symbol_c_c(more_than_ten_c, max_tmp):
                    symbols.append("c")
                else:
                    symbols.append("?")
        # D
        elif self.__is_symbol_d(max_tmp, min_tmp):
            symbols.append("D")
            if lat >= 0:
                summer_min_pre = min(pre[4:9])
                summer_max_pre = max(pre[4:9])
                winter_min_pre = min(min(pre[10:12]), min(pre[1:3]))
                winter_max_pre = max(max(pre[10:12]), max(pre[1:3]))
            else:
                summer_min_pre = min(min(pre[10:12]), min(pre[1:3]))
                summer_max_pre = max(max(pre[10:12]), max(pre[1:3]))
                winter_min_pre = min(pre[4:9])
                winter_max_pre = max(pre[4:9])
            more_than_ten_c = 0
            for t in tmp:
                if t >= 10:
                    more_than_ten_c += 1
            if self.__is_symbol_c_s(summer_min_pre, winter_max_pre):
                symbols.append("s")
                if self.__is_symbol_c_a(max_tmp):
                    symbols.append("a")
                elif self.__is_symbol_c_b(more_than_ten_c, max_tmp):
                    symbols.append("b")
                elif self.__is_symbol_c_c(more_than_ten_c, max_tmp):
                    symbols.append("c")
                elif self.__is_symbol_d_d(min_tmp):
                    symbols.append("d")
                else:
                    symbols.append("?")
            elif self.__is_symbol_c_w(winter_min_pre, summer_max_pre):
                symbols.append("w")
                if self.__is_symbol_c_a(max_tmp):
                    symbols.append("a")
                elif self.__is_symbol_c_b(more_than_ten_c, max_tmp):
                    symbols.append("b")
                elif self.__is_symbol_c_c(more_than_ten_c, max_tmp):
                    symbols.append("c")
                elif self.__is_symbol_d_d(min_tmp):
                    symbols.append("d")
                else:
                    symbols.append("?")
            else:
                symbols.append("f")
                if self.__is_symbol_c_a(max_tmp):
                    symbols.append("a")
                elif self.__is_symbol_c_b(more_than_ten_c, max_tmp):
                    symbols.append("b")
                elif self.__is_symbol_c_c(more_than_ten_c, max_tmp):
                    symbols.append("c")
                elif self.__is_symbol_d_d(min_tmp):
                    symbols.append("d")
                else:
                    symbols.append("?")
        # E
        elif self.__is_symbol_e(max_tmp):
            symbols.append("E")
            if self.__is_symbol_e_t(max_tmp):
                symbols.append("T")
            elif self.__is_symbol_e_f(max_tmp):
                symbols.append("F")
            else:
                symbols.append("?")
        # H
        else:
            symbols.append("H")
        return symbols

    # A ---------------------------------------------------------------------------------------------------
    @staticmethod
    def __is_symbol_a(min_tmp):
        if min_tmp >= 18:
            return True
        return False

    @staticmethod
    def __is_symbol_a_f(min_pre):
        if min_pre >= 60:
            return True
        return False

    @staticmethod
    def __is_symbol_a_m(tot_pre_r, min_pre):
        if 60 > min_pre >= 100 - (tot_pre_r / 25):
            return True
        return False

    @staticmethod
    def __is_symbol_a_s(summer_min_pre):
        if summer_min_pre < 60:
            return True
        return False

    @staticmethod
    def __is_symbol_a_w(winter_min_pre, tot_pre_r, min_pre):
        if winter_min_pre < 60:
            return True
        if min_pre < 60 and min_pre < 100 - (tot_pre_r / 25):
            return True
        return False

    # B ---------------------------------------------------------------------------------------------------
    @staticmethod
    def __is_symbol_b(avg_tmp_t, tot_pre_r, summer_pre, winter_pre):
        if summer_pre >= tot_pre_r * 0.7 and tot_pre_r < (20 * avg_tmp_t) + 280:
            return True
        elif winter_pre >= tot_pre_r * 0.7 and tot_pre_r < (20 * avg_tmp_t):
            return True
        elif (not summer_pre >= tot_pre_r * 0.7 and not winter_pre >= tot_pre_r * 0.7) \
                and tot_pre_r < (20 * avg_tmp_t) + 140:
            return True
        return False

    @staticmethod
    def __is_symbol_b_w(tot_pre_r, b_upper_limit):
        if tot_pre_r < b_upper_limit / 2:
            return True
        return False

    @staticmethod
    def __is_symbol_b_s(tot_pre_r, b_upper_limit):
        if b_upper_limit > tot_pre_r > b_upper_limit / 2:
            return True
        return False

    @staticmethod
    def __is_symbol_b_h(avg_tmp):
        if avg_tmp >= 18:
            return True
        return False

    @staticmethod
    def __is_symbol_b_k(avg_tmp):
        if avg_tmp < 18:
            return True
        return False

    # C ---------------------------------------------------------------------------------------------------
    @staticmethod
    def __is_symbol_c(max_tmp, min_tmp):
        if max_tmp >= 10 and 18 > min_tmp > -3:
            return True
        return False

    @staticmethod
    def __is_symbol_c_s(summer_min_pre, winter_max_pre):
        if summer_min_pre < 30 and summer_min_pre < winter_max_pre / 3:
            return True
        return False

    @staticmethod
    def __is_symbol_c_w(winter_min_pre, summer_max_pre):
        if winter_min_pre < summer_max_pre / 10:
            return True
        return False

    @staticmethod
    def __is_symbol_c_a(max_tmp):
        if max_tmp >= 22:
            return True
        return False

    @staticmethod
    def __is_symbol_c_b(more_than_ten_c, max_tmp):
        if more_than_ten_c >= 4 and max_tmp < 22:
            return True
        return False

    @staticmethod
    def __is_symbol_c_c(more_than_ten_c, max_tmp):
        if 1 <= more_than_ten_c <= 3 and max_tmp < 22:
            return True
        return False

    # D ---------------------------------------------------------------------------------------------------
    @staticmethod
    def __is_symbol_d(max_tmp, min_tmp):
        if max_tmp >= 10 and min_tmp <= -3:
            return True
        return False

    @staticmethod
    def __is_symbol_d_d(min_tmp):
        if min_tmp < -38:
            return True
        return False

    # E ---------------------------------------------------------------------------------------------------
    @staticmethod
    def __is_symbol_e(max_tmp):
        if max_tmp < 10:
            return True
        return False

    @staticmethod
    def __is_symbol_e_t(max_tmp):
        if 0 < max_tmp < 10:
            return True
        return False

    @staticmethod
    def __is_symbol_e_f(max_tmp):
        if max_tmp <= 0:
            return True
        return False
