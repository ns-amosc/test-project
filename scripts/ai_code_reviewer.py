#!/usr/bin/env python3
"""
AI Code Reviewer Script - Enhanced with Custom Prompt Support
Standalone script for AI-powered code review with customizable prompts
"""

import requests
import urllib3
import uuid
import json
import sys
import os
import argparse
import string
import random

# Disable SSL warnings for unverified HTTPS requests
urllib3.disable_warnings()

class AICodeReviewer:
    """AI Code Reviewer with Custom Prompt Support"""

    def __init__(self, token: str, cookies: str):
        """
        Initialize the reviewer

        Args:
            token (str): AI service authentication token
            cookies (str): AI service cookies (required)
        """
        self.token = token
        self.cookies = cookies
        self.api_url = "https://nschat.netskope.io/api/chat/completions"
        self.model = "ollama.deepseek-r1:latest"

    def _generate_session_id(self) -> str:
        """Generate session ID"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(20))

    def _build_headers(self) -> dict:
        """Build HTTP request headers with proper browser simulation"""
        headers = {
            "Authorization": self.token,
            "Cookie": self.cookies,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Cache-Control": "no-cache",
            "Origin": "https://nschat.netskope.io",
            "Referer": "https://nschat.netskope.io/chat"
        }
        return headers

    def _load_prompt_from_file(self, prompt_file: str) -> str:
        """
        Load prompt template from file

        Args:
            prompt_file (str): Path to prompt file

        Returns:
            str: Prompt template content
        """
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            if not content:
                print("⚠️ Warning: Prompt file is empty", file=sys.stderr)
                return ""

            print(f"✅ Loaded prompt from: {prompt_file}", file=sys.stderr)
            return content

        except FileNotFoundError:
            print(f"❌ Error: Prompt file not found: {prompt_file}", file=sys.stderr)
            return ""
        except Exception as e:
            print(f"❌ Error reading prompt file: {str(e)}", file=sys.stderr)
            return ""

    def _build_review_prompt(self, file_path: str, code_changes: str, custom_prompt: str = "") -> str:
        """
        Build code review prompt with optional custom template

        Args:
            file_path (str): File path being reviewed
            code_changes (str): Code changes content
            custom_prompt (str): Custom prompt template (optional)

        Returns:
            str: Final prompt for AI review
        """
        if custom_prompt:
            # Use custom prompt template
            # Replace placeholders if they exist
            prompt = custom_prompt

            # Support common placeholders
            prompt = prompt.replace("{FILE_PATH}", file_path)
            prompt = prompt.replace("{CODE_CHANGES}", code_changes)

            # If no placeholders, append file info to custom prompt
            if "{FILE_PATH}" not in custom_prompt and "{CODE_CHANGES}" not in custom_prompt:
                prompt += f"\n\nFile path: {file_path}\n\nCode changes:\n```diff\n{code_changes}\n```"

            return prompt
        else:
            # Use default prompt template
            default_prompt = f"""Please conduct a professional code review for the following code changes:

File path: {file_path}

Code changes:
```diff
{code_changes}
```

Please provide review feedback on the following aspects:
1. **Code Quality and Best Practices** - Does it follow coding standards?
2. **Potential Bugs or Issues** - Are there any logic errors or edge case problems?
3. **Performance Considerations** - Are there any performance bottlenecks or optimization opportunities?
4. **Security Issues** - Are there any security vulnerabilities or risks?
5. **Maintainability Suggestions** - Is the code easy to understand and maintain?
6. **Specific Improvement Suggestions** - Provide clear modification recommendations

