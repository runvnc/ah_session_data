from typing import Dict, Any, List, Union
import copy

def deep_update(target: Dict, source: Dict) -> Dict:
    """
    Recursively update a dictionary with another dictionary's values.
    Lists are replaced entirely (not merged).
    """
    target_copy = copy.deepcopy(target)
    
    for key, value in source.items():
        if key in target_copy and isinstance(target_copy[key], dict) and isinstance(value, dict):
            target_copy[key] = deep_update(target_copy[key], value)
        else:
            target_copy[key] = copy.deepcopy(value)
    
    return target_copy

def update_session_data(updates: Dict[str, Any], session_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Update session data with merge semantics - only specified fields are modified.
    Nested dictionaries are merged recursively. Lists are replaced entirely.
    
    Args:
        updates: Dictionary containing the updates to apply
        session_data: Existing session data (or None to start fresh)
    
    Returns:
        Updated session data dictionary
    """
    if session_data is None:
        session_data = {}
        
    return deep_update(session_data, updates)

def delete_session_data(path: List[str], session_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delete a value from session data at the specified path.
    
    Args:
        path: List of keys forming path to the value to delete
        session_data: Existing session data
        
    Returns:
        Updated session data dictionary
        
    Raises:
        KeyError: If path is invalid
    """
    if not path:
        raise ValueError("Path cannot be empty")
        
    result = copy.deepcopy(session_data)
    current = result
    
    # Navigate to parent of target
    for key in path[:-1]:
        if key not in current or not isinstance(current[key], dict):
            raise KeyError(f"Invalid path: {path}")
        current = current[key]
        
    # Delete target
    if path[-1] not in current:
        raise KeyError(f"Key not found: {path[-1]}")
    del current[path[-1]]
    
    return result

def add_to_session_list(path: List[str], value: Any, session_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a value to a list at the specified path in session data.
    Creates the list if it doesn't exist.
    
    Args:
        path: List of keys forming path to the target list
        value: Value to append to the list
        session_data: Existing session data
        
    Returns:
        Updated session data dictionary
        
    Raises:
        ValueError: If target exists but is not a list
    """
    result = copy.deepcopy(session_data)
    current = result
    
    # Navigate to parent of target
    for key in path[:-1]:
        if key not in current:
            current[key] = {}
        elif not isinstance(current[key], dict):
            raise ValueError(f"Cannot navigate path: {path}")
        current = current[key]
        
    # Handle target
    target_key = path[-1]
    if target_key not in current:
        current[target_key] = []
    elif not isinstance(current[target_key], list):
        raise ValueError(f"Target exists but is not a list: {path}")
        
    current[target_key].append(value)
    return result

def delete_from_session_list(path: List[str], index: int, session_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delete an item from a list at the specified path and index in session data.
    
    Args:
        path: List of keys forming path to the target list
        index: Index of item to delete
        session_data: Existing session data
        
    Returns:
        Updated session data dictionary
        
    Raises:
        KeyError: If path is invalid
        ValueError: If target is not a list or index out of range
    """
    result = copy.deepcopy(session_data)
    current = result
    
    # Navigate to parent of target
    for key in path[:-1]:
        if key not in current or not isinstance(current[key], dict):
            raise KeyError(f"Invalid path: {path}")
        current = current[key]
        
    # Handle target
    target_key = path[-1]
    if target_key not in current:
        raise KeyError(f"List not found: {path}")
    if not isinstance(current[target_key], list):
        raise ValueError(f"Target is not a list: {path}")
    if index < 0 or index >= len(current[target_key]):
        raise IndexError(f"List index out of range: {index}")
        
    del current[target_key][index]
    return result
