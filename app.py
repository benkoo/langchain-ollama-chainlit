import chainlit as cl


@cl.on_chat_start
async def main():
    res = await cl.AskUserMessage(content="What is your name?", timeout=30, author="J_ChATBOT").send()
    if res:
        await cl.Message(
            content=f"Hello {res['output']}! You are watching Chainlit Tutorial!",
            author='J_ChATBOT2'
        ).send()

    # files = None
    
    # while files == None:
    #     files = await cl.AskFileMessage(
    #         content="Please upload a text file to begin!",
    #         accept=["text/plain", ".md"]
    #     ).send()
        
    # text_file = files[0]
    # print(text_file.path)
    # file_path = text_file.path
    # contents = []
    # with open(file_path, 'r') as file:
    #     contents = file.read()
    
    # text = contents
    
    # await cl.Message(
    #     content=f"`{text_file.name}` uploaded, it contains {len(text)} characters."
    # ).send()    
    
    res = await cl.AskActionMessage(
       content="Are you satisfied with the answer? Once you click YES or NO. You can continue asking",
       actions=[
           cl.Action(name="YES", value="YES", lable="YES!!!"),
           cl.Action(name="NO", value="NO", label="NO !!!!!")
       ]
    ).send()

    if res and res.get("value") == "continue":
        await cl.Message(
           content="Continue",
        ).send()

    # text_content = text
    # elements = [
    #     cl.Text(name="TEXT ELEMENT!!", content=text_content, display="inline")
    # ]
    # await cl.Message(content="Check out this text element!", elements=elements).send()
