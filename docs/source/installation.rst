Installation
============

OneModel can be installed from the Python Package Index (PyPI) repository as a package for ``python3.8``.

For the impatients:

.. code-block:: bash

  $ pip install onemodel      # install OneModel
  $ pip install onemodel -u   # update to the newest version
  $ onemodel-gui              # open the graphical user interface
  $ onemodel-cli              # access the command-line interface
  $ onemodel-cli --help       # show help message

OneModel can be installed in Windows, Mac, or Linux; the only requirement is to have installed ``python 3.8``.

Therefore, the first step is to install ``python3.8`` in your system.
The installation process of Python varies depending on the operating system you are using: there are great tutorials regarding each operating system on the internet.

Once you have installed Python, you have to verify that the correct version of ``python`` and ``pip`` are installed. For this, write in the command prompt of your system: ``python --version`` and ``pip --version`` the output of these two commands should indicate that the version of Python is 3.8 in both cases.
If another version of Python appears, it means that you have multiple versions of Python installed in your system, then you should use ``pip3.8`` instead of ``pip`` for installing OneModel.

Now you can install OneModel by writing ``pip install onemodel`` in the command prompt (or ``pip3.8 install onemodel``). This command will install OneModel and all its dependencies in your system.
The examples of this Thesis were done for OneModel v0.0.10, they should still work in future versions, but we recommend using this specific version to follow the examples (you can install this version with ``pip install onemodel==0.0.10``), and to check the Thesis GitHub repository for more information.

The graphical user interface is opened by writing ``onemodel-gui`` in the command prompt and the command-line interface is accessed with ``onemodel-cli``.

Lastly, if you want to update OneModel to the newest version, you can use the following command: ``pip install onemodel -u``.


