#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import subprocess
import sys
from datetime import datetime
import ollama
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

OLLAMA_MODEL = 'qwen2.5-coder:3b'

console = Console()


SYSTEM_PROMPTS = {
    'command': {
        'role': 'system',
        'content': 'You are an expert in shell commands. Given a user\'s question, '
                   'your task is to provide the single, most appropriate shell command that answers the question. '
                   'You remember the conversation history. '
                   'Return ONLY the shell command and nothing else. Do not provide any explanation, '
                   'markdown formatting, or any text other than the command itself.',
    },
    'chat': {
        'role': 'system',
        'content': f'You are a helpful and conversational AI assistant. '
                   f'Provide concise and informative answers. The user is located in Ichhapur Defence Estate, '
                   f'West Bengal, India. The current time is {datetime.now().strftime("%I:%M %p on %A, %B %d, %Y")}.'
    }
}


def get_ollama_response(question: str, messages: list, mode: str) -> str:
    """
    Sends a question to the Ollama model and returns the response.
    The behavior of the response is guided by the 'mode'.

    Args:
        question: The natural language question from the user.
        messages: The list of previous messages in the conversation.
        mode: The current interaction mode ('command' or 'chat').

    Returns:
        The response from the model as a string.
    """
    with console.status(f"[bold cyan]🤔 Thinking... Asking Ollama with model '{OLLAMA_MODEL}'...[/]", spinner="dots"):
        try:
            messages.append({'role': 'user', 'content': question})

            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=messages,
            )
            response_content = response['message']['content'].strip()

            messages.append({'role': 'assistant', 'content': response_content})

            if mode == 'command':
                command = response_content
                if command.startswith("```") and command.endswith("```"):
                    command = command.removeprefix("```").removesuffix("```").strip()
                    if '\n' in command:
                        command = command.split('\n', 1)[-1].strip()
                if command.startswith('`') and command.endswith('`'):
                    command = command.strip('`')
                return command.strip()
            else:
                return response_content

        except Exception as e:
            console.print(f"[bold red]❌ Error communicating with Ollama: {e}[/]")
            console.print("[bold yellow]Please ensure the Ollama application is running and the specified model is available.[/]")
            if messages and messages[-1]['role'] == 'user':
                messages.pop()
            return ""

def execute_command(command: str):
    """
    Executes a shell command using subprocess and prints its output inside a panel.

    Args:
        command: The shell command to execute.
    """
    console.print(f"\n[bold green]Executing command: [yellow]{command}[/yellow][/]")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        
        output_content = ""
        panel_title = ""
        border_style = ""

        if result.returncode == 0:
            panel_title = "✅ Success"
            border_style = "green"
            if result.stdout:
                output_content += f"[bold]Output:[/]\n{result.stdout.strip()}"
            if result.stderr:
                 output_content += f"\n[bold yellow]Standard Error:[/]\n{result.stderr.strip()}"
        else:
            panel_title = "❌ Error"
            border_style = "red"
            output_content += f"[bold]Return Code:[/bold] {result.returncode}\n"
            if result.stdout:
                output_content += f"\n[bold]Standard Output:[/]\n{result.stdout.strip()}"
            if result.stderr:
                output_content += f"\n[bold]Standard Error:[/]\n{result.stderr.strip()}"

        if not output_content.strip():
            output_content = "[dim]Command executed with no output.[/dim]"

        console.print(Panel(output_content, title=panel_title, border_style=border_style, expand=False))

    except FileNotFoundError:
        console.print(f"[bold red]❌ Command not found. Please ensure the command is valid and in your system's PATH.[/]")
    except Exception as e:
        console.print(f"[bold red]❌ An unexpected error occurred: {e}[/]")

def main():
    """
    Main function to run the interactive CLI session.
    """
    art = """
[bold bright_magenta]
██╗    ██╗ █████╗ ██████╗ ██╗
██║    ██║██╔══██╗██╔══██╗██║
██║ █╗ ██║███████║██████╔╝██║
██║███╗██║██╔══██║██╔══██╗██║
╚███╔███╔╝██║  ██║██║  ██║██║██║
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝
[/]
"""
    console.print(art)
    console.print("[bold green]Shell & Chat Assistant[/]")
    console.print("[dim]Default is [bold]Command Mode[/]. Type '/chat' to switch to Chat Mode or '/command' to switch back.[/dim]")
    console.print("[dim]Type 'exit' or 'quit' to end the session.[/dim]")
    
    current_mode = 'command'
    messages = [SYSTEM_PROMPTS[current_mode]]

    while True:
        try:
            prompt_style = "bold cyan" if current_mode == 'command' else "bold magenta"
            question = Prompt.ask(f"\n[{prompt_style}]You ({current_mode.capitalize()} Mode)[/]").strip()

            if not question:
                continue

            if question.lower() in ['exit', 'quit']:
                console.print("[bold yellow]👋 Goodbye![/]")
                break

            if question.lower() == '/chat':
                current_mode = 'chat'
                messages[0] = SYSTEM_PROMPTS[current_mode] 
                console.print("\n[bold magenta]💬 Switched to Chat Mode.[/] Ask me anything!")
                continue 
            
            if question.lower() == '/command':
                current_mode = 'command'
                messages[0] = SYSTEM_PROMPTS[current_mode] 
                console.print("\n[bold cyan]👨‍💻 Switched to Command Mode.[/] Ask for a shell command.")
                continue 

            if current_mode == 'command':
                command = get_ollama_response(question, messages, mode='command')

                if not command:
                    console.print("[bold red]Could not determine a command to execute. Please try another question.[/]")
                    continue
                
                console.print(Panel(f"[bold yellow]{command}[/]", title="🤖 Suggested Command", border_style="blue", expand=False))

                confirm = Prompt.ask("Do you want to execute this command?", choices=["y", "n"], default="y")
                if confirm == 'y':
                    execute_command(command)
                else:
                    console.print("[bold yellow]👍 Command execution cancelled.[/]")
            
            elif current_mode == 'chat':
                response_text = get_ollama_response(question, messages, mode='chat')
                if response_text:
                    console.print(Panel(response_text, title="🤖 Assistant", border_style="magenta", expand=False))

        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold yellow]👋 Goodbye![/]")
            sys.exit(0)


if __name__ == "__main__":
    main()