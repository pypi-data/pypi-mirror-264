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
