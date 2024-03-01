import json
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

def convert_pda_json_to_jff(json_filename):
    # Read JSON file
    with open(json_filename, 'r') as json_file:
        data = json.load(json_file)

    # Create the base structure of the JFF file
    structure = Element('structure')
    type_element = SubElement(structure, 'type')
    type_element.text = 'pda'  # Specify type as PDA
    automaton = SubElement(structure, 'automaton')

    # Add states to the automaton
    for state in data['states']:
        state_element = SubElement(automaton, 'state', attrib={'id': str(state['id']), 'name': f"q{state['id']}"})
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
        # PDA specific elements for read, pop, and push operations
        SubElement(transition_element, 'read').text = transition['read'] if transition['read'] else "ε"
        SubElement(transition_element, 'pop').text = transition['pop'] if transition['pop'] else "ε"
        SubElement(transition_element, 'push').text = transition['push'] if transition['push'] else "ε"

    # Convert the ElementTree to a string and format it with minidom for pretty printing
    xml_str = tostring(structure, 'utf-8')
    pretty_xml_str = parseString(xml_str).toprettyxml()

    # Save the formatted XML to a .jff file with UTF-8 encoding
    jff_filename = json_filename.replace('.json', '.jff')
    with open(jff_filename, 'w', encoding='utf-8') as jff_file:
        jff_file.write(pretty_xml_str)

    print(f"Converted {json_filename} to {jff_filename}")


# Replace 'path_to_your_pda_json_file.json' with the actual path to your JSON file
convert_pda_json_to_jff('Envious Fountain.json')
