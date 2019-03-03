{% load i18n %}
{% load extratags %}

function dd2dms(value, d1, d2) {
    value = parseFloat(value);
    var abs_value  = Math.abs(value);
    var degrees    = Math.floor(abs_value);
    var frac       = abs_value - degrees;
    var minutes    = Math.floor(frac * 60);
    var seconds    = Math.round((frac * 3600) % 60);

    return degrees + "°" + minutes + "'" + seconds + '"' + ((value > 0) ? d1 : d2);
}

function lonAdjust(lon) {
  while (lon > 180.0)  lon -= 360.0;
  while (lon < -180.0) lon += 360.0;
  return lon;
}

function metric_dist(lat1, lon1, lat2, lon2)
{
    var c = Math.PI/180.0;
    var r1 = lat1 * c;
    var r2 = lat2 * c;
    var th = lon1 - lon2;
    var radth = th * c;
    var dist = Math.sin(r1) * Math.sin(r2) + Math.cos(r1) * Math.cos(r2) * Math.cos(radth);
    if (dist > 1) dist = 1;
    return Math.acos(dist) * 10000 / 90;
}

