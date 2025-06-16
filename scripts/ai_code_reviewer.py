#!/usr/bin/env python3
"""
AI Code Reviewer Script
Standalone script for AI-powered code review
Supports reading authentication info from environment variables
"""

import requests
import urllib3
import uuid
import json
import sys
import os
import argparse
from typing import Optional

# Disable SSL warnings for unverified HTTPS requests
urllib3.disable_warnings()


class AICodeReviewer:
    """AI Code Reviewer"""

    def __init__(self, token: str, cookies: Optional[str] = None):
        """
        Initialize the reviewer

        Args:
            token (str): AI service authentication token
            cookies (str, optional): AI service cookies
        """
        self.token = token
        self.cookies = cookies
        self.api_url = "https://nschat.netskope.io/api/chat/completions"
        self.model = "ollama.deepseek-r1:latest"

    def _build_headers(self) -> dict:
        """Build HTTP request headers"""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (GitHub Actions Code Review Bot)",
            "Accept": "text/event-stream",
            "Cache-Control": "no-cache",
            "Origin": "https://nschat.netskope.io",
            "Referer": "https://nschat.netskope.io/chat"
        }

        # Add cookies to headers if available
        if self.cookies:
            headers["Cookie"] = self.cookies

        return headers

    def _load_custom_prompt(self, prompt_file: str = "prompt.md") -> Optional[str]:
        """
        Load custom prompt file

        Args:
            prompt_file (str): Path to prompt file

        Returns:
            Optional[str]: Prompt content, or None if file doesn't exist
        """
        try:
            if os.path.exists(prompt_file):
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        print(f"✅ Loaded custom prompt file: {prompt_file}", file=sys.stderr)
                        return content
            return None
        except Exception as e:
            print(f"⚠️ Failed to load prompt file: {str(e)}", file=sys.stderr)
            return None

    def _build_review_prompt(self, file_path: str, code_changes: str, custom_prompt: Optional[str] = None) -> str:
        """
        Build code review prompt

        Args:
            file_path (str): File path
            code_changes (str): Code changes
            custom_prompt (str, optional): Custom prompt content
        """
        # Basic review context
        base_context = f"""
File path: {file_path}

Code changes:
```diff
{code_changes}
```
"""

        # Use custom prompt if available, otherwise use default
        if custom_prompt:
            # Combine custom prompt with code changes
            full_prompt = f"""{custom_prompt}

{base_context}

Please review this code change according to the above guidelines."""
        else:
            # Use default review prompt
            full_prompt = f"""
Please conduct a professional code review for the following code changes:

{base_context}

Please provide review feedback on the following aspects:
1. **Code Quality and Best Practices** - Does it follow coding standards?
2. **Potential Bugs or Issues** - Are there any logic errors or edge case problems?
3. **Performance Considerations** - Are there any performance bottlenecks or optimization opportunities?
4. **Security Issues** - Are there any security vulnerabilities or risks?
5. **Maintainability Suggestions** - Is the code easy to understand and maintain?
6. **Specific Improvement Suggestions** - Provide clear modification recommendations

Please respond in English with clear and readable formatting. If the code looks good, please provide a concise explanation and positive feedback.
Please use Markdown format for your response with appropriate headings and lists for better readability."""

        return full_prompt

    def review_code(self, file_path: str, code_changes: str, prompt_file: str = "prompt.md") -> str:
        """
        Review code changes

        Args:
            file_path (str): File path
            code_changes (str): Code changes content
            prompt_file (str): Custom prompt file path

        Returns:
            str: Review result
        """
        headers = self._build_headers()

        # Load custom prompt
        custom_prompt = self._load_custom_prompt(prompt_file)
        review_prompt = self._build_review_prompt(file_path, code_changes, custom_prompt)

        # Prepare request data
        data = {
            "chat_id": str(uuid.uuid4()),
            "id": str(uuid.uuid4()),
            "model": self.model,
            "messages": [{"role": "user", "content": review_prompt}],
            "session_id": str(uuid.uuid4())[:20],
            "stream": True
        }

        try:
            print(f"🔍 Reviewing file: {file_path}", file=sys.stderr)

            # Send request
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                verify=False,
                stream=True,
                timeout=120  # Increase timeout
            )

            if response.status_code == 200:
                return self._process_streaming_response(response)
            else:
                error_msg = f"❌ API request failed: HTTP {response.status_code}"
                if response.text:
                    error_msg += f"\nResponse content: {response.text[:200]}..."
                return error_msg

        except requests.exceptions.Timeout:
            return "❌ Request timeout, please try again later"
        except requests.exceptions.ConnectionError:
            return "❌ Connection error, please check network or API endpoint"
        except Exception as e:
            return f"❌ Error during review process: {str(e)}"

    def _process_streaming_response(self, response) -> str:
        """Process streaming response"""
        full_content = ""

        try:
            for line in response.iter_lines(decode_unicode=True):
                if line and line.startswith('data: '):
                    data_content = line[6:]  # Remove 'data: ' prefix

                    # Check for end marker
                    if data_content == '[DONE]':
                        break

                    try:
                        # Parse JSON data
                        chunk_data = json.loads(data_content)

                        # Extract content
                        if 'choices' in chunk_data and chunk_data['choices']:
                            delta = chunk_data['choices'][0].get('delta', {})
                            if 'content' in delta:
                                content = delta['content']
                                full_content += content

                    except json.JSONDecodeError:
                        # Skip invalid JSON
                        continue

        except Exception as e:
            return f"❌ Error processing response: {str(e)}"

        return full_content.strip() if full_content else "⚠️ AI did not respond with any content"


def main():
    """Main program entry point"""
    parser = argparse.ArgumentParser(description='AI Code Review Tool')
    parser.add_argument('file_path', help='File path to review')
    parser.add_argument('code_changes', help='Code changes content')
    parser.add_argument('--prompt-file', default='prompt.md', help='Custom prompt file path (default: prompt.md)')
    parser.add_argument('--token',
                        help='AI service authentication token (can also be set via AI_TOKEN environment variable)')
    parser.add_argument('--cookies', help='AI service cookies (can also be set via AI_COOKIES environment variable)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show verbose information')

    args = parser.parse_args()

    # Get authentication info
    token = args.token or os.getenv('AI_TOKEN')
    cookies = args.cookies or os.getenv('AI_COOKIES')

    if not token:
        print("❌ Error: No AI service authentication token provided", file=sys.stderr)
        print("Please provide via --token parameter or AI_TOKEN environment variable", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"📁 File path: {args.file_path}", file=sys.stderr)
        print(f"📄 Prompt file: {args.prompt_file}", file=sys.stderr)
        print(f"🔑 Token length: {len(token)} characters", file=sys.stderr)
        print(f"🍪 Cookies: {'Provided' if cookies else 'Not provided'}", file=sys.stderr)

    # Create reviewer and execute review
    reviewer = AICodeReviewer(token, cookies)
    result = reviewer.review_code(args.file_path, args.code_changes, args.prompt_file)

    # Output result
    print(result)


if __name__ == "__main__":
    main()