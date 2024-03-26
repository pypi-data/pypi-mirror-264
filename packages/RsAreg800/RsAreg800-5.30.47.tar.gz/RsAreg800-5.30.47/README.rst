==================================
 RsAreg800
==================================

.. image:: https://img.shields.io/pypi/v/RsAreg800.svg
   :target: https://pypi.org/project/ RsAreg800/

.. image:: https://readthedocs.org/projects/sphinx/badge/?version=master
   :target: https://RsAreg800.readthedocs.io/

.. image:: https://img.shields.io/pypi/l/RsAreg800.svg
   :target: https://pypi.python.org/pypi/RsAreg800/

.. image:: https://img.shields.io/pypi/pyversions/pybadges.svg
   :target: https://img.shields.io/pypi/pyversions/pybadges.svg

.. image:: https://img.shields.io/pypi/dm/RsAreg800.svg
   :target: https://pypi.python.org/pypi/RsAreg800/

Rohde & Schwarz AREG800A automotive radar echo generator RsAreg800 instrument driver.

Basic Hello-World code:

.. code-block:: python

    from RsAreg800 import *

    instr = RsAreg800('TCPIP::192.168.2.101::hislip0')
    idn = instr.query('*IDN?')
    print('Hello, I am: ' + idn)

Supported instruments: AREG

The package is hosted here: https://pypi.org/project/RsAreg800/

Documentation: https://RsAreg800.readthedocs.io/

Examples: https://github.com/Rohde-Schwarz/Examples/


Version history
----------------

	Latest release notes summary: Update for FW 5.30.047

	Version 5.30.47
		- Update for FW 5.30.047

	Version 5.0.57
		- First release for FW 5.00.057

