# app.py
import streamlit as st
import re
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Initialize LLM
llm = OllamaLLM(model="llama3.2")

# Initialize session state
if "stage" not in st.session_state:
    st.session_state.stage = "greeting"
if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {
        "answers": [],
        "assessment_questions": []
    }
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "👋 Hi! I'm TalentBot. Let's start by collecting your details!"}]
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0

# Define prompt templates
tech_prompt = ChatPromptTemplate.from_template("""
    Generate 3 technical interview questions to assess proficiency across these technologies: {tech_stack}.
    Questions should cover fundamental concepts and practical applications.
    Format: 1. [Question] 2. [Question] 3. [Question]
""")

def generate_tech_questions(tech_stack):
    """Generate technical questions using LLM"""
    response = llm.invoke(tech_prompt.format(tech_stack=", ".join(tech_stack)))
    return response

def parse_questions(response):
    """Parse numbered questions from LLM response"""
    questions = re.findall(r'\d+\.\s*(.*?)(?=\s*\d+\.|\s*$)', response, re.DOTALL)
    return [q.strip() for q in questions if q.strip()]

def main():
    st.title("TalentScout Hiring Assistant")
    
    # Display chat messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Auto-generate questions after tech stack input
    if st.session_state.stage == "generate_questions":
        tech_stack = st.session_state.candidate_data.get("tech_stack", [])
        response = generate_tech_questions(tech_stack)
        questions = parse_questions(response)
        
        if len(questions) >= 3:
            st.session_state.candidate_data["assessment_questions"] = questions
            first_question = f"📝 Question 1: {questions[0]}"
            st.session_state.messages.append({"role": "assistant", "content": first_question})
            st.session_state.stage = "answering_questions"
        else:
            error_msg = "❌ Failed to generate questions. Please try again later."
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.session_state.stage = "exit"
        
        st.rerun()

    # Process user input
    if prompt := st.chat_input("Type here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        if "exit" in prompt.lower():
            st.session_state.stage = "exit"

        bot_response = None
        
        # Conversation logic
        if st.session_state.stage == "greeting":
            bot_response = "Welcome to TalentScout! Let's begin with your full name:"
            st.session_state.stage = "collect_info"
        
        elif st.session_state.stage == "collect_info":
            if "name" not in st.session_state.candidate_data:
                st.session_state.candidate_data["name"] = prompt
                bot_response = "📧 Great! What's your email address?"
            elif "email" not in st.session_state.candidate_data:
                st.session_state.candidate_data["email"] = prompt
                bot_response = "📅 How many years of professional experience do you have?"
            elif "experience" not in st.session_state.candidate_data:
                st.session_state.candidate_data["experience"] = prompt
                bot_response = "💻 List the technologies you're familiar with (comma-separated):"
                st.session_state.stage = "tech_stack"
        
        elif st.session_state.stage == "tech_stack":
            st.session_state.candidate_data["tech_stack"] = [t.strip() for t in prompt.split(",")]
            bot_response = "🔧 Generating assessment questions..."
            st.session_state.stage = "generate_questions"
        
        elif st.session_state.stage == "answering_questions":
            current_idx = st.session_state.current_question_index
            questions = st.session_state.candidate_data["assessment_questions"]
            
            # Store answer
            st.session_state.candidate_data["answers"].append({
                "question": questions[current_idx],
                "answer": prompt
            })
            
            # Move to next question or complete
            st.session_state.current_question_index += 1
            if st.session_state.current_question_index < len(questions):
                next_q = f"📝 Question {st.session_state.current_question_index + 1}: {questions[st.session_state.current_question_index]}"
                bot_response = next_q
            else:
                bot_response = "✅ Assessment complete! Thank you for your time."
                st.session_state.stage = "exit"
                # Here you can add code to store the final data
                st.write("Final collected data:", st.session_state.candidate_data)
        
        elif st.session_state.stage == "exit":
            bot_response = "👋 Thank you! We'll review your application. Good luck!"
        
        else:
            bot_response = "❌ I didn't understand that. Please try again or say 'exit' to end."

        if bot_response:
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            st.rerun()

if __name__ == "__main__":
    main()