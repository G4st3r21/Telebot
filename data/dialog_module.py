import dialogflow
from google.api_core.exceptions import InvalidArgument


def AI_chatting(text):
    DIALOGFLOW_PROJECT_ID = 'tardis-isbv'
    DIALOGFLOW_LANGUAGE_CODE = 'ru-RU'
    GOOGLE_APPLICATION_CREDENTIALS = 'data\Answers\small-talk-xbwx-d6e32b0bddf4.json'
    SESSION_ID = '102526221439446739333'
    text_to_be_analyzed = text
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(
        text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(
            session=session, query_input=query_input)
    except InvalidArgument:
        raise
    
    return response.query_result.fulfillment_text
