# MaiTai Python SDK Guide

Welcome to the MaiTai Python SDK guide. This document will help you get started with integrating the MaiTai SDK into your application for evaluating AI outputs. Follow the steps below to install, configure, and use the SDK effectively.

## Installation

To install the MaiTai SDK, run the following command in your terminal:

```bash
pip install maitai-python
```

## Configuration

Before you can start evaluating AI outputs, you need to set your `application_id` and `api_key`. These credentials are essential for authenticating your requests to the MaiTai service.

1. Obtain your `application_id` and `api_key` from the MaiTai platform.
2. Configure these values in your application as shown below:

```python
import maitai

maitai.api_key = 'your_api_key_here'
maitai.application_id = 'your_application_id_here'
```

## Updating Session Context

Before evaluating AI output, you may need to update the session context with relevant information. This context helps in tailoring the evaluation process. Follow these steps to update the session context:

1. Ensure your `application_id` and `api_key` are set as described in the Configuration section.
2. Use the `update_session_context` method of the `Evaluator` class, providing a `session_id` and a context dictionary. The `session_id` is an identifier of your choosing, and the context is a dictionary of key-value pairs, where the key describes the context piece passed as the value.

Here's an example of how to update the session context:

```python
import maitai

# Your session ID and the context you want to update
session_id = 'your_session_id_here'
context = {
    'user_age': 25,
    'user_interests': ['technology', 'music']
}

# Update the session context
maitai.Evaluator.update_session_context(session_id, context)
```

## Evaluating AI Output

To evaluate AI output, you'll need to use the `Evaluator` class provided by the SDK. Here's a simple example of how to evaluate a text content:

```python
import maitai

# Your session ID and the content you want to evaluate
session_id = 'your_session_id_here'
content = 'The content you want to evaluate'

# Evaluate the content
maitai.Evaluator.evaluate(session_id, content)
```

This will send the evaluation request to the MaiTai service asynchronously. Ensure that your `application_id` and `api_key` are correctly set as shown in the Configuration section above.

## Conclusion

You're now ready to start using the MaiTai Python SDK to evaluate AI outputs in your application. Remember to follow best practices for managing your `api_key` and `application_id` securely within your application. If you encounter any issues or have further questions, refer to the [MaiTai Documentation](https://docs.maitai.ai) or reach out to the support team.
