# utils.py


# Function to get the intent name
def get_intent(event):
    intent_name = event["sessionState"]["intent"]["name"]
    return intent_name


# Function to get the session attributes
def get_session_attributes(event):
    session_attributes = event["sessionState"].get("sessionAttributes", {})
    return session_attributes


# Function to get all slots
def get_slots(event):
    slots = event["sessionState"]["intent"].get("slots", {})
    return slots


# Function to get a specific slot by name
def get_slot_value(event, slot_name):
    # Extract the slots from the event's session state
    slots = event.get("sessionState", {}).get("intent", {}).get("slots", {})

    # Get the slot from the slots dictionary
    slot_value = slots.get(slot_name, None)

    if slot_value is None:
        return None  # If the slot doesn't exist, return None

    # Check if the slot has a 'value' dictionary and extract the 'interpretedValue'
    value_dict = slot_value.get("value", {})
    interpreted_value = value_dict.get("interpretedValue", None)

    return interpreted_value
