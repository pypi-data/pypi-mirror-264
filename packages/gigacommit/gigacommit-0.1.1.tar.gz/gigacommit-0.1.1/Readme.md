# Generate commit messages with GigaChat

## Installing

The easiest way to install `gigacommit` is to use pip3:

    $ pip3 install gigacommit

or from sources:

    $ git clone https://git.dntsk.dev/DNTSK/gigacommit.git
    $ cd gigacommit
    $ python3 setup.py install

## Usage

Export GIGACHAT_TOKEN with authentication data:

```
export GIGACHAT_TOKEN="PASSYOURAUTHDATAHERE=="
```

Now you may stage your changes in git and run:

```
gigachat
```
