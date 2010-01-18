# coding: utf-8

# maposmatic, the web front-end of the MapOSMatic city map generation system
# Copyright (C) 2009  David Decotigny
# Copyright (C) 2009  Frédéric Lehobey
# Copyright (C) 2009  Pierre Mauduit
# Copyright (C) 2009  David Mentré
# Copyright (C) 2009  Maxime Petazzoni
# Copyright (C) 2009  Thomas Petazzoni
# Copyright (C) 2009  Gaël Utard

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import psycopg2

from ocitysmap.coords import BoundingBox as OCMBoundingBox
from www.maposmatic.models import MapRenderingJob
import www.settings

def check_osm_id(osm_id, table='polygon'):
    """Make sure that the supplied OSM Id is valid and can be accepted for
    rendering (bounding box not too large, etc.). Raise an exception in
    case of error."""

    # If no GIS database is configured, bypass the city_exists check by
    # returning True.
    if not www.settings.has_gis_database():
        raise ValueError("No GIS database available")

    conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %
                            (www.settings.GIS_DATABASE_NAME,
                             www.settings.DATABASE_USER,
                             www.settings.DATABASE_HOST,
                             www.settings.DATABASE_PASSWORD))

    try:
        cursor = conn.cursor()
        cursor.execute("""select osm_id,st_astext(st_transform(st_envelope(way),
                                                               4002))
                          from planet_osm_%s where
                          osm_id=%d""" % (table,int(osm_id)))
        result = cursor.fetchall()
        try:
            ((ret_osm_id, envlp),) = result
        except ValueError:
            raise ValueError("Cannot lookup OSM ID in table %s" % table)

        assert ret_osm_id == osm_id

        # Check bbox size
        bbox = OCMBoundingBox.parse_wkt(envlp)
        (metric_size_lat, metric_size_long) = bbox.spheric_sizes()
        if metric_size_lat > www.settings.BBOX_MAXIMUM_LENGTH_IN_METERS or \
                metric_size_long > www.settings.BBOX_MAXIMUM_LENGTH_IN_METERS:
            raise ValueError("Area too large")

    finally:
        conn.close()

def rendering_already_exists(osmid):
    """Returns the ID of a rendering matching the given OpenStreetMap city ID
    from the last 24 hours, or None if no rendering can be found matching this
    criteria."""

    # First try to find rendered items
    rendered_items = (MapRenderingJob.objects
                      .filter(submission_time__gte=(datetime.datetime.now()
                                                   - datetime.timedelta(1)))
                      .filter(administrative_osmid=osmid)
                      .filter(status=2)
                      .filter(resultmsg="ok")
                      .order_by("-submission_time")[:1])

    if len(rendered_items) and rendered_items[0].has_output_files():
        return rendered_items[0].id

    # Then try to find items being rendered or waiting for rendering
    rendered_items = (MapRenderingJob.objects
                      .filter(submission_time__gte=(datetime.datetime.now()
                                                   - datetime.timedelta(1)))
                      .filter(administrative_osmid=osmid)
                      .filter(status__in=[0,1])
                      .order_by("-submission_time")[:1])

    if len(rendered_items):
        return rendered_items[0].id

    # No rendering found
    return None

def get_letters():
    """Returns the list of map first-letter selectors. For now, it only returns
    the ASCII letters of the latin alphabet. This should be improved for
    different languages!"""

    # Should we improve this to differenciate letters that have maps from those
    # who don't?
    return [chr(i) for i in xrange(ord('A'), ord('Z')+1)]

