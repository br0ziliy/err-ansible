{%- if playbooks is defined %}
*Playbooks:*

| Filename | Comment
-----------|--------
{% for obj in playbooks -%}
{{ obj.fname }} | {{ obj.comment }} 
{% endfor %}{% endif %}

{%- if inventories is defined %}
*Inventory files:*

| Filename | Comment
-----------|--------
{% for obj in inventories -%}
{{ obj.fname }} | {{ obj.comment }}
{% endfor %}{% endif %}