Please respond in English with clear and readable formatting. If the code looks good, please provide a concise explanation and positive feedback.
Please use Markdown format for your response with appropriate headings and lists for better readability."""

            return default_prompt

    def review_code(self, file_path: str, code_changes: str, prompt_file: str = None, verbose: bool = False) -> str:
        """
        Review code changes with optional custom prompt

        Args:
            file_path (str): File path
            code_changes (str): Code changes content
            prompt_file (str): Optional path to custom prompt file
            verbose (bool): Show verbose debug information

        Returns:
            str: Review result
        """
        headers = self._build_headers()

        # Load custom prompt if provided
        custom_prompt = ""
        if prompt_file:
            custom_prompt = self._load_prompt_from_file(prompt_file)
            if verbose and custom_prompt:
                print(f"🔧 Using custom prompt (length: {len(custom_prompt)} chars)", file=sys.stderr)

        # Build final prompt
        review_prompt = self._build_review_prompt(file_path, code_changes, custom_prompt)

        # Prepare request data
        data = {
            "chat_id": str(uuid.uuid4()),
            "id": str(uuid.uuid4()),
            "model": self.model,
            "messages": [{"role": "user", "content": review_prompt}],
            "session_id": self._generate_session_id(),
            "stream": False
        }

        if verbose:
            print(f"🔧 Headers: {json.dumps(headers, indent=2)}", file=sys.stderr)
            print(f"🔧 Model: {data['model']}", file=sys.stderr)
            print(f"🔧 Final prompt length: {len(review_prompt)} chars", file=sys.stderr)

        try:
            print(f"🔍 Reviewing file: {file_path}", file=sys.stderr)
            if prompt_file:
                print(f"📝 Using prompt file: {prompt_file}", file=sys.stderr)

            # Send request with SSL verification disabled
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                verify=False,
                timeout=30
            )

            if verbose:
                print(f"🔧 Response status: {response.status_code}", file=sys.stderr)

            if response.status_code == 200:
                return self._process_response(response, verbose)
            else:
                error_msg = f"❌ API request failed: HTTP {response.status_code}"
                if response.text:
                    error_msg += f"\nResponse content: {response.text[:500]}..."

                if verbose:
                    print(f"🔧 Full error response: {response.text}", file=sys.stderr)

                return error_msg

        except requests.exceptions.Timeout:
            return "❌ Request timeout, please try again later"
        except requests.exceptions.ConnectionError as e:
            return f"❌ Connection error: {str(e)}\nPlease check network or API endpoint"
        except Exception as e:
            return f"❌ Error during review process: {str(e)}"

    def _process_response(self, response, verbose: bool = False) -> str:
        """Process normal HTTP response"""
        try:
            response_data = response.json()

            if verbose:
                print(f"🔧 Response data keys: {list(response_data.keys())}", file=sys.stderr)

            # Extract content from response
            if 'choices' in response_data and response_data['choices']:
                message = response_data['choices'][0].get('message', {})
                content = message.get('content', '')

                if verbose:
                    print(f"🔧 Content length: {len(content)}", file=sys.stderr)

                return content.strip() if content else "⚠️ AI did not respond with any content"
            else:
                return "⚠️ No valid response from AI service"

        except json.JSONDecodeError as e:
            return f"❌ Error parsing response JSON: {str(e)}"
        except Exception as e:
            return f"❌ Error processing response: {str(e)}"


def main():
    """Main program entry point"""
    parser = argparse.ArgumentParser(description='AI Code Review Tool with Custom Prompt Support')
    parser.add_argument('file_path', help='File path to review')
    parser.add_argument('code_changes', help='Code changes content')
    parser.add_argument('--token',
                        help='AI service authentication token (can also be set via AI_TOKEN environment variable)')
    parser.add_argument('--cookies', help='AI service cookies (can also be set via AI_COOKIES environment variable)')
    parser.add_argument('--prompt', '-p', help='Path to custom prompt template file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show verbose information')

    args = parser.parse_args()

    # Get authentication info
    token = args.token or os.getenv('AI_TOKEN')
    cookies = args.cookies or os.getenv('AI_COOKIES')

    # Check required authentication info
    if not token:
        print("❌ Error: No AI service authentication token provided", file=sys.stderr)
        print("Please provide via --token parameter or AI_TOKEN environment variable", file=sys.stderr)
        sys.exit(1)

    if not cookies:
        print("❌ Error: No AI service cookies provided", file=sys.stderr)
        print("Please provide via --cookies parameter or AI_COOKIES environment variable", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"📁 File path: {args.file_path}", file=sys.stderr)
        print(f"🔑 Token length: {len(token)} characters", file=sys.stderr)
        print(f"🍪 Cookies length: {len(cookies)} characters", file=sys.stderr)
        if args.prompt:
            print(f"📝 Custom prompt file: {args.prompt}", file=sys.stderr)

    # Create reviewer and execute review
    reviewer = AICodeReviewer(token, cookies)
    result = reviewer.review_code(args.file_path, args.code_changes, args.prompt, args.verbose)

    # Output result
    print(result)


if __name__ == "__main__":
    main()