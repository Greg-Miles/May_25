document.addEventListener('DOMContentLoaded', function() {
    const appointment = document.querySelector('.make_appointment_btn');
    if (appointment) {
        appointment.addEventListener('click', function() {
            window.location.href = '/thanks';
        });
    } else {
        console.error('Кнопки нет.');
    }
    
    // Новый код для автоматического закрытия сообщений
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            // Проверяем, доступен ли bootstrap.Alert
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                var bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } else {
                // Если bootstrap.Alert недоступен, используем простое скрытие
                alert.style.opacity = '0';
                setTimeout(function() {
                    alert.style.display = 'none';
                }, 500); // Задержка для анимации исчезновения
            }
        });
    }, 5000); // Закрыть через 5 секунд
});