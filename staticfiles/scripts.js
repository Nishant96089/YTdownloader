document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.download-form').forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            let loader = form.querySelector('.loader');
            let button = form.querySelector('.download-btn');
            loader.style.display = 'inline-block';
            button.disabled = true;
            button.textContent = 'Downloading...';

            let formData = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                body: formData,
            })
            .then(response => response.blob())
            .then(blob => {
                loader.style.display = 'none';
                button.disabled = false;
                button.textContent = 'Download';

                let url = window.URL.createObjectURL(blob);
                let a = document.createElement('a');
                a.href = url;
                a.download = formData.get('format_id') + '.mp4';
                document.body.appendChild(a);
                a.click();
                a.remove();
            })
            .catch(error => {
                console.error('Error:', error);
                loader.style.display = 'none';
                button.disabled = false;
                button.textContent = 'Download';
            });
        });
    });
});
