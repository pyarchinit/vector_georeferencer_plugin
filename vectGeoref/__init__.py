# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VectorGeoref
                                 A QGIS plugin
 A visual tool to georeferencing vector layers
                             -------------------
        begin                : 2013-11-11
        copyright            : (C) 2013 by Giuliano Curti
        email                : giulianc51@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load VectorGeoref class from file VectorGeoref
    from vectorgeoref import VectorGeoref
    return VectorGeoref(iface)
