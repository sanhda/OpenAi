import wx
import openai
import os
from openai import OpenAI
import asyncio
from pathlib import Path

client = OpenAI(
    api_key="sk-name-P2uMlZS23qQS9cdVPteiT3BlbkFJvE5N1lguoPock5j3I2AV"
)

conversation_state = {
    "action": None,
    "object": "wall_rebar",
    "details": {
        "horizontal diameter": 12,
        "vertical diameter": 10,
        "spacing": 100
    }
}

action_keys = ["create rebar", "add", "remove", "increase", "decrease", "change"]

class ChatBotFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(ChatBotFrame, self).__init__(*args, **kwargs)
        
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.chat_display = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.sizer.Add(self.chat_display, 1, wx.EXPAND | wx.ALL, 5)
        
        self.user_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.sizer.Add(self.user_input, 0, wx.EXPAND | wx.ALL, 5)
        
        self.user_input.Bind(wx.EVT_TEXT_ENTER, self.on_enter_pressed)
        
        self.panel.SetSizer(self.sizer)
        self.SetTitle('Chatbot Interface')
        self.Show()
    
    def on_enter_pressed(self, event):
        user_message = self.user_input.GetValue()
        self.chat_display.AppendText(f'You: {user_message}\n')
        
        response = self.get_bot_response(user_message, conversation_state)
        self.chat_display.AppendText(f'Bot: {response}\n')
        
        self.user_input.SetValue('')

    def get_bot_response(self, prompt, current_state):
      details_keys = "; ".join([f"{key}=<value>mm" for key in current_state["details"].keys()])
      valid_actions = "; ".join(action_keys)

      conversation = [
          {"role": "system", "content": f"You are a helpful assistant. Interpret user requests for actions on wall rebar creation and modification." \
               + " Respond in English. The action must be one of the following: {valid_actions}. " \
               + " If the request is an action, respond with 'Action: <action>, Object: <object>, Details: {details_keys}'. " \
               + "If you cannot provide specific details, respond with 'Action: <action>, Object: <object>, Details: {{}}'. " \
               + " If the request is a chat, respond with 'Chat: <response>'."},
          {"role": "user", "content": prompt}
      ]

      response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation,
        max_tokens=150
      )

      ai_response = response.choices[0].message.content
      response_type, action, obj, details = self.parse_response(ai_response)

      if response_type == "action":
        self.update_conversation_state(action, obj, details, conversation_state)
        print(conversation_state)
        return f"Action: {action}, Object: {obj}, Details: {details}"
      elif response_type == "chat":
        return f"Chat Response: {action}"
      else:
        return "Sorry, can not understand you"

    def parse_response(self, response):
      if response.startswith("Action:"):
          parts = response.split(", ")
          action = parts[0].split(": ")[1].strip()
          obj = parts[1].split(": ")[1].strip() if len(parts) > 1 else None
          details = parts[2].split(": ")[1].strip() if len(parts) > 2 else ""
          return "action", action, obj, details
      elif response.startswith("Chat:"):
          chat_response = response.split(": ", 1)[1].strip()
          return "chat", chat_response, None, None
      else:
          return None, None, None, None

    def update_conversation_state(self, action, obj, details, state):
      if action.lower() in ["create rebar", "create"]:
        state["action"] = "create"
        state["object"] = "wall_rebar"
      
      if details:
        for key, value in details.items():
            if key in state["details"]:
              value = convert_to_mm(value)

              if action.lower() == ""
                state["details"][key] = convert_to_mm(value)

    def convert_to_mm(self, value):
      # Kiểm tra và chuyển đổi giá trị với đơn vị "cm"
      if value.endswith("cm"):
          return str(float(value.replace("cm", "").strip()) * 10) + "mm"
      # Kiểm tra và chuyển đổi giá trị với đơn vị "m"
      if value.endswith("m"):
          return str(float(value.replace("m", "").strip()) * 1000) + "mm"
      # Nếu không có đơn vị, mặc định là "mm"
      if not value.endswith("mm"):
          return value + "mm"
      return value

app = wx.App(False)
frame = ChatBotFrame(None, size=(600, 400))
app.MainLoop()
