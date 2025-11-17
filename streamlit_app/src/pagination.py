def array_paginator(table, page_size, page_number):
    first_idx = (page_number -1) * page_size
    end_idx = first_idx + page_size
    return table[first_idx:end_idx]