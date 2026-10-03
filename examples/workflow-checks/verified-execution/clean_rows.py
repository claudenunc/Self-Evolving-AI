def clean_rows(rows):
    seen = set()
    result = []
    for row in rows:
        key = row.get('id')
        if key is not None and key != '' and key not in seen:
            seen.add(key)
            result.append(row)
    return result
