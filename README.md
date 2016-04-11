EZVD
==========

![EZVD Screencast](https://raw.githubusercontent.com/apollo-ng/ezvd/master/screencast.gif)




## Installation

### Dependencies

  * Python 3.x
    * with UTF support
    * with ncurses support

Every reasonably recent GNU system should have this available.

### Clone repo

    $ git clone https://github.com/apollo-ng/ezvd.git
    $ cd ezvd

## Usage

### Run

    $ ./ezvd.py

### Interaction

#### Basic Parameters

| Key | Function                                 |
|:---:|:----------------------------------------:|
|  1  | Enter value of R1 in Ohms                |
|  2  | Enter value of R2 in Ohms                |
|  M  | Enter maximum input Voltage (Full-Scale) |
|  R  | Enter ADC Reference Voltage              |

#### Simulation Control

| Key | Function                                     |
|:---:|:--------------------------------------------:|
| Tab | Cycle between simulation targets (VIN/R1/R2) |
|  +  | Increase simulation step size                |
|  -  | Decrease simulation step size                |
|  ▲  | Change simulation direction (Up)             |
|  ▼  | Change simulation direction (Down)           |
| P/Space | Pause/Resume simulation                  |

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Support & Contact

Please use the issue tracker for ezvd related issues.

More info: https://apollo.open-resource.org/mission:resources:ezvd


