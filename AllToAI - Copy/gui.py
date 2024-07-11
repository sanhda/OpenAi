
try:
    import wx
    from openai import OpenAI
except Exception as e:
    print("Missing library: " + str(e))

from .const import *
# from .data_process import DataProcess

client = OpenAI(api_key=API_KEY)

class ChatBotFrame(wx.Frame):
    def __init__(self, doc, *args, **kwargs):
        super(ChatBotFrame, self).__init__(*args, **kwargs)
        
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.chat_display = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.sizer.Add(self.chat_display, 1, wx.EXPAND | wx.ALL, 5)
        
        self.user_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.sizer.Add(self.user_input, 0, wx.EXPAND | wx.ALL, 5)
        
        self.user_input.Bind(wx.EVT_TEXT_ENTER, self.on_enter_pressed)

        # self.data_process = DataProcess(doc)
        
        self.panel.SetSizer(self.sizer)
        self.SetTitle('Chatbot Interface')
        self.Show()
    
    def on_enter_pressed(self, event):
        user_message = self.user_input.GetValue()
        self.chat_display.AppendText(f'You: {user_message}\n')
        
        response = self.get_bot_response(user_message)
        self.chat_display.AppendText(f'Bot: {response}\n')
        
        self.user_input.SetValue('')

    def get_bot_response(self, prompt):
        details_keys = "<key>=<value>"
        conditions_keys = "; ".join([f"{key}=<value>" for key in CONDITION_KEYS])
        valid_actions = "; ".join(ACTION_KEYS)
        valid_objects = "; ".join(OBJECT_KEYS)
        
        conversation = [
            {"role": "system", "content": f"You are a helpful assistant. Interpret user requests for actions on objects modification. Respond in English." \
                                        + f"The action must be one of the following: {valid_actions}." \
                                        + f"The object must be one of the following: {valid_objects}." \
                                        + f"If the request is an action, respond with 'Action: <action>|<object>|{conditions_keys}|{details_keys}'." \
                                        + f"If the request is invalid, respond with 'Error: Unrecognized action'."},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=conversation,
            max_tokens=150
        )

        ai_response = response.choices[0].message.content
        return ai_response
        response_type, action, obj, conditions, details = self.parse_response(ai_response)

        if response_type == "action":
            response = self.data_process.process_action(action, obj, conditions, details)
            return response
        else:
            return "Can not recognize the command"

    def parse_response(self, response):
        if response.startswith("Action: "):
            parts = response[7:].split("|")
            action = parts[0].strip()
            obj = parts[1].strip() if len(parts) > 1 else None
            conditions = parts[2].strip() if len(parts) > 2 else ""
            details = parts[3].strip() if len(parts) > 3 else ""
            return "action", action, obj, conditions, details

        else:
            return None, None, None, None, None

def GUI(doc):
    app = wx.App()
    app.locale = wx.Locale(wx.LANGUAGE_DEFAULT)
    frame = ChatBotFrame(doc, None, wx.ID_ANY, "")
    app.SetTopWindow(frame)
    frame.Show()
    frame.Center()
    return app