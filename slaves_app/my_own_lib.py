

def remove_redundancy_items_from_a_list(queryset):
    queryset = list(dict.fromkeys(queryset))
    return queryset



