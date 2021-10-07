OneModel's syntax
=================

Model Elements
--------------

Comments
~~~~~~~~

OneModel supports single-line comments using the symbol ``#`` (everything written between a ``#`` and the end of the line will be considered as a comment).

::

  # This is a single line comment.

  # Species definiton.
  species x = 0   # Definition of x.

  parameter       # Start parameter block.
    k = 1         # Definition of k.
    d = 1         # Definition of d.
  end             # End of parameter block.

  reaction
    0 -> x; k     # Translation.
    x -> 0; d*x   # Degradation.
  end


Comments are ignored by OneModel and they wont appear in the generated SBML.

Parameters
~~~~~~~~~~


