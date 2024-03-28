.. highlight:: shell

============
Installation
============


Stable release
--------------

To install Boosting CV-LLM sentiment, run this command in your terminal:

.. code-block:: console

    $ pip install boosting_cv_llm_sentiment

This is the preferred method to install Boosting CV-LLM sentiment, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

Setting up the OpenAI API Key
-----------------------------

1. **Find Your API Key**: First, locate your API key from your OpenAI account under API settings.

2. **Configure the Key in Your Environment**:

   - **On Unix/Linux/macOS**:
     Open your terminal and run the following command, replacing ``YOUR_API_KEY`` with your actual OpenAI API key:

     .. code-block:: bash

        export OPENAI_API_KEY="YOUR_API_KEY"

     To make this change permanent, you can add the command to your ``~/.bashrc``, ``~/.zshrc``, or the configuration file of your shell.

   - **On Windows**:
     Open Command Prompt as an administrator and run:

     .. code-block:: cmd

        setx OPENAI_API_KEY "YOUR_API_KEY"

     Alternatively, you can set the environment variable through the System Properties. Search for "Edit the system environment variables" in the Start menu, click on "Environment Variables", and then add a new variable under "User variables" with the name ``OPENAI_API_KEY`` and your actual key as the value.

Verifying the Configuration
---------------------------

You can verify that your API key is set up correctly by running the following command in your terminal or Command Prompt:

- **Unix/Linux/macOS**:

  .. code-block:: bash

     echo $OPENAI_API_KEY

- **Windows**:

  .. code-block:: cmd

     echo %OPENAI_API_KEY%

If the command prints your API key, then you're all set.

Please ensure you keep your API key secure and do not share it publicly.


From sources
------------

The sources for Boosting CV-LLM sentiment can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/ToroData/boosting_cv_llm_sentiment

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/ToroData/boosting_cv_llm_sentiment/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/ToroData/boosting_cv_llm_sentiment
.. _tarball: https://github.com/ToroData/boosting_cv_llm_sentiment/tarball/master
