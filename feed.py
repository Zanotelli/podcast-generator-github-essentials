import yaml
import xml.etree.ElementTree as xml_tree

###
# Usa como exemplo um modelo para consturção de arquivos RSS da Apple
# https://help.apple.com/itc/podcasts_connect/#/itcbaf351599
###

# Abre arquivo yaml no mode leitura
with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

    # Cria um elemento com tag 'rss'
    rss_element = xml_tree.Element('rss', {
        'version': "2.0",
        'xmlns:itunes': "http://www.itunes.com/dtds/podcast-1.0.dtd",
        'xmlns:content': "http://purl.org/rss/1.0/modules/content/"
    })

    channel_element = xml_tree.SubElement(rss_element, 'channel')

    link_prefix = yaml_data['link']

    # Leitura de informações gerais
    xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
    xml_tree.SubElement(channel_element, 'format').text = yaml_data['format']
    xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
    xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
    xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']
    xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
    xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data['image']})
    xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})
    xml_tree.SubElement(channel_element, 'link').text = link_prefix

    # Adiciona lista de Itens
    for item in yaml_data['item']:
        item_element = xml_tree.SubElement(channel_element, 'item')
        xml_tree.SubElement(item_element, 'title').text = item['title']
        xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data['author']
        xml_tree.SubElement(item_element, 'description').text = item['description']
        xml_tree.SubElement(item_element, 'pubDate').text = item['published']
        xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']

        enclosure = xml_tree.SubElement(item_element, 'enclosure', {
            'url': link_prefix + item['file'],
            'length': link_prefix + item['length'],
            'type': 'audio/mpeg'
        })

    # Cria a árevore XML usando o objeto 'rss' como base
    output_tree = xml_tree.ElementTree(rss_element)

    # Escreve o XML em um erquivo
    output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)
