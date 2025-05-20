# from openai import OpenAI
# import json

# # Initialize OpenAI client
# client = OpenAI()

# # Function to load IDs from a file

# assistant_id = "asst_3i5D8GsOpJrIAMyBChDmgoDK"
# #asst_3i5D8GsOpJrIAMyBChDmgoDK
# #asst_sm2mmHPOVtkkPTRbVyjMT3ev # first one

# # Function to interact with the assistant
# def ask_assistant(prompt):
#     # Create a thread and attach the file to the message
#     thread = client.beta.threads.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt,
#                 "attachments": [],
#             }
#         ]
#     )

#     # Use the create and poll SDK helper to create a run and poll the status of the run until it's in a terminal state.
#     run = client.beta.threads.runs.create_and_poll(
#         thread_id=thread.id, assistant_id=assistant_id
#     )

#     messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

#     message_content = messages[0].content[0].text
#     annotations = message_content.annotations
#     citations = []
#     for index, annotation in enumerate(annotations):
#         message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
#         if file_citation := getattr(annotation, "file_citation", None):
#             cited_file = client.files.retrieve(file_citation.file_id)
#             citations.append(f"[{index}] {cited_file.filename}")

#     print("\033[92m"+ message_content.value +"\033[0m")
#     #print("\n".join(citations))




def handle_error(error_message, AI):
    """Handles errors based on the AI flag."""
    if (AI == True):
        print("\033[91m"+ error_message +"\033[0m")  # red
        # ask_assistant(error_message)
        raise SyntaxError("\033[92m"+ "Flex AI :)" +"\033[0m") # green
    else:
        raise SyntaxError("\033[91m"+ error_message +"\033[0m") # red

