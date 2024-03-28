.. image:: https://img.shields.io/badge/License-WTFPL-brightgreen.svg
   :target: http://www.wtfpl.net/about/
   :alt: License: WTFPL
.. image:: https://readthedocs.org/projects/glxviewer/badge/?version=latest
   :target: https://glxviewer.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

==============================
Galaxie Viewer's documentation
==============================
.. figure::  https://glxviewer.readthedocs.io/en/latest/_images/logo_galaxie.png
   :align:   center

Description
-----------
Provide a Text Based line viewer, it use a template. It existe many template for high level language, but nothing for text one.

Our mission is to provide useful display template for terminal. Actually every Galaxie tool use it; where print() is not use any more...

Links
-----
  * CodeBerg: https://codeberg.org/Tuuux/galaxie-viewer/
  * Issue: https://codeberg.org/Tuuux/galaxie-viewer/issues
  * Read the Doc: https://glxviewer.readthedocs.io/
  * PyPI: https://pypi.org/project/galaxie-viewer/
  * PyPI Test: https://test.pypi.org/project/galaxie-viewer/


Screenshots
-----------
v 0.5

.. figure::  https://glxviewer.readthedocs.io/en/latest/_images/screen_01.png
   :align:   center

Installation via pip
--------------------
Pypi

.. code:: bash

  pip install galaxie-viewer

Pypi Test

.. code:: bash

  pip install -i https://test.pypi.org/simple/ galaxie-viewer

Code Example
------------

.. code:: python

    import sys
    import os
    import time

    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(current_dir))

    from glxviewer import viewer


    def main():
        start_time = time.time()
        viewer.write(
            column_1=__file__,
            column_2='Yes that is possible',
            status_text_color='MAGENTA',
        )
        viewer.write(
            column_1=__file__,
            column_2='it have no difficulty to make it',
            column_3='what ?'
        )
        viewer.write(
            column_1='Use you keyboard with Ctrl + c for stop the demo',
            status_text='INFO',
            status_text_color='GREEN',
            status_symbol='!',
        )
        while True:

            viewer.write(
                column_1=__file__,
                column_2=str(time.time() - start_time),
                status_text='REC',
                status_text_color='RED',
                status_symbol='<',
                prompt=-1
            )


    if __name__ == '__main__':
        try:
            main()
        except KeyboardInterrupt:
            viewer.flush_a_new_line()
            sys.exit()


CLI Example
-----------

.. code:: bash

     glx-viewer --with-no-date --column-1 "PIP INSTALL GLXVIEWER" --status-text-color GREEN --status-text "OK" --status-symbol ''

