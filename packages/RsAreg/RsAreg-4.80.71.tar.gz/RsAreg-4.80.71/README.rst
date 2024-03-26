==================================
 RsAreg
==================================

.. image:: https://img.shields.io/pypi/v/RsAreg.svg
   :target: https://pypi.org/project/ RsAreg/

.. image:: https://readthedocs.org/projects/sphinx/badge/?version=master
   :target: https://RsAreg.readthedocs.io/

.. image:: https://img.shields.io/pypi/l/RsAreg.svg
   :target: https://pypi.python.org/pypi/RsAreg/

.. image:: https://img.shields.io/pypi/pyversions/pybadges.svg
   :target: https://img.shields.io/pypi/pyversions/pybadges.svg

.. image:: https://img.shields.io/pypi/dm/RsAreg.svg
   :target: https://pypi.python.org/pypi/RsAreg/

Rohde & Schwarz AREG100A automotive radar echo generator RsAreg instrument driver.

Basic Hello-World code:

.. code-block:: python

    from RsAreg import *

    instr = RsAreg('TCPIP::192.168.2.101::hislip0')
    idn = instr.query('*IDN?')
    print('Hello, I am: ' + idn)

Supported instruments: AREG

The package is hosted here: https://pypi.org/project/RsAreg/

Documentation: https://RsAreg.readthedocs.io/

Examples: https://github.com/Rohde-Schwarz/Examples/


Version history
----------------

	Latest release notes summary: Documentation Fixes

	Version 4.80.71
		- Documentation Fixes

	Version 4.80.70
		- First release for FW 4.80.070
