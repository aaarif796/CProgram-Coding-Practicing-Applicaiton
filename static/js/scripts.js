function compileAndRun() {
    const code = document.getElementById('code-input').value;

    // Get CSRF token from cookie
    const csrftoken = getCookie('csrftoken');

    // Make POST request with CSRF token included in headers
    fetch('/compile-and-run/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: 'code=' + encodeURIComponent(code)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            document.getElementById('output').innerText = 'Error: ' + data.error;
        } else {
            document.getElementById('output').innerText = 'Output: ' + data.output;
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        document.getElementById('output').innerText = 'Fetch error: ' + error.message;
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
