from setuptools import setup

readme = ""
with open("README.md") as rf:
    readme = rf.read()

requirements = ["langfuse==2.*"]

setup(
    name="totvs-dta-utils",
    author="TotvsLabs",
    version="0.1.1",
    author_email="info@totvs.ai",
    python_requires=">=3.10",
    description="Lib for integration with DTA services",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    include_package_data=True,
    keywords=[
        "dta",
    ],
    packages=[
        "dta_utils",
        "dta_utils.services",
        "dta_utils.services.assets",
        "dta_utils.services.assets.chat_assets",
        "dta_utils.services.assets.chat_assets.Nunito_Sans",
    ],
    url="https://github.com/totvs-ai/dta-utils-python",
)
