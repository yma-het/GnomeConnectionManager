import pytermgui as ptg

with ptg.WindowManager() as manager:
   demo = ptg.Window(
      ptg.Label("[210 bold]Hello world!"),
      ptg.Label(),
      ptg.InputField(prompt="Who are you?"),
      ptg.Label(),
      ptg.Button("Submit!")
   )
   
   manager.add(demo)
   manager.run()