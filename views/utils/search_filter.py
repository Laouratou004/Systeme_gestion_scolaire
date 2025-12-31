# views/utils/search_filter.py
"""
Module utilitaire pour la recherche et le filtrage de données
"""

def search_in_list(data_list, search_term, fields):
    """
    Recherche dans une liste de tuples/listes
    
    Args:
        data_list: Liste de données (tuples ou listes)
        search_term: Terme de recherche
        fields: Indices des colonnes à rechercher
    
    Returns:
        Liste filtrée
    
    Exemple:
        data = [(1, "Jean", "Dupont", "L3"), (2, "Marie", "Martin", "L2")]
        result = search_in_list(data, "Jean", [1, 2])  # Recherche dans colonnes 1 et 2
    """
    if not search_term or not search_term.strip():
        return data_list
    
    search_term = search_term.lower().strip()
    filtered = []
    
    for row in data_list:
        # Rechercher dans les champs spécifiés
        for field_index in fields:
            if field_index < len(row):
                field_value = str(row[field_index]).lower()
                if search_term in field_value:
                    filtered.append(row)
                    break  # Éviter les doublons
    
    return filtered


def filter_by_value(data_list, column_index, filter_value):
    """
    Filtre une liste par une valeur dans une colonne spécifique
    
    Args:
        data_list: Liste de données
        column_index: Indice de la colonne à filtrer
        filter_value: Valeur à rechercher (ou "Tous" pour tout afficher)
    
    Returns:
        Liste filtrée
    """
    if not filter_value or filter_value == "Tous":
        return data_list
    
    filtered = []
    for row in data_list:
        if column_index < len(row):
            if str(row[column_index]) == str(filter_value):
                filtered.append(row)
    
    return filtered


def sort_data(data_list, column_index, reverse=False):
    """
    Trie une liste par une colonne spécifique
    
    Args:
        data_list: Liste de données
        column_index: Indice de la colonne pour le tri
        reverse: True pour ordre décroissant
    
    Returns:
        Liste triée
    """
    if not data_list:
        return data_list
    
    try:
        # Trier en gérant les valeurs None et les types mixtes
        sorted_list = sorted(
            data_list,
            key=lambda x: (x[column_index] is None, str(x[column_index]).lower() if x[column_index] is not None else ""),
            reverse=reverse
        )
        return sorted_list
    except Exception as e:
        print(f"Erreur de tri: {e}")
        return data_list


def get_unique_values(data_list, column_index):
    """
    Récupère les valeurs uniques d'une colonne
    
    Args:
        data_list: Liste de données
        column_index: Indice de la colonne
    
    Returns:
        Liste des valeurs uniques triées
    """
    if not data_list:
        return []
    
    unique_values = set()
    for row in data_list:
        if column_index < len(row) and row[column_index] is not None:
            unique_values.add(str(row[column_index]))
    
    return sorted(list(unique_values))


def apply_filters(data_list, search_term="", search_fields=None, filters=None, sort_column=None, sort_reverse=False):
    """
    Applique tous les filtres et tris sur une liste de données
    
    Args:
        data_list: Liste de données
        search_term: Terme de recherche
        search_fields: Indices des colonnes pour la recherche
        filters: Dict {column_index: filter_value}
        sort_column: Indice de la colonne pour le tri
        sort_reverse: Ordre de tri
    
    Returns:
        Liste filtrée et triée
    """
    result = data_list
    
    # Appliquer la recherche
    if search_term and search_fields:
        result = search_in_list(result, search_term, search_fields)
    
    # Appliquer les filtres
    if filters:
        for column_index, filter_value in filters.items():
            result = filter_by_value(result, column_index, filter_value)
    
    # Appliquer le tri
    if sort_column is not None:
        result = sort_data(result, sort_column, sort_reverse)
    
    return result