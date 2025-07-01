.. vim: set fileencoding=utf-8:
.. -*- coding: utf-8 -*-
.. +--------------------------------------------------------------------------+
   |                                                                          |
   | Licensed under the Apache License, Version 2.0 (the "License");          |
   | you may not use this file except in compliance with the License.         |
   | You may obtain a copy of the License at                                  |
   |                                                                          |
   |     http://www.apache.org/licenses/LICENSE-2.0                           |
   |                                                                          |
   | Unless required by applicable law or agreed to in writing, software      |
   | distributed under the License is distributed on an "AS IS" BASIS,        |
   | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
   | See the License for the specific language governing permissions and      |
   | limitations under the License.                                           |
   |                                                                          |
   +--------------------------------------------------------------------------+


*******************************************************************************
Accretive Modules
*******************************************************************************


Introduction
===============================================================================

The ``accretive.modules`` submodule provides functionality to enhance Python
modules with accretive behavior and concealment, with optional automatic
documentation generation. This is particularly useful for package authors who
want to prevent accidental modification of their module's existing attributes
while allowing new attributes to be added and providing rich documentation.

The module provides two main approaches:

1. **Module reclassification** - converts standard modules to have accretive 
   and concealed attributes
2. **Module finalization** - combines documentation generation with
   reclassification in a single convenient function


Module Reclassification
===============================================================================

The ``reclassify_modules`` function converts modules to use a custom module
class that provides accretive and concealment behaviors. Here's how you
might use it in a hypothetical package:

.. code-block:: python

    # mypackage/__init__.py
    import accretive
    
    # Import your submodules
    from . import core
    from . import utils
    from . import exceptions
    
    # Apply module reclassification
    accretive.reclassify_modules( __name__, recursive = True )

After reclassification, the modules become accretive:

.. code-block:: python

    # This would raise AttributeImmutability exception
    # mypackage.core.some_function = "modified"
    
    # But new attributes can be added
    mypackage.core.new_feature = "allowed"
    
    # Non-public attributes are concealed from dir()
    # dir( mypackage )  # Only shows public attributes

The ``recursive = True`` parameter ensures that all submodules within the
package hierarchy are also reclassified, providing consistent behavior
throughout your package.


Individual Module Reclassification
-------------------------------------------------------------------------------

You can also reclassify individual modules without affecting the entire
package hierarchy:

.. code-block:: python

    # mypackage/core.py
    import accretive
    
    def important_function():
        ''' This function should not be accidentally modified. '''
        return "Important result"
    
    # Reclassify only this module
    accretive.reclassify_modules( __name__ )

This approach is useful when you want fine-grained control over which modules
in your package receive the enhanced behaviors.


Module Finalization with Documentation
===============================================================================

The ``finalize_module`` function provides a convenient way to combine automatic
documentation generation (via Dynadoc integration) with module reclassification.
This is the recommended approach for most packages.

Basic Usage
-------------------------------------------------------------------------------

.. code-block:: python

    # mypackage/__init__.py
    import accretive
    
    from . import core
    from . import utils
    from . import exceptions
    
    # Finalize the module with documentation and reclassification
    accretive.finalize_module( __name__, recursive = True )

The ``finalize_module`` function will:

1. Generate comprehensive documentation for the module and its members using
   Dynadoc introspection
2. Apply any documentation fragments you provide
3. Reclassify the module and its submodules for accretion and concealment

Advanced Configuration
-------------------------------------------------------------------------------

For complex packages, you might want to configure different parts differently:

.. code-block:: python

    # mypackage/__init__.py
    import accretive
    
    # Configure main package with full documentation
    accretive.finalize_module(
        __name__,
        recursive = False  # Handle submodules individually
    )
    
    # Configure submodules with different settings
    accretive.finalize_module(
        f"{__name__}.core",
        recursive = True
    )
    
    accretive.finalize_module(
        f"{__name__}.utils",
        recursive = True
    )

This approach allows you to provide different documentation and
introspection settings for different parts of your package.


Best Practices
===============================================================================

Package-Level Application
-------------------------------------------------------------------------------

For most packages, apply ``finalize_module`` at the package level in your
``__init__.py`` file:

.. code-block:: python

    # mypackage/__init__.py
    import accretive
    
    # Package metadata
    __version__ = '1.0.0'
    
    # Import public API
    from .core import PublicClass, public_function
    from .utils import helper_function
    
    # Finalize the entire package
    accretive.finalize_module( __name__, recursive = True )

This pattern ensures that:

- Your package's public API is documented
- All modules in the package are accretive and concealed
- The entire package hierarchy is protected from accidental modification of existing attributes

Error Handling
-------------------------------------------------------------------------------

When using module finalization, be aware that the resulting modules will raise
``AttributeImmutability`` exceptions if code attempts to modify existing attributes:

.. code-block:: python

    import accretive.exceptions
    
    # After finalization, this will raise an exception
    try:
        mypackage.core.some_function = lambda: "modified"
    except accretive.exceptions.AttributeImmutability as e:
        print( f"Cannot modify existing attribute: {e}" )
    
    # But this is allowed
    mypackage.core.new_attribute = "this works"

Design your package APIs to avoid modification of existing attributes after 
finalization. If you need dynamic behavior, consider using configuration 
objects or factory functions instead of direct module attribute modification.


Integration with Build Systems
===============================================================================

Module finalization integrates well with modern Python build systems. The
accretive behavior ensures that your package's API surface is clearly defined
and existing attributes cannot be accidentally modified at runtime while still
allowing extension.

For packages that use entry points or plugin systems, apply finalization after
all dynamic setup is complete:

.. code-block:: python

    # mypackage/__init__.py
    import accretive
    
    # Dynamic setup (plugin registration, etc.)
    _setup_plugins()
    _register_entry_points()
    
    # Final API definition
    from .api import *
    
    # Lock down the package
    accretive.finalize_module( __name__, recursive = True )

This ensures that your package initialization is complete before the
accretive protections are applied.