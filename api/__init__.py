# __init__.py
# Copyright 2017 Roger Marsh
# Licence: See LICENCE (BSD licence)

'''A collection of modules containing functions used by applications on
www.solentware.co.uk which do not fit in solentware_base or solentware_grid,
siblings of solentware_misc, or are deliberately not put there.

The modulequery module imports attributes from the solentware_base package, but the
setup module for solentware_misc does not declare the dependency.  It is
assumed the solentware_base package will be present if modulequery is used.
'''
