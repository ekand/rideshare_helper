
community_sections = {'central': [8, 32, 33],
     'north_side': [5, 6, 7, 21, 22],
     'far_north_side': [1, 2, 3, 4, 9, 10, 11, 12, 13, 14, 76, 77],
     'northwest_side': [15, 16, 17, 18, 19, 20],
     'west_side': [23, 24, 25, 26, 27, 28, 29, 30, 31],
     'south_side': [34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 60, 69],
     'southwest_side': [56, 57, 58, 59, 61, 62, 63, 64, 65, 66, 67, 68],
     'far_southeast_side': [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55],
     'far_southwest_side': [70, 71, 72, 73, 74, 75]
                      }

community_areas = list(range(1, 78))


def community_areas_from_dict_func():
    t = []
    for value in community_sections.values():
        t.extend(value)
    return sorted(t)


assert list(range(1, 78)) == community_areas_from_dict_func()


# for a, b in zip(community_areas, community_areas_from_dict_func()):
#     print(a, b)
