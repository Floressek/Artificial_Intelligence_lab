#  Gardening system - Szymon Florek WCY22IY2S1 82077

import random


def yellow_leaves(information):
    """Determines whether the leaves are yellowish or not. If the leaves are yellowish, it may indicate that the
    plant"""
    if information.get('Leaves are yellowish'):
        return 'The leaves are yellowish, which may indicate the plant requires more water'
    return 'The leaves are not yellowish. Maintain regular checks.'


def brown_tips(information):
    """Determines whether the leaves have brown tips or not. If the leaves have brown tips, it may indicate that the"""
    if information.get('Leaves have brown tips'):
        if not information.get('Leaves are yellowish.', False):
            return 'The leaves have brown tips, which could be due to overwatering or nutrient deficiency.'
    return 'The leaves do not have brown tips. Maintain regular checks.'


def wilting_plant(information):
    """Determines cause of plant wilting based on color leaf and wilting status"""
    # if information.get('The plant is wilting', False): if information.get('Leaves are yellowish', False): return
    # 'The plant is wilting and the leaves are yellowish, which could be due to plant needing more water.' elif
    # information.get('Leaves have brown tips', False): return 'The plant is wilting and the leaves have brown tips,
    # which could be due to overwatering or ' \ 'lack of sufficient watering.' return 'The plant is not wilting. This
    # could be due to other reasons.'
    wilting = information.get('The plant is wilting')
    yellowish = information.get('Leaves are yellowish')
    brownish_tips = information.get('Leaves have brown tips')

    if wilting:
        if yellowish:
            return 'The plant is wilting and the leaves are yellowish, which could be due to plant needing more water.'
        elif brownish_tips:
            return 'The plant is wilting and the leaves have brown tips, which could be due to overwatering or ' \
                   'lack of sufficient watering.'
        else:
            return 'The plant is wilting but shows no other clear symptoms, consider checking the root damage or pests.'


def spot_on_the_leaves(information):
    """Determines if the leaves have spots and provides a recommendation based on the presence of spots."""
    if information.get('Leaves have spots', False):
        return 'The leaves have spots, which could be due to a fungal infection. It is recommended to apply the ' \
               'antifungal agent'
    return 'The leaves do not have spots. Maintain regular checks.'


def plant_growth_stunted(information):
    """Determines if the plant growth is stunted based on the information provided."""
    if information.get('Plant growth is stunted', False):
        return 'The plant growth is stunted, which could be due to lack of nutrients or overwatering. Consider ' \
               'adjusting yhe water schedule and verifying the soil fertility.'
    return 'The plant growth is not stunted. Keep monitoring other symptoms for further diagnosis.'


# Set of rules based on our gardening system
rules = [yellow_leaves, brown_tips, wilting_plant, spot_on_the_leaves, plant_growth_stunted]


def reasoning(information, set_of_rules):
    """Reasoning function that applies the rules to the information provided and returns the reasons."""
    reasons = []
    for rule in set_of_rules:
        reason_result = rule(information)
        if reason_result:
            reasons.append(reason_result)
    return reasons


plants = {
    'Rose': {'Leaves are yellowish': True, 'Leaves have brown tips': False, 'The plant is wilting': True},
    'Lily': {'Leaves are yellowish': False, 'Leaves have brown tips': True, 'The plant is wilting': False},
    'Orchid': {'Leaves are yellowish': False, 'Leaves have brown tips': False, 'The plant is wilting': False,
               'Leaves have spots': True},
    'Tulip': {'Leaves are yellowish': False, 'Leaves have brown tips': False, 'The plant is wilting': False,
              'Leaves have spots': False, 'Plant growth is stunted': True},
    'Cactus': {'Leaves are yellowish': False, 'Leaves have brown tips': False, 'The plant is wilting': False,
               'Leaves have spots': False, 'Plant growth is stunted': False}
}

# Assumed that when the leaf has only one certain color
plants_random = {plant: {'Leaves are yellowish': random.choice([True, False]),
                         'Leaves have brown tips': not yellow_leaves,
                         'The plant is wilting': random.randint(0, 1),
                         'Leaves have spots': random.randint(0, 1),
                         'Plant growth is stunted': random.randint(0, 1)}
                 for plant in ['Rose', 'Lily', 'Orchid', 'Tulip', 'Cactus']}

"""Determines the symptoms of the plants based on the rules and information provided."""
for name, info_plants in plants_random.items():
    result = reasoning(info_plants, rules)
    if result:
        print(f"{name}: {', '.join(result)}.")
    else:
        print(f'{name}: No symptoms found.')
