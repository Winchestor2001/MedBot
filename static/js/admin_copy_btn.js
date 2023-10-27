let activate_url = document.querySelector('.readonly');

activate_url.insertAdjacentHTML('afterEnd', '<button type="button" class="btn btn-primary mt-2" onclick="copyLink()">Копировать ссылку</button>')


function copyLink() {
    const linkContainer = document.querySelector('.readonly');
    const textToCopy = linkContainer.innerText;

    const textArea = document.createElement('textarea');
    textArea.value = textToCopy;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);

    alert('Ссылка скопирована: ' + textToCopy);
}
