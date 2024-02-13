from icecream import ic
import time
from openai import OpenAI


class Response:
    def __init__(self, status, content):
        self.status = status
        self.content = content

class AssistantWrapper:
    def __init__(self, assistant_name, user_api_key=None):
        if user_api_key==None:
            print("You must enter your valid API KEY to use this service")
        self.conversation = []
        self.client = OpenAI(api_key=user_api_key)  # This should be authenticated already.
        self.assistant_name = assistant_name
        self.assistant_id = self.get_assistant_id_by_name(assistant_name)

    def get_assistant_id_by_name(self, assistant_name):
        ic(assistant_name)
        assts = {'HennyOldman': 'asst_CdtzlCNGkogXmBj5NX0NlmU6',
                 'henny': 'asst_CdtzlCNGkogXmBj5NX0NlmU6', 
                 'DFB': 'asst_dvc4PpLMBzzBRrJBlth9EkoI', 
                 'dfb': 'asst_dvc4PpLMBzzBRrJBlth9EkoI', 
                 'SerpAssist': 'asst_RWOTpjEA0KHXW7bAV7LjJMdq', 
                 'serpassist': 'asst_RWOTpjEA0KHXW7bAV7LjJMdq', 
                 'BIE': 'asst_oJEOSFB8BJAAeHzg1gmcFkzu', 
                 'bie': 'asst_oJEOSFB8BJAAeHzg1gmcFkzu', 
                 'CritSum': 'asst_bhGiDuYCxXgkWshvM1GDBRWV',
                 'critsum': 'asst_bhGiDuYCxXgkWshvM1GDBRWV'}
        return assts[assistant_name]  # this will Throw if you don't know your assistants name...

    def create_thread(self):
        thread = self.client.beta.threads.create()
        return thread

    def submit_message(self, thread, user_message):
        message = self.client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=user_message
        )
        # is the message even used anywhere?
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id,
        )
        return run

    def wait_on_run(self, run, thread):
        while run.status in ["queued", "in_progress"]:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run

    def get_response(self, thread):
        messages = self.client.beta.threads.messages.list(thread_id=thread.id, order="asc")  # returns a SyncCursorPage[ThreadMessage]
        return messages.model_dump()

    def _extract_response(self, msg_dict):
        try:
            msg_data = msg_dict['data']  # a list 
            # ic(msg_data)
            if len(msg_data) < 2:
                # Something wrong here...
                ic(len(msg_data), msg_data)
            else:
                reply = msg_data[-1]  # take the last one...
                # ic("reply: ", reply)
            message_reply = reply['content'][0]['text']['value']
            return message_reply
        except Exception as e:
            ic("_extract_response Exception", e)
            return str(e)

    def ask(self, user_message):
        try:
            self.conversation.append(user_message)
            thread = self.create_thread()
            run = self.submit_message(thread, user_message)
            run = self.wait_on_run(run, thread)
            msg_dict = self.get_response(thread)  # returns a dict()    
            # ic(msg_dict)
            message_reply = self._extract_response(msg_dict)
            # ic(message_reply)
            self.conversation.append(message_reply)
            return Response("OK", message_reply)
        except Exception as e:
            ic("ask Exception", e)
            return Response("Error", str(e))


# henny_response = henny.ask("What is the airspeed of an unladen swallow")

# print(f"Status: {response.status}")
# print(f"Content: {response.content}")
# print("\n".join(assistant.conversation))