"""Bill multiple households using fictional progressive rates for practice."""

FIRST_SLAB_LIMIT = 100
SECOND_SLAB_LIMIT = 200
FIRST_RATE = 10
SECOND_RATE = 15
THIRD_RATE = 20
MAX_INTEGER_DIGITS = 18


def get_valid_integer(prompt, minimum=0):
    """Read a bounded whole number; invalid values retry the same prompt."""
    while True:
        text = input(prompt).strip()
        if text.isdecimal():
            normalized = text.lstrip("0") or "0"
            if len(normalized) <= MAX_INTEGER_DIGITS:
                number = int(normalized)
                if number >= minimum:
                    return number
        print(
            f"Invalid input! Enter a whole number of {minimum} or more "
            f"with at most {MAX_INTEGER_DIGITS} significant digits."
        )


def main():
    """Use a for loop, range, slab conditions and revenue/count accumulators."""
    print("===== ELECTRICITY BILL SYSTEM =====")
    print("Practice rates only: these are not actual electricity tariffs.")
    households = get_valid_integer("Enter the number of households: ", minimum=1)
    total_revenue = 0
    processed_households = 0

    for household in range(1, households + 1):
        print(f"\n--- Household {household} ---")
        units = get_valid_integer("Enter electricity units consumed: ")

        # Charge each slab separately, rather than one rate on every unit.
        if units <= FIRST_SLAB_LIMIT:
            bill = units * FIRST_RATE
        elif units <= SECOND_SLAB_LIMIT:
            bill = (
                FIRST_SLAB_LIMIT * FIRST_RATE
                + (units - FIRST_SLAB_LIMIT) * SECOND_RATE
            )
        else:
            bill = (
                FIRST_SLAB_LIMIT * FIRST_RATE
                + (SECOND_SLAB_LIMIT - FIRST_SLAB_LIMIT) * SECOND_RATE
                + (units - SECOND_SLAB_LIMIT) * THIRD_RATE
            )

        print(f"Units Consumed: {units}")
        print(f"Electricity Bill: Rs. {bill}")
        total_revenue += bill
        processed_households += 1

    print("\n===== MONTHLY REVENUE REPORT =====")
    print(f"Households Processed: {processed_households}")
    print(f"Total Revenue: Rs. {total_revenue}")


if __name__ == "__main__":
    main()
