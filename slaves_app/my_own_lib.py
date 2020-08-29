

def remove_redundancy_items_from_the_list(queryset):
    queryset = list(dict.fromkeys(queryset))
    return queryset



