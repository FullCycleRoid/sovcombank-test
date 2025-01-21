from dataclasses import dataclass
from typing import List
from decimal import Decimal, ROUND_HALF_UP
from abc import ABC, abstractmethod
import time
import random


class NegativeProportionError(ValueError):
    """Исключение для долей с отрицательным значением"""
    pass


@dataclass
class Proportion:
    value: Decimal

    def __post_init__(self):
        self.value = Decimal(str(self.value))


@dataclass
class Percentage:
    value: Decimal

    def __str__(self):
        return f"{self.value:.3f}"


class IProportionCalculatorService(ABC):
    @abstractmethod
    def calculate_percentages(self, proportions: List[Proportion]) -> List[Percentage]:
        pass


class DecimalProportionCalculator(IProportionCalculatorService):
    def calculate_percentages(self, proportions: List[Proportion]) -> List[Percentage]:
        if not proportions:
            return []

        total = sum(proportion.value for proportion in proportions)

        if total == 0:
            raise ValueError("Сумма долей должна быть больше нуля")

        percentages = []
        for proportion in proportions:
            if int(proportion.value) <= 0:
                raise NegativeProportionError('Значение доли должно быть больше 0')

            percentage = (proportion.value / total)
            formatted_percentage = Decimal(str(percentage)).quantize(
                Decimal('0.001'),
                rounding=ROUND_HALF_UP
            )
            percentages.append(Percentage(formatted_percentage))

        return percentages


class proportionCalculatorApplication:
    def __init__(self, calculator: IProportionCalculatorService):
        self.calculator = calculator

    def process_proportions(self, raw_proportions: List[float]) -> List[str]:
        try:
            proportions = [Proportion(value) for value in raw_proportions]
            percentages = self.calculator.calculate_percentages(proportions)
            return [str(percentage) for percentage in percentages]
        except NegativeProportionError as err:
            print(f"Ошибка: {err}")
            return []


def test_performance(n: int, max_value: int) -> float:
    proportions = [random.uniform(1, max_value) for _ in range(n)]
    start_time = time.time()

    total = sum(proportions)
    _ = [(proportion / total) for proportion in proportions]

    elapsed = time.time() - start_time
    return elapsed


def performance_analysis():
    test_sizes = [
        1000,
        10000,
        100000,
        1000000,
        10000000,
        100000000
    ]

    print('=========== Оценка времени выполнения =============')
    for size in test_sizes:
        time_spend = test_performance(size, 1000000000)  # 1000000000 -> 10^9
        print(f"N = {size:,}, Время: {time_spend:.3f} сек.")


def run_task():
    raw_proportions1 = [1.5, 3, 6, 1.5]
    raw_proportions2 = [1.5, 3, 6, 1.5, 7, 12, 132.7]
    negative_test = [1.5, 3, 6, 1.5, 7, 12, 132.7, -11]

    calculator = DecimalProportionCalculator()
    app = proportionCalculatorApplication(calculator)

    for payload in [raw_proportions1, raw_proportions2, negative_test]:
        print('========== Start calculation =========')
        results = app.process_proportions(payload)
        for percentage in results:
            print(percentage)
        print('========== End calculation =========')


if __name__ == "__main__":
    run_task()
    performance_analysis()
