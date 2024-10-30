from setuptools import setup, find_packages

# Read README file for long description (optional, recommended for PyPI)
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ai_text_processor",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for AI text processing tasks such as text generation, summarization, and translation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai_text_processor",  # Replace with your GitHub repo or package URL
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "ai-text-processor=ai_text_processor.processor:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
