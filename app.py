from application.orchestrators.agent import run_agent

def main():
    query = input("Ingrese query: ")
    response = run_agent(query)
    question_response = []
    while response["request_information"].requires_more_information:
        user_answer = 0
        for question in response["request_information"].clarification_questions:
            print(f"{question.name}")
            print("\n".join(
                f"{i} {answer}"
                for i, answer in enumerate(question.alternative_answer, start=1)
            ))
            answer_position = int(input("Responda: "))
            while answer_position <= 0 or answer_position > len(question.alternative_answer):
                position = int(input("Responda: "))
            user_answer = question.alternative_answer[answer_position-1]
            question_response.append(
                f"question: {question.name}\n"
                f"answer: {user_answer}"
            )
        response = run_agent(f"query original: {query}\n\n{'\n'.join(question_response)}")

    print(response["documentation"])           

if __name__ == "__main__":
    main()