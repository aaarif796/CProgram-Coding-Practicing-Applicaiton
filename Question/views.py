# Question/views.py
from django.shortcuts import render, get_object_or_404
from .models import Question, TestCase
import subprocess
import os
import tempfile
import shutil
from django.contrib.auth.decorators import login_required


@login_required
def question_list(request):
    questions = Question.objects.all()
    return render(request, 'question_list.html', {'questions': questions})


@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, question_id=question_id)
    return render(request, 'question_detail.html', {'question': question})


@login_required
def compile_and_run(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        question_id = request.POST.get('question_id', '')
        if not code or not question_id:
            return render(request, 'question_detail.html', {'error': 'No code or question provided', 'code': code})

        try:
            question = Question.objects.get(question_id=question_id)
        except Question.DoesNotExist:
            return render(request, 'question_detail.html', {'error': 'Question does not exist', 'code': code})

        test_cases = question.test_cases.all()

        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        try:
            # Paths
            c_file_path = os.path.join(temp_dir, 'temp.c')
            exe_file_path = os.path.join(temp_dir, 'temp')

            # Write code to temp.c
            with open(c_file_path, 'w') as f:
                f.write(code)

            # Compile code
            compile_command = ['gcc', '-o', exe_file_path, c_file_path]
            compile_result = subprocess.run(compile_command, capture_output=True, text=True)
            
            if compile_result.returncode != 0:
                return render(request, 'question_detail.html', {'error': compile_result.stderr, 'code': code, 'question': question})

            # Run the executable using subprocess and test with test cases
            outputs = []
            for test_case in test_cases:
                try:
                    test_data = test_case.test_data
                    input_data = test_data.split('input:')[1].split('output:')[0].strip()
                    expected_output = test_data.split('output:')[1].strip()

                    process = subprocess.Popen([exe_file_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = process.communicate(input=input_data)
                    output = output.strip()
                    
                    if error or process.returncode != 0:
                        outputs.append(f"Test Case Failed: {test_data}\nError: {error}\n")
                    elif output == expected_output:
                        outputs.append(f"Test Case Passed: {test_data}\nOutput: {output}\n")
                    else:
                        outputs.append(f"Test Case Failed: {test_data}\nExpected: {expected_output}\nGot: {output}\n")
                except Exception as e:
                    outputs.append(f"Test Case Failed: {test_data}\nError: {str(e)}\n")

            return render(request, 'question_detail.html', {'output': '\n'.join(outputs), 'code': code, 'question': question})
        finally:
            # Clean up temporary files and directory
            shutil.rmtree(temp_dir, ignore_errors=True)

    return render(request, 'questions:question_detail.html', {'error': 'Invalid request method.'})