"""
ECAPYbara is an implementation of Elementary Cellular Automata for PYthon.
Ecapybara is the classname.
"""

class Ecapyworld:
    """
    Foundation class for an instance that is used to generate and iterate cellular automata.
    """

    def __init__(self, width):
        self.ruleset = self.generate_rules()
        self.set_initial_state(width)
        print(f"Initialized ecapy object with width {width}")

    def generate_rules(self):
        """
        generate a dictionary of dictionaries indexed by Wolfram code
        within each code, 8 possibilities (base 10) for transformation
        based on group of 3 blocks.
        """
        rules = {}
        for i in range(256):
            mapping = {}
            num = str(bin(i))[2:].rjust(8, "0")
            for j in range(8):
                mapping[j] = num[7 - j]
            rules[i] = mapping
        return rules


    def set_initial_state(self, width):
        """
        return a block with only middle block in 1 state
        """
        side_size = width // 2
        print(f"Side size set to: {side_size}")
        initial_state = "0" * side_size + "1" + "0" * side_size
        print(f"Initial state width: {str(len(initial_state))}")
        self.state = [initial_state]

    def get_current_state(self):
        """
        Get only the most current state from our state object.
        """
        return self.state[len(self.state) -1]

    def get_full_state(self):
        """
        Get the entire historical state.
        """
        return self.state

    def iterate_state(self, rule):
        """
        apply current rule to current state and return new state
        """
        curr = self.get_current_state()
        new_state = ""
        width = len(curr)
        new_state += curr[0]
        for i in range(0, width - 2):
            three_cells = "0b" + curr[i:i + 3]
            value = int(three_cells, 2)
            new_state += rule[value]
        new_state += curr[width - 1]
        self.state.append(new_state)


    def textmode(self):
        """
        format a 'binary string' into textmode for printing
        return current state
        """
        output = ''
        for s in self.state:
            s = s.replace("1", "█")
            s = s.replace("0", " ")
            s += '\n'
            output += s
        return output


    # def webtextmode(self, binary_string, color_a, color_b):
    #     """
    #     format a 'binary string' into a web-printable text representation
    #     TODO: improve this by coalescing large runs of same color
    #     TODO: use blocks or something else
    #     """
    #     color_a_txt = f"<span style='color:{color_a}'>█</span>"
    #     color_b_txt = f"<span style='color:{color_b}'>█</span>"
    #     binary_string = binary_string.replace("1", color_a_txt)
    #     binary_string = binary_string.replace("0", color_b_txt)
    #     return binary_string + "<br />"
