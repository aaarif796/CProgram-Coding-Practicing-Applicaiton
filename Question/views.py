# Question/views.py
from django.shortcuts import render, get_object_or_404
from .models import Question, TestCase, CodeSubmission

import subprocess
import os
import tempfile
import shutil
import re
from django.contrib.auth.decorators import login_required

def extract_test_cases(test_cases):
    extracted_cases = []
    for test_case in test_cases:
        matches = re.findall(r'input\s*:\s*(.*?)\s*output\s*:\s*(.*?)\s*(?=case|$)', test_case.test_data, re.DOTALL)
        for match in matches:
            input_data = match[0].strip()
            expected_output = match[1].strip()
            extracted_cases.append({'input': input_data, 'expected_output': expected_output})
    return extracted_cases

@login_required
def question_list(request):
    questions = Question.objects.all()
    question_status = {}

    for question in questions:
        # Fetch the most recent submission by the user for the current question
        last_submission = CodeSubmission.objects.filter(user=request.user, question=question).order_by('-submitted_at').first()
        
        if last_submission:
            # Get all test cases for the question
            test_cases = question.test_cases.all()
            total_cases = test_cases.count()
            # Count how many test cases were passed in the latest submission
            passed_cases = CodeSubmission.objects.filter(
                user=request.user,
                question=question,
                test_case_pass=True
            ).count()

            # Compare passed cases with total cases
            if passed_cases >= total_cases:
                question_status[question.question_id] = 'Completed'
            else:
                question_status[question.question_id] = 'Not Completed'
        else:
            question_status[question.question_id] = 'Not Attempted'
    print(question_status)
    return render(request, 'question_list.html', {'questions': questions, 'question_status': question_status})


@login_required
def question_detail(request, question_id):
    # question = get_object_or_404(Question, question_id=question_id)
    # user = request.user
    # return render(request, 'question_detail.html', {'question': question})
    question = get_object_or_404(Question, question_id=question_id)
    user = request.user

    # Fetch the most recent submission by the user for the current question
    last_submission = CodeSubmission.objects.filter(user=user, question=question).order_by('-submitted_at').first()
    
    # Prepare context data
    context = {
        'question': question,
        'last_submission': last_submission,  # Include the last submission data
    }

    return render(request, 'question_detail.html', context)


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

        test_cases = extract_test_cases(question.test_cases.all())
        temp_dir = tempfile.mkdtemp()
        score = 0
        max_score_per_case = 1  # Adjust if needed

        try:
            c_file_path = os.path.join(temp_dir, 'temp.c')
            exe_file_path = os.path.join(temp_dir, 'temp')

            with open(c_file_path, 'w') as f:
                f.write(code)

            compile_command = ['gcc', '-o', exe_file_path, c_file_path]
            compile_result = subprocess.run(compile_command, capture_output=True, text=True)
            
            if compile_result.returncode != 0:
                return render(request, 'question_detail.html', {'error': compile_result.stderr, 'code': code, 'question': question})

            outputs = []
            for case in test_cases:
                try:
                    process = subprocess.Popen([exe_file_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    
                    # Set a timeout for the execution
                    output, error = process.communicate(input=case['input'], timeout=2)  # Set timeout to 2 seconds
                    output = output.strip()

                    if error or process.returncode != 0:
                        outputs.append(f"Test Case Failed: Input: {case['input']}\nError: {error}\n")
                    elif output == case['expected_output']:
                        outputs.append(f"Test Case Passed: Input: {case['input']}\nOutput: {output}\n")
                        score += max_score_per_case
                    else:
                        outputs.append(f"Test Case Failed: Input: {case['input']}\nExpected: {case['expected_output']}\nGot: {output}\n")
                except subprocess.TimeoutExpired:
                    process.kill()  # Kill the process if it exceeds the timeout
                    outputs.append(f"Test Case Timeout: Input: {case['input']}\n")
                except Exception as e:
                    outputs.append(f"Test Case Failed: Input: {case['input']}\nError: {str(e)}\n")

            CodeSubmission.objects.create(
                user=request.user,
                question=question,
                code=code,
                test_case_pass=(score == len(test_cases) * max_score_per_case),
                no_of_attempt=CodeSubmission.objects.filter(user=request.user, question=question).count() + 1,  # Update logic for attempts
                score=score
            )

            return render(request, 'question_detail.html', {'output': '\n'.join(outputs), 'code': code, 'question': question, 'score': score})
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    return render(request, 'question_detail.html', {'error': 'Invalid request method.'})
