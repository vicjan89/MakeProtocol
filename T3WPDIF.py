from random import uniform
from cmath import rect, pi, phase


from pydantic import field_validator
from interfaces import Function
import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt, radians


class T3WPDIF(Function):

    INSTNAME: str = 'дифференциальная защита'
    Global_base_values: list
    GlobalBaseSelW1: int
    GlobalBaseSelW2: int
    GlobalBaseSelW3: int
    IdMin: float
    IdUnre: float
    EndSection1: float
    EndSection2: float
    SlopeSection2: float
    SlopeSection3: float
    I2_I1Ratio: float
    I5_I1Ratio: float
    step_iter: float = 0.1
    start_iter_torm: float = 0.0
    count_iter_IdUnre: int = 5
    C1W1: dict
    C2W1: dict
    C1W2: dict
    C2W2: dict
    C1W3: dict
    C2W3: dict


    @field_validator('IdMin')
    @classmethod
    def validate_IdMin(cls, v: float):
        assert 0.1 <= v <= 0.6, 'Параметр должен быть в диапазоне от 0.1 до 0.6'
        return v

    def diff(self, in_value: float):
        '''
        Расчёт уставки дифференциального тока
        :param in_value: тормозной ток в относительных единицах
        :return: уставка дифференциального тока в относительных единицах
        '''
        if 0 <= in_value < self.EndSection1:
            return self.IdMin
        elif in_value < self.EndSection2:
            return self.IdMin + self.SlopeSection2 * (in_value - self.EndSection1) / 100
        else:
            diff = self.IdMin + self.SlopeSection2 * (self.EndSection2 - self.EndSection1) / 100\
                   + self.SlopeSection3 * (in_value - self.EndSection2) / 100
            return diff if diff <= self.IdUnre else self.IdUnre

    # def diff_to_I1(self, diff: float) -> float:
    #     '''
    #     Расчёт тока прямой последовательности канала W1 для реализации заданного дифференциального тока
    #     :param diff: дифференциальный ток в относительных единицах
    #     '''
    #     return  diff * self.Global_base_values[self.GlobalBaseSelW1].IBase

    def set_diff_torm(self, diff: float, torm: float, mode: str ='1W1-1W2'):
        a = np.matrix([[2, -1, -1],
                      [-1, 2, -1],
                      [-1, -1, 2]])
        b = np.matrix([[1, -1, 0],
                      [0, 1, -1],
                      [-1, 0, 1]])
        torm_value = torm * self.Global_base_values[self.GlobalBaseSelW1-1].IBase
        i1 = np.matrix([[rect(torm_value, 0)],
                        [rect(torm_value, 2*pi/3)],
                        [rect(torm_value, 4*pi/3)]])
        diff_value = diff * self.Global_base_values[self.GlobalBaseSelW1-1].IBase
        id = np.matrix([[rect(diff_value, 0)],
                        [rect(diff_value, 2*pi/3)],
                        [rect(diff_value, 4*pi/3)]])
        x = (id - a * i1 / 3) / self.Global_base_values[self.GlobalBaseSelW2-1].UBase / sqrt(3) * self.Global_base_values[self.GlobalBaseSelW1-1].UBase
        i2 = b * x
        match mode:
            case '1W1-1W2':
                self.analog_inputs[self.C1W1['num']].channels[self.C1W1['l1']].v_prim = i1[0, 0]
                self.analog_inputs[self.C1W1['num']].channels[self.C1W1['l2']].v_prim = i1[1, 0]
                self.analog_inputs[self.C1W1['num']].channels[self.C1W1['l3']].v_prim = i1[2, 0]

                self.analog_inputs[self.C1W2['num']].channels[self.C1W2['l1']].v_prim = i2[0, 0]
                self.analog_inputs[self.C1W2['num']].channels[self.C1W2['l2']].v_prim = i2[1, 0]
                self.analog_inputs[self.C1W2['num']].channels[self.C1W2['l3']].v_prim = i2[2, 0]


    def get_diff_torm(self):
        '''
        Возвращает значения дифференциального и тормозного тока в относительных единицах для занчений выставленных
        на аналоговых входах
        '''
        a = np.matrix([[2, -1, -1],
                       [-1, 2, -1],
                       [-1, -1, 2]]) / 3
        b = np.matrix([[1, 0, -1],
                       [-1, 1, 0],
                       [0, -1, 1]]) / np.sqrt(3)
        iW1 = np.matrix(np.zeros((3, 1), dtype=complex))
        if self.C1W1['num'] is not None:
            iW1 += np.matrix([[self.analog_inputs[self.C1W1['num']].channels[self.C1W1['l1']].v_prim],
                              [self.analog_inputs[self.C1W1['num']].channels[self.C1W1['l2']].v_prim],
                              [self.analog_inputs[self.C1W1['num']].channels[self.C1W1['l3']].v_prim]])
        if self.C2W1['num'] is not None:
            iW1 += np.matrix([[self.analog_inputs[self.C2W1['num']].channels[self.C2W1['l1']].v_prim],
                              [self.analog_inputs[self.C2W1['num']].channels[self.C2W1['l2']].v_prim],
                              [self.analog_inputs[self.C2W1['num']].channels[self.C2W1['l3']].v_prim]])

        iW2 = np.matrix(np.zeros((3, 1), dtype=complex))
        if self.C1W2['num'] is not None:
            iW2 += np.matrix([[self.analog_inputs[self.C1W2['num']].channels[self.C1W2['l1']].v_prim],
                              [self.analog_inputs[self.C1W2['num']].channels[self.C1W2['l2']].v_prim],
                              [self.analog_inputs[self.C1W2['num']].channels[self.C1W2['l3']].v_prim]])
        if self.C2W2['num'] is not None:
            iW2 += np.matrix([[self.analog_inputs[self.C2W2['num']].channels[self.C2W2['l1']].v_prim],
                              [self.analog_inputs[self.C2W2['num']].channels[self.C2W2['l2']].v_prim],
                              [self.analog_inputs[self.C2W2['num']].channels[self.C2W2['l3']].v_prim]])

        iW3 = np.matrix(np.zeros((3, 1), dtype=complex))
        if self.C1W3['num'] is not None:
            iW3 += np.matrix([[self.analog_inputs[self.C1W3['num']].channels[self.C1W3['l1']].v_prim],
                              [self.analog_inputs[self.C1W3['num']].channels[self.C1W3['l2']].v_prim],
                              [self.analog_inputs[self.C1W3['num']].channels[self.C1W3['l3']].v_prim]])
        if self.C2W3['num'] is not None:
            iW3 += np.matrix([[self.analog_inputs[self.C2W3['num']].channels[self.C2W3['l1']].v_prim],
                              [self.analog_inputs[self.C2W3['num']].channels[self.C2W3['l2']].v_prim],
                              [self.analog_inputs[self.C2W3['num']].channels[self.C2W3['l3']].v_prim]])

        W2 = self.Global_base_values[self.GlobalBaseSelW2-1].UBase / self.Global_base_values[self.GlobalBaseSelW1-1].UBase * iW2
        W3 = self.Global_base_values[self.GlobalBaseSelW3-1].UBase / self.Global_base_values[self.GlobalBaseSelW1-1].UBase * iW3

        idiff_complex = (a * iW1 + b * W2 + b * W3) / self.Global_base_values[self.GlobalBaseSelW1-1].IBase
        idiff = abs(max(idiff_complex)[0, 0])
        itorm = abs(max((max(iW1), max(W2), max(W3)))[0,0]) / self.Global_base_values[self.GlobalBaseSelW1-1].IBase
        return idiff, itorm

    def __iter__(self):
        self.start_iter_torm = self.IdMin / 2 - self.step_iter
        self.count_iter_IdUnre = 5
        return self

    def __next__(self):
        self.start_iter_torm += self.step_iter
        diff = self.diff(self.start_iter_torm)
        if diff == self.IdUnre:
            self.count_iter_IdUnre -= 1
        if self.count_iter_IdUnre:
            return self.start_iter_torm, diff
        else:
            raise StopIteration

    def get_electric(self):
        self.te.h3('Проверка функции дифференциальной защиты T3WPDIF')
        if not self.tests.get('result_electric', False):
            print(f'Для функции {self.INSTNAME} отсутствуют данные тестов. Данные сгенерированы ')
            self.tests.update({'torm_haract': []})
            for cs in ('ВЭ-110 - В10-ЭК1', 'СВ-110 - В10-ЭК2'):
                self.tests['torm_haract'].append({'mode': cs})
                self.tests['torm_haract'][-1].update({'haract': []})
                for torm, diff in self:
                    self.set_diff_torm(diff, torm)
                    k = uniform(0.99, 1.01)
                    self.analog_inputs[self.C1W2["num"]].channels[self.C1W2["l1"]].v_sec *= k
                    self.analog_inputs[self.C1W2["num"]].channels[self.C1W2["l2"]].v_sec *= k
                    self.analog_inputs[self.C1W2["num"]].channels[self.C1W2["l3"]].v_sec *= k
                    self.tests['torm_haract'][-1]['haract'].append([abs(self.analog_inputs[self.C1W1["num"]].channels[self.C1W1["l1"]].v_sec),
                                                          np.degrees(phase(self.analog_inputs[self.C1W1["num"]].channels[self.C1W1["l1"]].v_sec)),
                                                          abs(self.analog_inputs[self.C1W1["num"]].channels[self.C1W1["l2"]].v_sec),
                                                          np.degrees(phase(self.analog_inputs[self.C1W1["num"]].channels[self.C1W1["l2"]].v_sec)),
                                                          abs(self.analog_inputs[self.C1W1["num"]].channels[self.C1W1["l3"]].v_sec),
                                                          np.degrees(phase(self.analog_inputs[self.C1W1["num"]].channels[self.C1W1["l3"]].v_sec)),
                                                          abs(self.analog_inputs[self.C1W2["num"]].channels[
                                                                    self.C1W2["l1"]].v_sec),
                                                          np.degrees(phase(
                                                                self.analog_inputs[self.C1W2["num"]].channels[
                                                                    self.C1W2["l1"]].v_sec)),
                                                          abs(self.analog_inputs[self.C1W2["num"]].channels[
                                                                    self.C1W2["l2"]].v_sec),
                                                          np.degrees(phase(
                                                                self.analog_inputs[self.C1W2["num"]].channels[
                                                                    self.C1W2["l2"]].v_sec)),
                                                          abs(self.analog_inputs[self.C1W2["num"]].channels[
                                                                    self.C1W2["l3"]].v_sec),
                                                          np.degrees(phase(
                                                                self.analog_inputs[self.C1W2["num"]].channels[
                                                                    self.C1W2["l3"]].v_sec))
                                                                    ])
            d = self.IdMin * 3
            self.set_diff_torm(d, d)
            d2 = abs(self.analog_inputs[self.C1W1["num"]].channels[self.C1W1["l1"]].v_sec)
            i2 = self.I2_I1Ratio / 100 * d2 * uniform(0.99, 1.01)
            i5 = self.I5_I1Ratio / 100 * d2 * uniform(0.99, 1.01)
            self.tests.update({'result_i2': [d2, i2, i2 * 0.96]})
            self.tests.update({'result_i5': [d2, i5, i5 * 0.96]})
        for cs in self.tests['torm_haract']:
            self.te.h3(f'Снятие тормозной характеристики {cs["mode"]}')
            self.te.table_head('Ток I1A, A', 'Ток I1B, A', 'Ток I1C, A', 'Ток I2A, A', 'Ток I2B, A', 'Ток I2C, A',
                    'Ток торможения, о.е.', 'Дифференциальный ток фактический, о.е.',
                    'Дифференциальный ток уставки, о.е.', 'Отклонение, %')
            torm_list = []
            diff_list = []
            for data in cs['haract']:
                self.analog_inputs[self.C1W1['num']].channels[self.C1W1['l1']].v_sec = rect(data[0], radians(data[1]))
                self.analog_inputs[self.C1W1['num']].channels[self.C1W1['l2']].v_sec = rect(data[2], radians(data[3]))
                self.analog_inputs[self.C1W1['num']].channels[self.C1W1['l3']].v_sec = rect(data[4], radians(data[5]))
                self.analog_inputs[self.C1W2['num']].channels[self.C1W2['l1']].v_sec = rect(data[6], radians(data[7]))
                self.analog_inputs[self.C1W2['num']].channels[self.C1W2['l2']].v_sec = rect(data[8], radians(data[9]))
                self.analog_inputs[self.C1W2['num']].channels[self.C1W2['l3']].v_sec = rect(data[10], radians(data[11]))
                idiff, itorm = self.get_diff_torm()
                torm_list.append(itorm)
                diff_list.append(idiff)
                idiff_ust = self.diff(itorm)
                self.te.table_row(f'{data[0]:.3f}A {data[1]:.1f}°',
                        f'{data[2]:.3f}A {data[3]:.1f}°',
                        f'{data[4]:.3f}A {data[5]:.1f}°',
                        f'{data[6]:.3f}A {data[7]:.1f}°',
                        f'{data[8]:.3f}A {data[9]:.1f}°',
                        f'{data[10]:.3f}A {data[11]:.1f}°',
                        f'{itorm:.2f}', f'{idiff:.3f}', f'{idiff_ust:.2f}',
                        f'{(idiff_ust-idiff)*100/idiff:.2f}')
            fig, ax = plt.subplots()
            fig.set_figheight(7)
            fig.set_figwidth(8)
            ax.plot(torm_list, diff_list, color='C1')
            ax.set_xlabel("Iторм,A", fontsize=13)
            ax.set_ylabel("Iдиф,А", fontsize=13)
            ax.minorticks_on()
            ax.grid(which='major', lw=1)
            ax.grid(which='minor', lw=0.5)
            plt.savefig(f'source/_static/{self.name_terminal}_{cs["mode"]}_diff_real.png', format="png", dpi=1000)
        self.te.h3('Проверка блокировки дифференциальной защиты по второй гармонике')
        self.te.table_head('I1,A 50Гц', 'I2,A 100Гц', 'I2в,A 100Гц', 'Кв', 'I2/I1,%', 'I2/I1изм,%')
        self.te.table_row(f'{self.tests["result_i2"][0]:.3f}', f'{self.tests["result_i2"][1]:.3f}',
                f'{self.tests["result_i2"][2]:.3f}', f'{self.tests["result_i2"][2] / self.tests["result_i2"][1]:.3f}',
                f'{self.I2_I1Ratio}', f'{self.tests["result_i2"][1] / self.tests["result_i2"][0] * 100:.2f}')
        self.te.h3('Проверка блокировки дифференциальной защиты по пятой гармонике')
        self.te.table_head('I1,A 50Гц', 'I5,A 100Гц', 'I5в,A 100Гц', 'Кв', 'I5/I1,%', 'I5/I1изм,%')
        self.te.table_row(f'{self.tests["result_i5"][0]:.3f}', f'{self.tests["result_i5"][1]:.3f}',
                f'{self.tests["result_i5"][2]:.3f}', f'{self.tests["result_i5"][2] / self.tests["result_i5"][1]:.3f}',
                f'{self.I5_I1Ratio}', f'{self.tests["result_i5"][1] / self.tests["result_i5"][0] * 100:.2f}')

    def get_complex(self):
        d = self.IdMin * 1.1
        self.set_diff_torm(d, d)
        d2 = abs(self.analog_inputs[self.C1W1["num"]].channels[self.C1W1["l1"]].v_sec)
        self.te.h3(f'Комплексная проверка функции дифференциальной защиты T3WPDIF при токе {d2:.3f} A')
        self.te.table_head('Время, сек', 'Сработавший контакт')
        for num, t_contact in enumerate(self.tests['result_complex']):
            t = f'{t_contact:.3f}' if t_contact else 'Не сработал'
            self.te.table_row(f'{t}', f'{self.contacts[num]}')
        self.te.p(f'При токе {d2 / 1.21:.2f} A не срабатывает.')



    def get_charact_diff(self):

        fig, ax = plt.subplots()
        fig.set_figheight(7)
        fig.set_figwidth(8)
        torm_list = []
        dif_list = []
        for torm, diff in self:
            torm_list.append(torm)
            dif_list.append(diff)
        ax.plot(torm_list, dif_list, color='C1')
        ax.set_xlabel("Iторм,A", fontsize=13)
        ax.set_ylabel("Iдиф,А", fontsize=13)
        ax.minorticks_on()
        ax.grid(which='major', lw=1)
        ax.grid(which='minor', lw=0.5)
        plt.savefig('diff.png', format="png", dpi=1000)