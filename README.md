# TalentScout Hiring Assistant

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-v1.0-blue.svg)](https://streamlit.io/)

TalentScout Hiring Assistant is an interactive, chat-based application built with Streamlit. It leverages Langchain's OllamaLLM to generate dynamic technical interview questions based on a candidate's provided tech stack. This tool streamlines candidate screening by guiding candidates through an engaging conversation where they share their details and answer assessment questions.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview
TalentScout Hiring Assistant helps hiring teams quickly evaluate candidates by:
- Collecting essential candidate information (name, email, years of experience).
- Accepting a list of familiar technologies from the candidate.
- Generating three technical interview questions based on the candidate's tech stack using an LLM.
- Recording candidate responses in a structured format.

This repository contains a single main file, `app.py`, which manages session state, the conversation flow, and LLM integrations.

## Features
- **Conversational UI:** Utilizes Streamlit’s chat interface for a natural dialogue experience.
- **Dynamic Question Generation:** Generates tailored technical questions using the `OllamaLLM` model.
- **State Management:** Uses Streamlit's session state to track candidate progress.
- **Customizable Prompts:** The prompt template for generating questions is easily adjustable.

## How It Works
1. **Greeting & Information Collection:**  
   The assistant starts by greeting the candidate and requesting basic details (full name, email, years of experience).

2. **Tech Stack Input:**  
   The candidate is prompted to provide their familiar technologies as a comma-separated list.

3. **Question Generation:**  
   Using the provided tech stack, the application invokes the LLM to generate three technical interview questions.

4. **Assessment:**  
   The candidate answers each generated question sequentially.

5. **Completion:**  
   Once all questions are answered, the application displays a confirmation message and logs the final candidate data.

## Installation

### Prerequisites
- **Python 3.8 or higher**
- **Streamlit**
- **Langchain Modules:** `langchain_ollama` and `langchain_core`
- The built-in Python `re` module (part of the standard library)

### Clone the Repository
```bash
git clone https://github.com/yourusername/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant
