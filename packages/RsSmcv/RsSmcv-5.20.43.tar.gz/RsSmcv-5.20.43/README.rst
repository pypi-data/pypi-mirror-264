==================================
 RsSmcv
==================================

.. image:: https://img.shields.io/pypi/v/RsSmcv.svg
   :target: https://pypi.org/project/ RsSmcv/

.. image:: https://readthedocs.org/projects/sphinx/badge/?version=master
   :target: https://RsSmcv.readthedocs.io/

.. image:: https://img.shields.io/pypi/l/RsSmcv.svg
   :target: https://pypi.python.org/pypi/RsSmcv/

.. image:: https://img.shields.io/pypi/pyversions/pybadges.svg
   :target: https://img.shields.io/pypi/pyversions/pybadges.svg

.. image:: https://img.shields.io/pypi/dm/RsSmcv.svg
   :target: https://pypi.python.org/pypi/RsSmcv/

Rohde & Schwarz SMCV100B Vector Signal Generator RsSmcv instrument driver.

Basic Hello-World code:

.. code-block:: python

    from RsSmcv import *

    instr = RsSmcv('TCPIP::192.168.56.101::hislip0', reset=True)
    idn = instr.query_str('*IDN?')
    print('Hello, I am: ' + idn)

Supported instruments: SMCV100B

The package is hosted here: https://pypi.org/project/RsSmcv/

Documentation: https://RsSmcv.readthedocs.io/

Examples: https://github.com/Rohde-Schwarz/Examples/tree/main/SignalGenerators/Python/RsSmcv_ScpiPackage


Version history
----------------

	Latest release notes summary: Update for FW 5.20.043

	Version 5.20.43
		- Update for FW 5.20.043

	Version 5.0.124.16
		- Updated core to the newest template.
		- Added DigitalModulation Interface.

	Version 5.0.122.13
		- Update for FW 5.00.122

	Version 4.80.2.11
		- Fixed bug in interfaces with the name 'base', new docu format

	Version 4.80.2.6
		- First released version
