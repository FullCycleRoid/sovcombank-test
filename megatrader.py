from dataclasses import dataclass
from typing import List, Tuple, Optional
from collections import defaultdict
from io import StringIO
import sys


@dataclass
class Bond:
    day: int
    name: str
    price: float
    quantity: int

    def lot_cost(self) -> float:
        return (self.price / 100) * 1000 * self.quantity

    def lot_income(self, days_till_maturity: int) -> float:
        coupon_income = days_till_maturity * self.quantity
        nominal_income = 1000 * self.quantity
        return coupon_income + nominal_income - self.lot_cost()


def find_optimal_trades_dp(N: int, S: float, bonds: List[Bond]) -> Tuple[float, List[Bond]]:
    bonds_by_day = defaultdict(list)
    for bond in bonds:
        bonds_by_day[bond.day].append(bond)

    dp = {0: {S: (0, [])}}

    for day in range(1, N + 1):
        dp[day] = {}
        current_bonds = bonds_by_day[day]

        for prev_budget, (prev_income, prev_bonds) in dp[day - 1].items():
            dp[day][prev_budget] = (prev_income, prev_bonds[:])

            for bond in current_bonds:
                if bond.lot_cost() <= prev_budget:
                    new_budget = prev_budget - bond.lot_cost()
                    days_till_maturity = N + 30 - day
                    new_income = prev_income + bond.lot_income(days_till_maturity)

                    if new_budget not in dp[day] or dp[day][new_budget][0] < new_income:
                        print(dp[day][new_budget], 'dp[day][new_budget]')
                        dp[day][new_budget] = (new_income, prev_bonds + [bond])

    max_income = 0
    best_result = None

    for budget, result in dp[N].items():
        if result[0] > max_income:
            max_income = result[0]
            best_result = result

    return best_result


def parse_input() -> Tuple[int, int, float, List[Bond]]:
    N, M, S = map(float, input().split())
    N, M = int(N), int(M)
    bonds = []

    while True:
        line = input().strip()
        if not line:
            break

        day, name, price, quantity = line.split()
        bonds.append(Bond(
            day=int(day),
            name=name,
            price=float(price),
            quantity=int(quantity)
        ))

    return N, M, S, bonds


def format_output(result: Tuple[float, List[Bond]]) -> None:
    total_income, selected_bonds = result
    print(f"{int(total_income)}")

    for bond in sorted(selected_bonds, key=lambda x: (x.day, x.name)):
        print(f"{bond.day} {bond.name} {bond.price} {bond.quantity}")
    print()


if __name__ == "__main__":
    # Тестовые наборы данных
    test_cases = [
        """2 2 8000
        1 alfa-05 100.2 2
        2 alfa-05 101.5 5
        2 gazprom-07 100.0 2
        """,

        """4 3 15000
        1 bond-a 98.5 3
        1 bond-b 99.0 2
        2 bond-c 97.5 4
        2 bond-d 98.8 2
        3 bond-e 99.5 3
        4 bond-a 97.0 5
        """,
        # ограниченный бюджет
        """3 2 5000
        1 short-a 99.0 2
        1 long-b 98.5 3
        2 mid-c 97.5 2
        3 short-d 98.0 1
        """
    ]

    for test_case in test_cases:
        print("Тестовый пример:")
        print(test_case)

        sys.stdin = StringIO(test_case)

        N, M, S, bonds = parse_input()

        result = find_optimal_trades_dp(N, S, bonds)

        print("Результат:")
        format_output(result)
        print("-" * 50)
