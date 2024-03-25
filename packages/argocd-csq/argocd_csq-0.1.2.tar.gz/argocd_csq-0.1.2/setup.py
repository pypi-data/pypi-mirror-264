from setuptools import find_packages, setup

def load_long_description():
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
    return long_description

setup(
    name = 'argocd_csq',
    version = '0.1.2',
    description = 'CS tool to manage ArgoCD',
    packages = find_packages(),
    entry_points={
        'console_scripts': [
            'argocd_csq = argocd_csq.entrypoint_script:main',
        ],
    },
    long_description=load_long_description(),
    long_description_content_type='text/markdown',
    
    install_requires = [
        "colorama==0.4.6",
        "inquirer==3.2.4",
        "PyJWT==2.8.0",
        "Requests==2.31.0",
        "structlog==24.1.0"
    ],
    python_requires = ">=3.10"
)