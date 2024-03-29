===========
User Guide
===========

**Q1**: I've got a list of parameters for a user to edit in my PyQt application.
Is there an easy way to make a widget for them?

**A1**: See the :ref:`guide.ParameterEditor` section.

**Q2**: Great!  Now, I want to provide an editor for my application's
preferences.  There will be several sections, each with different terms to be
edited.

**A2**: See the :ref:`guide.ParameterTree` section.

**Q3**: Sounds easy enough.  How do I describe my parameters?

**A3**: See the :ref:`guide.ParameterItem` section.

**Q4**: How do I get the parameter values from editor widget or the tree dialog?

**A4**: See sections :ref:`guide:get-editor-values` and :ref:`guide:get-tree-values`, respectively.

This package simplifies the construction of a ``QWidget`` to edit a set of
parameters (of a PyQt5 application.)  It provides a single
:ref:`guide.ParameterEditor` screen for editing a set of
:ref:`guide.ParameterItem` objects and a :ref:`guide.ParameterTree` dialog for
editing a hierarchical structure with various sets of parameters.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :glob:

   param_item
   param_editor
   param_tree
