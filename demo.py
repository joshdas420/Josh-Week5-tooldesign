"""
Demo script showing the text analysis tool in action with an agent workflow.
"""

import json
from tool import analyze_text, text_analysis_tool


def simple_agent(task_description: str, text_input: str, **tool_kwargs):
    """
    A simple agent simulation that uses the text analysis tool.
    In a real scenario, this would be an AI agent, but for demo purposes,
    we simulate the agent's decision-making and tool usage.
    """
    print("=" * 60)
    print(f"AGENT: Processing task - {task_description}")
    print("=" * 60)
    
    # Agent decides which tool to use based on task description
    if "readability" in task_description.lower() or "analyze" in task_description.lower():
        print("AGENT: Selected 'text_analyzer' tool for analysis")
        print(f"AGENT: Calling tool with parameters: {tool_kwargs}")
        print("-" * 40)
        
        # Execute the tool
        result = text_analysis_tool.execute(**tool_kwargs)
        
        # Agent processes and interprets the result
        print("AGENT: Tool execution complete. Interpreting results...")
        return result
    else:
        print("AGENT: No suitable tool found for this task")
        return None


def demo_successful_execution():
    """Demo 1: Successful tool execution with valid input."""
    print("\n" + "=" * 60)
    print("DEMO 1: Successful Text Analysis")
    print("=" * 60)
    
    # Sample business text
    text = """
    Artificial intelligence is transforming the business landscape. Companies are adopting AI 
    solutions to automate processes and gain insights from data. This technology enables better 
    decision-making and improves operational efficiency. However, organizations must carefully 
    consider the ethical implications and implementation challenges.
    """
    
    # Agent task
    result = simple_agent(
        task_description="Analyze text for readability and vocabulary insights",
        text_input=text,
        include_syllables=True
    )
    
    # Display results
    if result and "error" not in result:
        print("\n" + "-" * 40)
        print("ANALYSIS RESULTS:")
        print("-" * 40)
        print(f"Word Count: {result['basic_stats']['word_count']}")
        print(f"Sentence Count: {result['basic_stats']['sentence_count']}")
        print(f"Unique Words: {result['vocabulary_analysis']['unique_word_count']}")
        print(f"Lexical Diversity: {result['vocabulary_analysis']['lexical_diversity']}")
        print(f"Reading Ease: {result['readability_scores']['flesch_reading_ease']}")
        print(f"Grade Level: {result['readability_scores']['flesch_kincaid_grade']}")
        print(f"Reading Level: {result['readability_scores']['reading_level']}")
        print("\nTop 5 Words:")
        top_words = list(result['vocabulary_analysis']['top_10_words'].items())[:5]
        for word, count in top_words:
            print(f"  - '{word}': {count} times")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")


def demo_error_handling():
    """Demo 2: Error handling with invalid input."""
    print("\n" + "=" * 60)
    print("DEMO 2: Error Handling - Invalid Input")
    print("=" * 60)
    
    # Test with empty string
    result = simple_agent(
        task_description="Analyze text",
        text_input="   ",  # Empty after strip
        include_syllables=True
    )
    
    if result and "error" in result:
        print("\n" + "-" * 40)
        print("ERROR HANDLED SUCCESSFULLY:")
        print("-" * 40)
        print(f"Tool returned: {result['error']}")
    
    # Test with wrong type
    print("\n" + "-" * 40)
    print("Testing with wrong input type:")
    print("-" * 40)
    try:
        # This would fail if we don't validate properly
        result = simple_agent(
            task_description="Analyze text",
            text_input=12345,  # Not a string
            include_syllables=True
        )
        if result and "error" in result:
            print(f"Tool returned: {result['error']}")
    except Exception as e:
        print(f"Exception caught: {e}")


def demo_business_use_case():
    """Demo 3: Realistic business use case - content optimization."""
    print("\n" + "=" * 60)
    print("DEMO 3: Business Use Case - Content Optimization")
    print("=" * 60)
    
    # Two versions of marketing text to compare
    texts = {
        "technical": """
        Our enterprise-grade solution leverages cutting-edge artificial intelligence algorithms 
        to facilitate synergistic optimization of organizational workflows. The implementation 
        of our proprietary neural network architecture enables unprecedented levels of 
        operational efficiency and data-driven decision-making capabilities.
        """,
        
        "simple": """
        Our software uses AI to help your team work smarter. It automates routine tasks and 
        provides clear insights from your data. You'll make better decisions faster while 
        reducing manual work and errors.
        """
    }
    
    print("AGENT: Comparing two versions of marketing text for optimization...")
    print("AGENT: Version A - Technical, Version B - Simple\n")
    
    results = {}
    for version, text in texts.items():
        print(f"\nAnalyzing {version.upper()} version:")
        print("-" * 30)
        result = simple_agent(
            task_description="Analyze readability for marketing content",
            text_input=text,
            include_syllables=False
        )
        
        if result and "error" not in result:
            results[version] = result
            print(f"  Word count: {result['basic_stats']['word_count']}")
            print(f"  Reading ease: {result['readability_scores']['flesch_reading_ease']}")
            print(f"  Reading level: {result['readability_scores']['reading_level']}")
    
    # Business decision based on analysis
    print("\n" + "-" * 40)
    print("AGENT: RECOMMENDATION")
    print("-" * 40)
    
    if results:
        tech_score = results['technical']['readability_scores']['flesch_reading_ease']
        simple_score = results['simple']['readability_scores']['flesch_reading_ease']
        
        if simple_score > tech_score:
            print(f"✅ Recommend using SIMPLE version for general audience")
            print(f"   (Reading ease: {simple_score:.1f} vs {tech_score:.1f})")
        else:
            print(f"Technical version may be suitable for expert audience")
            print(f"   Consider simplifying for broader reach")


def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("TEXT ANALYSIS TOOL - INTEGRATION DEMO")
    print("=" * 60)
    
    demo_successful_execution()
    demo_error_handling()
    demo_business_use_case()
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()