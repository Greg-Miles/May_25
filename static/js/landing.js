document.addEventListener('DOMContentLoaded', function() {
    const appointment = document.querySelector('button');
    if (appointment) {
        appointment.addEventListener('click', function() {
            window.location.href = '/thanks';
        });
    } else {
        console.error('Кнопки нет.');
    }
});