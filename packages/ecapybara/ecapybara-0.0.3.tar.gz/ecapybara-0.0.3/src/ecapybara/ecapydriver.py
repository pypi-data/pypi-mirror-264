"""
Simple application that drives ecapybara in the console.
"""

import logging
import shutil
from .ecapyworld import Ecapyworld

def main():
    """
    driver for console app.
    """
    logging.basicConfig(level=logging.INFO)
    term_size = shutil.get_terminal_size()
    term_col = term_size.columns
    logging.info("Terminal width (columns): {%s}", term_col)
    width = term_col - 10
    if width % 2 == 0:
        width += 1
        logging.info("Added 1 to width to ensure seed is centered.")
    else:
        logging.info("Width is odd number of columns, not changing.")
    logging.info("Setting universe width to %s", width)
    ecapy = Ecapyworld(width)
    rule_num = -1
    while rule_num == -1:
        rule_num = input("Select a rule (0-255): ")
        rule_num = int(rule_num)
        logging.info("Entered: {%s}", rule_num)
        if rule_num < 0 or rule_num > 255:
            print("Error: you must enter an integer between 0 and 255.")
            rule_num = -1
    #trule = rules[rule_num]
    # TODO: larger step numbers do not generate reliable output, fix
    steps = 100
    get_steps = 0
    get_steps = steps = input(
        "Enter the number of steps you would like to iterate (default: 100): "
    )
    if not get_steps:
        print(f"Invalid number of steps entered, using default {str(steps)}")
    else:
        steps = int(get_steps)
        print(f"Entered {get_steps}, using value {steps}")
    print(f"Starting iteration ({steps} steps)\n")
    trule = ecapy.ruleset[rule_num]
    for _ in range(steps - 1):
        ecapy.iterate_state(trule)
    print(ecapy.textmode())
    print("End")


if __name__ == "__main__":
    main()
