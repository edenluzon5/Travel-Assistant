# test_debug.py - Test script to demonstrate Chain of Thought functionality
import os
from assistant import TravelAssistant

def test_chain_of_thought():
    """Test and demonstrate chain of thought functionality"""
    
    print("=" * 60)
    print("CHAIN OF THOUGHT DEMONSTRATION")
    print("=" * 60)
    print("This script demonstrates the Chain of Thought (CoT) functionality")
    print("required for the travel assistant assignment.")
    print()
    
    # Test question that triggers complex reasoning
    test_question = (
        "My friend and I (in our late 20s) are looking to plan a two-week trip for this "
        "upcoming January. We're on a pretty tight budget. We love adventurous travel—long "
        "hikes and amazing nature are a must—but we also want to experience some unique "
        "city life and maybe some nightlife. We're based in Israel and are open to a long "
        "flight if it means cheaper costs on the ground. It's important for us to avoid "
        "places that are freezing cold."
    )

    
    print(f"Test Question: {test_question}")
    print()
    
    # Test 1: Normal Mode (Final Answer Only)
    print("1. NORMAL MODE (SHOW_CHAIN_OF_THOUGHT=false)")
    print("-" * 50)
    os.environ["SHOW_CHAIN_OF_THOUGHT"] = "false"
    assistant_normal = TravelAssistant()
    
    response_normal = assistant_normal.get_response(test_question)
    print("Response (Final Answer Only):")
    print(response_normal)
    print()
    
    # Test 2: Debug Mode (Thinking Process Only)
    print("2. DEBUG MODE (SHOW_CHAIN_OF_THOUGHT=true)")
    print("-" * 50)
    os.environ["SHOW_CHAIN_OF_THOUGHT"] = "true"
    assistant_debug = TravelAssistant()
    
    response_debug = assistant_debug.get_response(test_question)
    print("Response (Thinking Process Only):")
    print(response_debug)
    print()
    

if __name__ == "__main__":
    test_chain_of_thought()
