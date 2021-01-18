# some graphical artefacts

from folium.features import DivIcon


def centered_circle(label, diameter, circle_color):
    radius = diameter // 2
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve"
style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd"
viewBox="0 0 {diameter} {diameter}">
  <g id="label">
<!--    <circle style="fill:url(#toning);stroke:#010101;stroke-width:.3;stroke-miterlimit:10;" cx="{radius}" cy="{radius}" r="{radius}">
    </circle> -->
    <text x="50%" y="50%" text-anchor="middle" stroke="#{circle_color}" stroke-width="1px" dy=".3em">{label}</text>
  </g>
</svg>"""


def label_icon(label, *, diameter=20, circle_color='#d22'):
    return DivIcon(
        icon_size=(diameter, diameter),
        icon_anchor=(diameter, 0),
        class_name="leaflet-div-icon",
        html=centered_circle(label, diameter, circle_color))
