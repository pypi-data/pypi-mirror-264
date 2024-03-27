from setuptools import setup, find_packages



VERSION = '0.1'
DESCRIPTION = "GeminiAI-Chat enables easy integration of AI Chat functionalities into Python projects."


# Setting up
setup(
    name="geminiai-chat-python",
    version=VERSION,
    author="mominiqbal1234",
    author_email="<mominiqbal1214@gmail.com>",
    description=DESCRIPTION,
    long_description="""
    # 
    GeminiAI-Chat – the revolutionary Python library designed to power up your applications with advanced conversational AI capabilities
    GeminiAI-Chat, developers can effortlessly integrate AI-driven chat functionalities into their projects,
    # How to install geminiai-chat

    ```python
    pip install geminiai-chat-python
    ```
    # Documentation
    
    GeminiAI-Chat offers a seamless way to incorporate intelligent, responsive AI chat features
    <br>
    https://github.com/MominIqbal-1234/geminiai-chat-python



    Check Our Site : https://mefiz.com/about </br>
    Developed by : Momin Iqbal

    """,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['.env']},
    install_requires=["httpx","python-dotenv"],
    keywords=['geminiai-chat-python','python', 'geminiai-chat', 'geminiai'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)