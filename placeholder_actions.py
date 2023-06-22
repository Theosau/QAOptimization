# from llm_actions import suggest_categories
# event_name = "Climate Change Policies"
# event_presenter = "Joe Biden"
# event_database_name = "Climate_Change_Policy_by_Joe_Biden"
# question_list = [
#     "How can we improve the enforcement of existing climate policies for more significant impact?", 
#     "What strategies are being implemented at the national level to transition towards renewable energy?", 
#     "How do current policies address the issue of climate justice, especially for marginalized communities most affected by climate change?", 
#     "What policy changes can help in driving large-scale carbon capture and storage technologies?", 
#     "Can you elaborate on how our climate change policies are aligning with the Paris Agreement goals?", 
#     " What challenges are being faced in implementing climate change policies at a global scale, and how can they be overcome?", 
#     "What will be the future impact of climate change on the price of food?",
#     "Can fictional characters play a role in preventing global warming to increase in the next 40 years?"
# ]
# print(suggest_categories(event_database_name, event_name, event_presenter))


from database_class import EventDatabase

eventdb = EventDatabase('Climate_Change_Policies_by_Joe_Biden')