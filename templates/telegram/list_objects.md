{%- if playbooks is defined %}
*Playbooks:*

{% for obj in playbooks -%}
* {{ obj.fname }} _({{ obj.comment }})_
{% endfor %}{% endif %}

{%- if inventories is defined %}
*Inventory files:*

{% for obj in inventories -%}
* {{ obj.fname }} _({{ obj.comment }})_
{% endfor %}{% endif %}

