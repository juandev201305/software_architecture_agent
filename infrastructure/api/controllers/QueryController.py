from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from application.orchestrators.agent import arun_agent
import json 

router = APIRouter()

@router.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()

    try:
        try:
            data = await websocket.receive_json()
            original_query = data.get("content")
        except WebSocketDisconnect:
            return

        response = await arun_agent(original_query)
        question_response = []

        while response["request_information"].requires_more_information:
            for question in response["request_information"].clarification_questions:
                payload = {
                    "status": "NEED_INFO",
                    "question": question.name,
                    "options": question.alternative_answer
                }
                await websocket.send_json(payload)

                try:
                    client_message = await websocket.receive_json()
                    user_answer = client_message.get("answer")
                except WebSocketDisconnect:
                    return
                    
                question_response.append(
                    f"question: {question.name}\n"
                    f"answer: {user_answer}"
                )

            new_query = f"query original: {original_query}\n\n{'\n'.join(question_response)}"
            response = await arun_agent(new_query)
        
        await websocket.send_json({
            "status": "SUCCESS",
            "documentation": response["documentation"]
        })
    except Exception as e:
        await websocket.send_json({"status": "ERROR", "details": str(e)})
    except WebSocketDisconnect:
        print("El cliente cerró la conexión. Estado liberado de la memoria.")