{% if playbooks is defined %}
# Playbooks
{% for obj in playbooks %}
{{ "\u27A1" }} {{ obj.fname }} {% if obj.comment %}_({{ obj.comment }})_{% endif %}
{% endfor %}
{% endif %}
-
{% if inventories is defined %}
# Inventory files
{% for obj in inventories %}
{{ "\u27A1" }} {{ obj.fname }} {% if obj.comment %}_({{ obj.comment }})_{% endif %}
{% endfor -%}
{% endif %}
