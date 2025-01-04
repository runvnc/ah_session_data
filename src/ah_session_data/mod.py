from lib.providers.commands import command
from lib.pipelines.pipe import pipeline_manager, pipe
from .session_data import (
    update_session_data,
    delete_session_data,
    add_to_session_list,
    delete_from_session_list
)
import traceback
from datetime import datetime
from tzlocal import get_localzone

def get_local_time_with_tz():
    local_tz = get_localzone()
    local_time = datetime.now(local_tz)
    return local_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')


def format_session_data(data: dict) -> str:
    return f"""

    ## Session Data 
     
    {str(data)}

    ___

    """


def add_formatted_session_data(data: dict, context_data: dict) -> dict:
    messages = data['messages']
    last_msg_content = messages[-1]['content']
    fmt_data = format_session_data(context_data['session'])
    print("ah_session_data: Found session data in context data")
    print(fmt_data)
    if isinstance(last_msg_content, str):
        print("ah_session_data: Last message content is a string")
        messages[-1]['content'] = fmt_data + last_msg_content
        data['messages'] = messages
        return data
    elif isinstance(last_msg_content, list):
        obj = { "type": "text", "text": fmt_data }
        messages[-1]['content'].insert(0, obj)
        data['messages'] = messages
        return data
    elif isinstance(last_msg_content, dict):
        print("ah_session_data: Last message content is a dict")
        if last_msg_content['type'] == 'text':
            messages[-1]['content']['text'] = fmt_data + last_msg_content['text']
            data['messages'] = messages
        return data


@pipe(name='filter_messages', priority=8)
def add_session_data(data: dict, context=None) -> dict:
    """
    Add context.data['session'] to the front of last message
    Message content may be a string or list
    If list then insert a text entry at the front

    If there is no 'session' in context.data then do nothing.
    """
    try:
        print("\033[43;34m add_session_data \033[m")
        if context is None or not hasattr(context, 'data'):
            print("No context data found in ah_session_data")
            return data
            
        if 'session' in context.data:
            return add_formatted_session_data(data, context.data)
        else:
            print("ah_session_data: No session data in context data. adding timestamp")
            context.data['session'] = { "server_time": str(datetime.now()) }
            return add_formatted_session_data(data, context.data)

    except Exception as e:
        trace = traceback.format_exc()
        print(f"\033[41;37m Error in ah_session_data: \n {e} \n {trace} \033[m")
        return data


@command()
async def session_data_update(updates: dict, context=None) -> dict:
    """
    Update session data with merge semantics - only specified fields are modified.
    Nested dictionaries are merged recursively. Lists are replaced entirely.
    """
    if context is None or not hasattr(context, 'data'):
        raise ValueError("Context or context.data not available")
        
    if 'session' not in context.data:
        context.data['session'] = {}

    context.data['session'] = update_session_data(updates, context.data['session'])
    return context.data['session']


@command()
async def session_data_del(path: list, context=None) -> dict:
    """
    Delete a value from session data at the specified path.
    """
    if context is None or not hasattr(context, 'data') or 'session' not in context.data:
        raise ValueError("No session data exists")

    context.data['session'] = delete_session_data(path, context.data['session'])
    return context.data['session']


@command()
async def session_data_list_add(path: list, value: any, context=None) -> dict:
    """
    Add a value to a list at the specified path in session data.
    Creates the list if it doesn't exist.
    """
    if context is None or not hasattr(context, 'data'):
        raise ValueError("Context or context.data not available")
        
    if 'session' not in context.data:
        context.data['session'] = {}

    context.data['session'] = add_to_session_list(path, value, context.data['session'])
    return context.data['session']


@command()
async def session_data_list_del(path: list, index: int, context=None) -> dict:
    """
    Delete an item from a list at the specified path and index in session data.
    """
    if context is None or not hasattr(context, 'data') or 'session' not in context.data:
        raise ValueError("No session data exists")

    context.data['session'] = delete_from_session_list(path, index, context.data['session'])
    return context.data['session']
