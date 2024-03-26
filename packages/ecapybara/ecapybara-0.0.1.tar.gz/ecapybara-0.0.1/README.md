# ecapybara
ecapybara, Elementary Cellular Automata for PYthon + BARA

<a href="https://github.com/nrejack/ecapybara/actions/workflows/pylint.yml">
  <img  alt="GitHubs Actions build status (Pylint)" 
        src="https://github.com/python-pillow/Pillow/workflows/Lint/badge.svg"></a>
                
Iterate the 256 [elementary cellular automata](https://en.wikipedia.org/wiki/Elementary_cellular_automaton)
starting from a fixed inital state (center cell 'live', all others 'dead').

## Usage

### Installed package
pip install ecapybara
python3 -m ecapybara.ecapydriver

### Console mode
`python3 src/ecapybara/ecapydriver.py`

You will be prompted to select one of the rules from 0-255, and the number of steps you would like to iterate. Output will be scaled to fit the number of columns in your terminal window with some padding.


## Sample output
![rule 22, 50 steps](img/sample_output.png)

## TODO
- Larger number of steps doesn't generate expected output.
- Needs to be modularized.
- Needs unit tests.
- Needs click interface for CLI.
- Needs to write images using PILlow.
- Logging needs work.
- Streaming from API not working
- Needs some JS or other trickery to get browser window width
- Add ability to scale fundamental elements
- Add ability to 'page' back and forth between different rules in browser view
- Programmatically generate visual representation of rules
- Needs ability to start from randomized seed
- COLORS !!!
- Animation modes (fades, slow transitions)

## Mascot
The official mascot of ecapybara is the e-capybara.

![e-capybara, our mascot](img/capy.jpg)
