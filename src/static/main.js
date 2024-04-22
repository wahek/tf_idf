document.getElementById('select-lev').addEventListener('change', function() {
    const selectedOption = this.value;
    let dynamicText = '';

    // Проверяем выбранное значение и устанавливаем соответствующий текст
    if (selectedOption === '0') {
        dynamicText = 'Предупреждение: уровень точности объединяет слова с разными окончаниями (природа | природу)';
    } else if (selectedOption === '1') {
        dynamicText = 'Предупреждение: уровень точности объединяет слова с опечатками. Есть вероятность попадания разных слов в одну группу (крот | грот)';
    }

    // Выводим динамический текст
    const dynamicTextElement = document.getElementById('warning-text');
    dynamicTextElement.textContent = dynamicText;
});

document.getElementById('fileInput').addEventListener('change', function() {
    const fileName = this.files[0].name;
    const color = 'MediumSpringGreen';
    const label = document.querySelector('.custom-upload-button > span');
    const div = document.querySelector('.custom-upload-button');

    const submitButton = document.querySelector('.submit-button');

    const fileExtension = fileName.split('.').pop();

    if (fileExtension !== 'txt') {
        alert('Приложение поддерживает только расширение файла txt');
        return;
    }


    label.textContent = fileName;
    div.style.backgroundColor = color;
    submitButton.style.backgroundColor = 'LightSteelBlue';
    submitButton.style.color = 'black';
    submitButton.border = '1px solid black';
    submitButton.removeAttribute('disabled');

});

