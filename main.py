import argparse
import sys
from agent import create_stock_agent

def run_interactive(agent):
    print("==================================================")
    print("   Stock Price Agent (powered by LangChain & Groq)")
    print("==================================================")
    print("Type your stock queries below. Type 'exit' or 'quit' to close.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            print("\nAgent is thinking...")
            response = agent.invoke({"input": user_input})
            print(f"\nAgent:\n{response['output']}\n")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError executing query: {e}\n")

def main():
    parser = argparse.ArgumentParser(description="Stock Price AI Agent using LangChain and Groq API.")
    parser.add_argument("query", nargs="?", type=str, help="A single query to run instead of interactive mode.")
    parser.add_argument("--model", type=str, default="llama-3.1-8b-instant", 
                        help="Groq LLM model name (default: llama-3.1-8b-instant)")
    parser.add_argument("--temp", type=float, default=0.0, 
                        help="LLM temperature (default: 0.0)")
                        
    args = parser.parse_args()
    
    try:
        agent = create_stock_agent(model_name=args.model, temperature=args.temp)
    except Exception as e:
        print(f"Initialization Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    if args.query:
        # Run single query
        try:
            print(f"Query: {args.query}")
            print("Agent is thinking...\n")
            response = agent.invoke({"input": args.query})
            print(f"Agent Response:\n{response['output']}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Run interactive loop
        run_interactive(agent)

if __name__ == "__main__":
    main()
