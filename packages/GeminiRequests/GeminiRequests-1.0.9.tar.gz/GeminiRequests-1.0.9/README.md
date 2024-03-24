# Gemini AI Project


## Setup
To set up the Gemini AI project, follow these steps:

**Install the Gemini Package**
   Within the project directory, execute:
   ```
   pip install GeminiRequests
   ```

## Usage
To use the Gemini AI functionality in your application, follow these steps:

1. Import the `GenerativeAI` class from the `gemini` package:
   ```python
   from gemini.AI import GenerativeAI
   ```

2. Create an instance of the `GenerativeAI` class, providing the necessary `history_file` and `gemini_api_key`:
   ```python
   ai = GenerativeAI('path_to_history_file', 'your_gemini_api_key')
   ```

3. Generate text by calling the `generate_text` method with your input text:
   ```python
   result = ai.generate_text("Your input text here")
   print(result)
   ```

## Contributing
We welcome contributions to the Gemini AI Project! If you're interested in contributing, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with descriptive commit messages.
4. Push your branch and submit a pull request against the main branch.

For more details on contributing, please check out our contributing guidelines.
