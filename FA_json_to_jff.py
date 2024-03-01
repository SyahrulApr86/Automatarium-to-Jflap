import json
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString


def convert_json_to_jff(json_filename):
    # Read JSON file
    with open(json_filename, 'r') as json_file:
        data = json.load(json_file)

    # Create the base structure of the JFF file
    structure = Element('structure')
    type_element = SubElement(structure, 'type')
    type_element.text = 'fa'
    automaton = SubElement(structure, 'automaton')

    # Add states to the automaton
    for state in data['states']:
        # Use state ID to generate a name if 'name' key is missing
        state_name = f"q{state['id']}"
        state_element = SubElement(automaton, 'state', attrib={'id': str(state['id']), 'name': state_name})
        SubElement(state_element, 'x').text = str(state['x'])
        SubElement(state_element, 'y').text = str(state['y'])
        if state.get('isFinal', False):
            SubElement(state_element, 'final')
        if data['initialState'] == state['id']:
            SubElement(state_element, 'initial')

    # Add transitions to the automaton
    for transition in data['transitions']:
        transition_element = SubElement(automaton, 'transition')
        SubElement(transition_element, 'from').text = str(transition['from'])
        SubElement(transition_element, 'to').text = str(transition['to'])
        SubElement(transition_element, 'read').text = transition['read']

    # Convert the ElementTree to a string and format it with minidom for pretty printing
    xml_str = tostring(structure, 'utf-8')
    pretty_xml_str = parseString(xml_str).toprettyxml()

    # Save the formatted XML to a .jff file
    jff_filename = json_filename.replace('.json', '.jff')
    with open(jff_filename, 'w') as jff_file:
        jff_file.write(pretty_xml_str)

    print(f"Converted {json_filename} to {jff_filename}")

filename = 'Envious Fountain'
convert_json_to_jff(f'{filename}.json')