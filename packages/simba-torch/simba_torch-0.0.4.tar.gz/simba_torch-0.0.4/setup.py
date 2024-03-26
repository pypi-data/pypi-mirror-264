# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simba_torch']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'simba-torch',
    'version': '0.0.4',
    'description': 'Paper - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Simba\nA simpler Pytorch + Zeta Implementation of the paper: "SiMBA: Simplified Mamba-based Architecture for Vision and Multivariate Time series"\n\n\n## install\n`$ pip install simba-torch`\n\n## usage\n```python\n\nimport torch \nfrom simba_torch.main import Simba\n\n# Forward pass with images\nimg = torch.randn(1, 3, 224, 224)\n\n# Create model\nmodel = Simba(\n    dim = 4,                # Dimension of the transformer\n    dropout = 0.1,          # Dropout rate for regularization\n    d_state=64,             # Dimension of the transformer state\n    d_conv=64,              # Dimension of the convolutional layers\n    num_classes=64,         # Number of output classes\n    depth=8,                # Number of transformer layers\n    patch_size=16,          # Size of the image patches\n    image_size=224,         # Size of the input image\n    channels=3,             # Number of input channels\n    # use_pos_emb=True # If you want\n)\n\n# Forward pass\nout = model(img)\nprint(out.shape)\n\n```\n\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/Simba',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
