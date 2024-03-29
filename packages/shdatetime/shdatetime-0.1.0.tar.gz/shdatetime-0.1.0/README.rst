shdatetime
==========

``shdatetime`` `Solar Hijri`_ implementation of Python's `datetime`_ module.

Installation
------------
``pip install shdatetime``

Usage
-----
This module exactly follows Python Standard datetime module's methods https://docs.python.org/3/library/datetime.html

Also these methods are added to ``shdatetime.date`` and ``shdatetime.datetime`` :


.. code-block:: python

    fromgregorian(**kw)
        Convert gregorian to jalali and return shdatetime.date
        jdatetime.date.fromgregorian(day=X,month=X,year=X)
        jdatetime.date.fromgregorian(date=datetime.date)
        jdatetime.datetime.fromgregorian(datetime=datetime.datetime)
    togregorian(self)
        Convert current jalali date to gregorian and return datetime.date
    isleap(self)
        check if year is leap year
        algortim is based on http://en.wikipedia.org/wiki/Leap_year


Example
-------

.. code-block:: shell

    >>> import shdatetime
    >>> shdatetime.datetime.now()
    shdatetime.datetime(1394, 12, 4, 8, 37, 31, 855729)
    >>> shdatetime.date.today()
    shdatetime.date(1394, 12, 4)


Locale
------
In order to get the date string in farsi you need to set the locale to `shdatetime.FA_LOCALE`. The locale
could be specified explicitly upon instantiation of `date`/`datetime` instances, or by
setting a default locale.

Instance locales is *named argument only*:

.. code-block:: python

    import shdatetime
    fa_date = shdatetime.date(1397, 4, 23, locale=shdatetime.FA_LOCALE)
    fa_datetime = shdatetime.datetime(1397, 4, 23, 11, 40, 30, locale=shdatetime.FA_LOCALE)


`date` and `datetime` instances provide the method `aslocale()` to return a clone of the instance
with the same timestamp, in a different locale.


Default Locale
~~~~~~~~~~~~~~
It's possible to set the default locale, so all new instances created afterwards would use
the desired locale, unless explicitly specified otherwise.

.. code-block:: shell

    >>> import locale
    >>> import shdatetime
    >> shdatetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
    u'Wed, 08 Ord 1395 20:47:32'
    >>> locale.setlocale(locale.LC_ALL, shdatetime.FA_LOCALE)
    'fa_IR'
    >>> shdatetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
    u'\u0686\u0647\u0627\u0631\u0634\u0646\u0628\u0647, 08 \u0627\u0631\u062f\u06cc\u0628\u0647\u0634\u062a 1395 20:47:56'


If your requirements demand to support different locales withing the same process,
you could set the default locale per thread. New `date` and `datetime` instances
created in each thread, will use the specified locale by default.
This supports both Python threads, and greenlets.


.. code-block:: python

    import shdatetime
    shdatetime.set_locale(shdatetime.FA_LOCALE)
    shdatetime.datetime.now().strftime('%A %B')
    # u'\u062f\u0648\u0634\u0646\u0628\u0647 \u062e\u0631\u062f\u0627\u062f'

Fork of jdatetime
-----------------
``shdatetime`` is a fork of `jdatetime`_.

Main differences:

- ``shdatetime`` is released under the terms of GPL-v3 license.
- Instead of relying on `jalali-core`_, ``shdatetime`` uses `gshconveter`_ which is fully compatible with ``jalali-core`` and is thoroughly tested. It's also faster!
- ``shdatetime`` requires Python 3.12+.


.. _Solar Hijri: https://en.wikipedia.org/wiki/Solar_Hijri_calendar
.. _datetime: https://docs.python.org/3/library/datetime.html
.. _jdatetime: https://github.com/slashmili/python-jalali
.. _jalali-core: https://github.com/slashmili/jalali-core
.. _PSFL: https://en.wikipedia.org/wiki/Python_Software_Foundation_License
.. _fork: https://help.github.com/en/articles/fork-a-repo
.. _repository: https://github.com/slashmili/python-jalali
.. _gshconveter: https://github.com/5j9/gshconverter
