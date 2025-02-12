from Helena import Helena

while True:
    user_input = input("User: ")
    if user_input.lower() == "sair":
        break
    response = Helena.response('Wellington', user_input)
    print(f"Helena: {response['message']}") 

""" 
from pprint import pprint
import inquirer

questions = [
    inquirer.List(
        "quest",
        message="Pegar",
        choices=["opção 1", "opção 2", "opção 3"],
    ),
]

answers = inquirer.prompt(questions)
pprint(answers['quest']) """