# langchain RCE test
This project is written on WSL2. Check your environment.
- Ubuntu 24.04 LTS
- Python 3.12.3

1. Clone this repository and move to the directory
```
cd lc_test
```
2. Create a Python virtual environment
```
python3 -m venv myenv
```
3. Activate the environment
```
source myenv/bin/activate
```
4. Install packages from requirements
```
pip install -r requirements.txt
```
5. Run uvicorn
```
uvicorn main:app --reload
```
6. Open the client page (index.html), or you can open 127.0.0.1:8000 from your browser
7. Chat to the langchain application! It allows you to execute any Python code or Linux shell operations.
