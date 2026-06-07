import re

with open("backend/app/services/hvac_analysis.py", "r") as f:
    content = f.read()

# Replace float conversion to handle ValueError
new_content = content.replace(
    'power_kw = float(node.properties.get("power_kW") or node.properties.get("rated_power_kW") or 0.0)',
    '''try:
            power_kw = float(node.properties.get("power_kW") or node.properties.get("rated_power_kW") or 0.0)
        except (ValueError, TypeError):
            power_kw = 0.0'''
)

new_content = new_content.replace(
    'cop = float(node.properties.get("cop") or 0.0)',
    '''try:
                    cop = float(node.properties.get("cop") or 0.0)
                except (ValueError, TypeError):
                    cop = 0.0'''
)

new_content = new_content.replace(
    'cooling = float(node.properties.get("cooling_capacity_kW") or 0.0)',
    '''try:
                    cooling = float(node.properties.get("cooling_capacity_kW") or 0.0)
                except (ValueError, TypeError):
                    cooling = 0.0'''
)

with open("backend/app/services/hvac_analysis.py", "w") as f:
    f.write(new_content)
