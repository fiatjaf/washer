======
washer
======
Create fulltext indexes with your files and query them from the command line.
------

Install
-------

With pip or (better) `pipsi <https://github.com/mitsuhiko/pipsi>`:

::

    pipsi install --python (which python3) washer
    # or `sudo pip3 install washer`


Usage
-----

::

    Usage: washer [OPTIONS] COMMAND [ARGS]...
    
    Options:
      -d, --indexdir DIRECTORY  The directory in which the index files will be
                                kept. Defaults to a temporary directory.
      --help                    Show this message and exit.
    
    Commands:
      index     Creates or overwrites and index at an...
      info      Display information about the index and...
      morelike  Lists files present at the index that share...
      search    Search the given index for a term or multiple...

::

    Usage: washer index [OPTIONS] [FILES_TO_INDEX]...
    
      Creates or overwrites and index at an specified location using the given
      files.
    
      FILES_TO_INDEX accepts multiple files and wildcards, as usual.
    
    Options:
      -l, --lang [ar|da|nl|en|fi|fr|de|hu|it|no|pt|ro|ru|es|sv|tr]
                                      Comma-separated list of languages to use
                                      when indexing. Should be specified multiple
                                      times. Defaults to "-l pt -l en".
      --help                          Show this message and exit.


::

    Usage: washer search [OPTIONS] [QUERY]...
    
      Search the given index for a term or multiple terms.
    
      QUERY can be anything, typically it will be just one or a bunch of words,
      but it accepts special operators (NOT, AND, *, ? etc.) as specified in
      http://whoosh.readthedocs.io/en/latest/querylang.html
    
    Options:
      --count             Force counting results. A mostly useless flag.
      --frag / --no-frag  Show text fragments of the files that matched.Enabled by
                          default.
      --help              Show this message and exit.

License
-------

This tool is licensed in the same way as Whoosh, as long as it complies with requirements from the other two dependencies, Click and blessings.
