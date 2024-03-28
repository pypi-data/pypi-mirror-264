from setuptools import setup, find_packages

setup(
    name='DataPrekit',
    version='0.1',
    packages=find_packages(),
    description='A toolkit for preprocessing datasets for machine learning and data analysis.',
    author='aseel thobaity',
    author_email='a9ile20@gmail.com',
    install_requires=[
        'pandas',
        'numpy',
        # أي تبعيات أخرى تحتاجها
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # يمكن تغيير هذا حسب حالة مشروعك
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # تأكد من اختيار الترخيص المناسب لمشروعك
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
