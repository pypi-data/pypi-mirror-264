# get_cemeb_cal – Get calendar from CeMEB
[![PyPI Version](https://img.shields.io/pypi/v/get_cemeb_cal?color=00aa00)](https://pypi.org/project/get_cemeb_cal)
[![PyPI License](https://img.shields.io/pypi/l/get_cemeb_cal)](COPYING)

## Installation from PyPI
```sh
pip install get_cemeb_cal
```

## Installation from source code
```sh
pip install .
```

## Usage as standalone program
```sh
get_cemeb_cal -h
```

## Automated local calendar update
Given a local calendar file obtained by e.g.,
```sh
get_cemeb_cal -o ~/.cemeb.ics -f 01/01/2024
```
a possible cron job can be added using `crontab -e` with
```crontab
# M  H  d  m    W  /path/command
  0  8  *  *  1-5  python -m get_cemeb_cal -i ~/.cemeb.ics -o ~/.cemeb.ics
```
which will update the calendar every week day at 8 o’clock.

## Usage as python module
Currently not implemented

## Copyright
Copyright 2024 Robert Wolff <mahlzahn@posteo.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
